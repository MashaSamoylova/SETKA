#!/usr/bin/env python3
import sys
import pathlib
import os
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import Slider

from windows.mainwindow import Ui_MainWindow
from windows.settings import Ui_Dialog
from windows.editordialog import Ui_EditorDialog
from windows.connectdialog import Ui_Dialog as Ui_ConnectDialog
from windows.graphicsdialog import Ui_GraphicsDialog
from pyboard import PyBoard, error_map
from utils import to_float, chunkstring

pyboard = PyBoard()

class MatplotlibWidget(QtWidgets.QWidget):

    timelen = 900
    ticks = []

    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        # self.canvas.setMinimumSize(QtCore.QSize(1500, 0))

        self.axis = self.figure.add_subplot(111)
        self.update(0)
        #self.spos = Slider(self.axis, 'Время', 0, 150)
        #self.spos.on_changed(self.update)

        self.sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setFocusPolicy (QtCore.Qt.NoFocus)
        self.sld.valueChanged[int].connect(self.update)
        self.sld.valueChanged.connect(self.redraw)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)
        self.layoutVertical.addWidget(self.sld)

    def clear(self):
        self.axis.clear()
        self.sld.setValue(0)

    def redraw(self):
        self.canvas.draw_idle()

    def update(self, val):
        a, b = val * (self.timelen // 100), (val + 1) * (self.timelen // 100)
        self.axis.set_xticklabels(self.ticks[a:b])
        self.axis.set_xlim(a, b)


class SETKAapp(Ui_MainWindow):

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()

        self.setupUi(self.MainWindow)
        self.temp_graph = MatplotlibWidget(self.MainWindow)
        self.press_graph = MatplotlibWidget(self.MainWindow)
        self.temp_scroll.setWidget(self.temp_graph)
        self.press_scroll.setWidget(self.press_graph)
        import random
        r_data = []
        cur_time = 0
        cur_temp = 0
        for i in range(900):
            r_data.append([str(cur_time).zfill(4)] + [cur_temp for _ in range(4)])
            cur_time += random.randint(1, 3)
            cur_temp += random.randint(5, 30) - 15
        self.plot_graphics(r_data)
        self.connect_slots()
        self.datetime = QtCore.QDateTime.currentDateTime()
        timer = QtCore.QTimer(self.app)
        timer.timeout.connect(self.update)
        timer.start(1000)

    def update(self):
        """Called every second"""

        error_string = 'Подключите PyBoard'
        self.datetime = self.datetime.addSecs(1)
        self.engines_table.item(0, 0).setText(''.join(pyboard.extruder_speed) if pyboard.connected else error_string)
        self.engines_table.item(1, 0).setText(''.join(pyboard.first_head_speed) if pyboard.connected else error_string)
        self.engines_table.item(2, 0).setText(''.join(pyboard.second_head_speed) if pyboard.connected else error_string)
        self.engines_table.item(3, 0).setText(''.join(pyboard.reciever_speed) if pyboard.connected else error_string)
        self.data_table.item(0, 0).setText(''.join(pyboard.t1) if pyboard.connected else error_string)
        self.data_table.item(1, 0).setText(''.join(pyboard.t2) if pyboard.connected else error_string)
        self.data_table.item(2, 0).setText(''.join(pyboard.p1) if pyboard.connected else error_string)
        self.data_table.item(3, 0).setText(''.join(pyboard.p2) if pyboard.connected else error_string)
        self.misc_table.item(0, 0).setText(''.join(pyboard.config)[:3] if pyboard.connected else error_string)
        self.misc_table.item(1, 0).setText(self.datetime.time().toString() )
        self.misc_table.item(2, 0).setText(self.datetime.date().toString())
        if pyboard.error_status:
            self.misc_table.item(3, 0).setText(error_map[pyboard.error_status - 2] if pyboard.connected else error_string)
        else:
            self.misc_table.item(3, 0).setText('' if pyboard.connected else error_string)

    def connect_slots(self):
        slots = [x.triggered for x in [self.connect_pyboard_button,
                                     self.build_graph_button,
                                     self.open_conf_editor_button,
                                     self.settings_button]]
        callbacks = [self.on_connect_button, self.on_build_graph,
                     self.on_open_editor, self.on_open_settings]
        for slot, callback in zip(slots, callbacks):
            slot.connect(callback)

    def on_connect_button(self):
            dlg = ConnectDialog()
            dlg.exec_()

    def on_build_graph(self):
        if not pyboard.connected:
            QtWidgets.QMessageBox.warning(self.MainWindow, "Ошибка",
                                "PyBoard не подключен, используйте Меню->Покдлючить PyBoard")
        else:
            dlg = GraphicsDialog()
            dlg.exec_()
        
    def on_open_editor(self):
        """if not pyboard.connected:
            QtWidgets.QMessageBox.warning(self.MainWindow, "Ошибка",
                                "PyBoard не подключен, используйте Меню->Покдлючить PyBoard")
        else:"""
        dlg = EditorDialog()
        dlg.exec_()

    def on_open_settings(self):
        dlg = SettingsDialog()
        if dlg.exec_() and dlg.result():
            self.datetime = dlg.new_datetime

    def run(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def plot_graphics(self, data):
        ticks = [':'.join(chunkstring(x[0], 2)) for x in data]
        print(data)
        print(ticks)
        int_time = list(range(len(data)))
        temp1 = [float(x[1]) for x in data] 
        temp2 = [float(x[2]) for x in data] 
        press1 = [float(x[3]) for x in data] 
        press2 = [float(x[4]) for x in data]
        temp_ticks_func = lambda x, pos: ticks[pos]
        press_ticks_func = lambda x, pos: ticks[pos]
        self.temp_graph.axis.xaxis.set_major_formatter(FuncFormatter(temp_ticks_func))
        self.press_graph.axis.xaxis.set_major_formatter(FuncFormatter(press_ticks_func))
        for graph in [self.temp_graph, self.press_graph]:
            graph.clear()
            graph.ticks = ticks
            graph.timelen = len(data)
        self.temp_graph.axis.plot(int_time, temp1, 'C1', label='T1')
        self.temp_graph.axis.plot(int_time, temp2, 'C3', label='T2')
        self.temp_graph.axis.legend()
        self.press_graph.axis.plot(int_time, press1, 'C4', label='P1')
        self.press_graph.axis.plot(int_time, press2, 'C2', label='P2')
        self.press_graph.axis.legend()
        self.temp_graph.canvas.draw()
        self.press_graph.canvas.draw()


class GraphicsDialog(QtWidgets.QDialog, Ui_GraphicsDialog):

    fetching_list = False
    downloading = False
    fetch_finished_signal = QtCore.pyqtSignal(int, name='fetch_finished_signal')
    load_finished_signal = QtCore.pyqtSignal(int, name='load_finished_signal')

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.open_butt.setEnabled(False)
        self.open_butt.clicked.connect(self.on_open)
        self.fetch_finished_signal.connect(self.on_finish_fetching)
        self.load_finished_signal.connect(self.on_file_downloaded)
        self.start_fetching()

    def start_fetching(self):
        self.update_status('Получаем список файлов...')
        self.fetching_list = True
        fetch_thread = threading.Thread(target=self.fetch)
        fetch_thread.daemon = True
        fetch_thread.start()

    def fetch(self):
        pyboard.recieve_logs_list()
        while pyboard.recieve_flag != -1:
            time.sleep(0.05)
        self.fetch_finished_signal.emit(1)

    def on_finish_fetching(self):
        self.update_status('Выберите файл')
        files_raw = ''.join([chr(x) for x in pyboard.recieved_file])
        if files_raw != 'no':
            files = ['.'.join(chunkstring(x, 2)) for x in chunkstring(files_raw, 10)]
            print(files)
            for filename in files:
                self.files_list.addItem(filename)
        self.open_butt.setEnabled(True)
        self.fetching_list = False

    def cancel_downloading(self):
        if self.fetching_list:
            self.fetching_list = False
        if self.downloading:
            self.downloading = False
        pyboard.cmd = 0

    def closeEvent(self, evnt):
        if self.fetching_list or self.downloading:
            self.cancel_downloading()
        super(GraphicsDialog, self).closeEvent(evnt)

    def update_status(self, status):
        self.status_label.setText(status)

    def on_open(self):
        selected = self.files_list.currentItem()
        if not selected:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите файл!")
            return
        filename = selected.text()
        print(filename)
        self.open_butt.setEnabled(False)
        save_thread = threading.Thread(target=self.download_file, args=(filename,))
        save_thread.daemon = True
        save_thread.start()

    def download_file(self, filename):
        pyboard.download_log(filename)
        while pyboard.recieve_flag != -1:
            time.sleep(0.05)
        self.load_finished_signal.emit(1)

    def on_file_downloaded(self):
        file_raw = ''.join([chr(x) for x in pyboard.recieved_file])
        self.open_butt.setEnabled(True)
        data = [[x[:4]] + list(chunkstring(x[4:], 5)) for x in file_raw.split('\n') if len(x) == 24]
        print("GRAFIC data", data)
        app.plot_graphics(data)

class EditorDialog(QtWidgets.QDialog, Ui_EditorDialog):

    load_finished_signal = QtCore.pyqtSignal(int, name='load_finished_signal')
    save_finished_signal = QtCore.pyqtSignal(int, name='save_finished_signal')
    exist_finished_signal = QtCore.pyqtSignal(int, name='exist_finished_signal')
    speeds = None

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.save_button.clicked.connect(self.on_save)
        self.open_button.clicked.connect(self.on_load)
        self.recipes_list.itemClicked.connect(self.on_list_click)
        self.save_button.setEnabled(False)
        self.open_button.setEnabled(False)
        self.download_existing()
        self.load_finished_signal.connect(self.on_load_finished, QtCore.Qt.QueuedConnection)
        self.save_finished_signal.connect(self.on_save_finished, QtCore.Qt.QueuedConnection)
        self.exist_finished_signal.connect(self.on_download_existing_finished, QtCore.Qt.QueuedConnection)

    def on_list_click(self, item):
        self.recipe_spin_box.setValue(int(item.text())) 

    def download_existing(self):
        exist_thread = threading.Thread(target=self.wait_for_existing)
        exist_thread.daemon = True 
        self.warn('Получаем список существующих рецептов...')
        exist_thread.start()

    def wait_for_existing(self):
        pyboard.download_existing()
        time.sleep(0.1)
        while pyboard.recieve_flag != -1:
            time.sleep(0.05)
        self.exist_finished_signal.emit(1)
        print("DOWNLOAD FINISHED")

    def on_download_existing_finished(self, status):
        print("BEGIN PARSING")
        print(pyboard.recieved_file)
        files_raw = ''.join([chr(x) for x in pyboard.recieved_file])
        print("EDITOR data", files_raw)
        if files_raw != 'no':
            files = chunkstring(files_raw, 3)
            self.recipes_list.clear()
            for filename in files:
                self.recipes_list.addItem(filename)
        self.open_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.warn('Список существующих рецептов получен!')

    def warn(self, text):
        self.warning_label.setText(text)

    def choosen_file(self):
        return str(self.recipe_spin_box.value()).zfill(3)

    def fill_speeds(self, speeds):
        self.e1_edit.setText(speeds[0])
        self.e2_edit.setText(speeds[1])
        self.e3_edit.setText(speeds[2])
        self.e4_edit.setText(speeds[3])

    def on_save_finished(self, status):
        self.open_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.warn('Конфиг сохранен!')
        self.download_existing()

    def wait_for_save(self):
        while pyboard.cmd:
            time.sleep(0.1)
        self.save_finished_signal.emit(1)

    def on_save(self):
        try:
            speeds = [to_float(x.text()) for x in [self.e1_edit, 
                                                   self.e2_edit,
                                                   self.e3_edit,
                                                   self.e4_edit]]
            print('Speeds are', speeds)
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректный формат!")
        else:
            self.open_button.setEnabled(False)
            self.save_button.setEnabled(False)
            self.warn('Загружаем в PyBoard')
            pyboard.config_value = [x for i in speeds for x in i]
            print('Config value is ', pyboard.config_value)
            pyboard.arg = int(self.choosen_file())
            pyboard.cmd = 4
            save_thread = threading.Thread(target=self.wait_for_save)
            save_thread.daemon = True
            save_thread.start()

    def on_load_finished(self, status):
        self.open_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.fill_speeds(self.speeds)
        self.warn('Конфиг получен!')

    def wait_for_load(self):
        while pyboard.cmd:
            time.sleep(0.1)
        self.speeds = [''.join(pyboard.config_value[i*5:(i+1)*5]) for i in range(4)]
        print(self.speeds)
        self.load_finished_signal.emit(1)

    def on_load(self):
        self.open_button.setEnabled(False)
        self.save_button.setEnabled(False)
        pyboard.arg = int(self.choosen_file())
        print('ARG IS ', pyboard.arg)
        pyboard.cmd = 3
        self.warn('Получаем конфиг с PyBoard')
        load_thread = threading.Thread(target=self.wait_for_load)
        load_thread.daemon = True
        load_thread.start()


class ConnectDialog(QtWidgets.QDialog, Ui_ConnectDialog):

    connect_finished_signal = QtCore.pyqtSignal(int, name='connect_finished_signal')

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.connect_butt.clicked.connect(self.on_connect)
        self.port_edit.setText('/dev/ttyUSB0')
        self.connect_finished_signal.connect(self.on_connected)

    def log(self, text):
        self.status_label.setText(text)

    def on_connect(self):
        self.connect_butt.setEnabled(False)
        port = self.port_edit.text()
        if not port: self.log('Invalid port')
        else:
            self.log('Trying to connect...')
            thread = threading.Thread(target=pyboard.connect,
                                      args=(port, self.on_connected))
            thread.daemon = True
            thread.start()

    def on_connect_finished(self, res):
        self.connect_finished_signal.emit(res)

    def on_connected(self, res):
        self.connect_butt.setEnabled(True)
        if res == 1:
            self.log('PyBoard connected!')
        if not res:
            self.log('Connecting error')
            

class SettingsDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.new_datetime = self.date_time_edit.dateTime()
        self.date_time_edit.dateTimeChanged.connect(self.on_datetime_change)

    def on_datetime_change(self, new_datetime):
        print(new_datetime)
        self.new_datetime = new_datetime

if __name__ == "__main__":
    thread = threading.Thread(target=pyboard.run)
    thread.daemon = True
    thread.start()
    app = SETKAapp()
    app.run()
