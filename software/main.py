import sys
import pathlib
import os
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure 
from mainwindow import Ui_MainWindow
from settings import Ui_Dialog
from editordialog import Ui_EditorDialog
from connectdialog import Ui_Dialog as Ui_ConnectDialog
from pyboard import PyBoard

from utils import to_float

pyboard = PyBoard()

class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)


class SETKAapp(Ui_MainWindow):

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()

        self.setupUi(self.MainWindow)
        self.temp_graph = MatplotlibWidget(self.MainWindow)
        self.press_graph = MatplotlibWidget(self.MainWindow)
        self.graphs_layout.addWidget(self.temp_graph)
        self.graphs_layout.addWidget(self.press_graph)
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
        graph_file = QtWidgets.QFileDialog.getOpenFileName(directory=self.board_dir,
                                                           filter="(*.data)")[0]
        if not graph_file: return
        try:
            with open(graph_file) as f:
                data = [x.strip().split(';') for x in f.readlines()]

            temp1 = [int(x[0]) for x in data] 
            temp2 = [int(x[1]) for x in data] 
            press1 = [int(x[2]) for x in data] 
            press2 = [int(x[3]) for x in data]
        except:
            QtWidgets.QMessageBox.warning(self.MainWindow, "Ошибка", "Некорректный формат файла!")
        else:
            self.temp_graph.axis.plot(temp1, 'C1', label='T1')
            self.temp_graph.axis.plot(temp2, 'C3', label='T2')
            self.temp_graph.axis.legend()
            self.press_graph.axis.plot(press1, 'C4', label='P1')
            self.press_graph.axis.plot(press2, 'C2', label='P2')
            self.press_graph.axis.legend()
            self.temp_graph.canvas.draw()
            self.press_graph.canvas.draw()
        
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
            speeds = list(map(lambda x: to_float(x.text()), [self.e1_edit, 
                                                            self.e2_edit,
                                                            self.e3_edit,
                                                            self.e4_edit]))
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
