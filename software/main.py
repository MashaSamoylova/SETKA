import sys
import pathlib
import os
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure 

from windows.mainwindow import Ui_MainWindow
from windows.settings import Ui_Dialog
from windows.editordialog import Ui_EditorDialog
from windows.connectdialog import Ui_Dialog as Ui_ConnectDialog
from windows.graphicsdialog import Ui_GraphicsDialog
from pyboard import PyBoard
from utils import to_float, chunkstring

pyboard = PyBoard()

class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setMinimumSize(QtCore.QSize(1500, 0))

        self.axis = self.figure.add_subplot(111)
        self.axis.set_xlim(0, 900)
        self.axis.set_ylim(0, 200)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)


class SETKAapp(Ui_MainWindow):

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()

        self.setupUi(self.MainWindow)
        self.temp_graph = MatplotlibWidget(self.MainWindow)
        self.press_graph = MatplotlibWidget(self.MainWindow)
        self.temp_scroll.setWidget(self.temp_graph)
        self.press_scroll.setWidget(self.press_graph)
        #import random
        #self.plot_graphics([[random.randint(0, 100) for _ in range(4)] for i in range(900)])
        self.connect_slots()
        self.datetime = QtCore.QDateTime.currentDateTime()
        timer = QtCore.QTimer(self.app)
        timer.timeout.connect(self.update)
        timer.start(1000)

    def update(self):
        """Called every second"""

        self.datetime = self.datetime.addSecs(1)
        self.main_table.item(13, 0).setText(self.datetime.time().toString())
        self.main_table.item(14, 0).setText(self.datetime.date().toString())
        self.main_table.item(1, 0).setText(''.join(pyboard.extruder_speed))
        self.main_table.item(2, 0).setText(''.join(pyboard.first_head_speed))
        self.main_table.item(3, 0).setText(''.join(pyboard.second_head_speed))
        self.main_table.item(4, 0).setText(''.join(pyboard.reciever_speed))
        self.main_table.item(6, 0).setText(''.join(pyboard.t1))
        self.main_table.item(7, 0).setText(''.join(pyboard.t2))
        self.main_table.item(8, 0).setText(''.join(pyboard.p1))
        self.main_table.item(9, 0).setText(''.join(pyboard.p2))
        self.main_table.item(12, 0).setText(''.join(pyboard.config))

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
        if not pyboard.connected:
            QtWidgets.QMessageBox.warning(self.MainWindow, "Ошибка",
                                "PyBoard не подключен, используйте Меню->Покдлючить PyBoard")
        else:
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
        temp1 = [float(x[0]) for x in data] 
        temp2 = [float(x[1]) for x in data] 
        press1 = [float(x[2]) for x in data] 
        press2 = [float(x[3]) for x in data]
        self.temp_graph.axis.clear()
        self.press_graph.axis.clear()
        self.temp_graph.axis.plot(list(range(len(temp1))), temp1, 'C1', label='T1')
        self.temp_graph.axis.plot(list(range(len(temp2))), temp2, 'C3', label='T2')
        self.temp_graph.axis.legend()
        self.press_graph.axis.plot(list(range(len(press1))), press1, 'C4', label='P1')
        self.press_graph.axis.plot(list(range(len(press2))), press2, 'C2', label='P2')
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
        data = [list(chunkstring(x, 5)) for x in file_raw.split('\n') if len(x) == 20]
        print(data)
        app.plot_graphics(data)

class EditorDialog(QtWidgets.QDialog, Ui_EditorDialog):

    load_finished_signal = QtCore.pyqtSignal(int, name='load_finished_signal')
    save_finished_signal = QtCore.pyqtSignal(int, name='save_finished_signal')
    speeds = None

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.save_button.clicked.connect(self.on_save)
        self.open_button.clicked.connect(self.on_load)
        self.load_finished_signal.connect(self.on_load_finished, QtCore.Qt.QueuedConnection)
        self.save_finished_signal.connect(self.on_save_finished, QtCore.Qt.QueuedConnection)

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
