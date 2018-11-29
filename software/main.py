import sys
import pathlib
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from mainwindow import Ui_MainWindow
from settings import Ui_Dialog
from editordialog import Ui_EditorDialog


class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)


class SETKAapp(Ui_MainWindow):

    board_dir = '/home/roman/setka_test'
    board_connected = True

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
        directory = QtWidgets.QFileDialog.getExistingDirectory()
        self.board_dir = directory
        self.board_connected = True


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
        if not self.board_connected:
            QtWidgets.QMessageBox.warning(self.MainWindow, "Ошибка",
                                "PyBoard не подключен, используйте Меню->Покдлючить PyBoard")
        else:
            dlg = EditorDialog(self.board_dir)
            dlg.exec_()

    def on_open_settings(self):
        dlg = SettingsDialog()
        if dlg.exec_() and dlg.result():
            self.datetime = dlg.new_datetime

    def run(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())


class EditorDialog(QtWidgets.QDialog, Ui_EditorDialog):

    def __init__(self, directory, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.directory = os.path.join(directory, 'recipes')
        pathlib.Path(self.directory).mkdir(parents=True, exist_ok=True)
        self.setupUi(self)
        self.save_button.clicked.connect(self.on_save)
        self.open_button.clicked.connect(self.on_load)

    def warn(self, text):
        self.warning_label.setText(text)

    def choosen_file(self):
        filename = str(self.recipe_spin_box.value()).zfill(2) + ".txt"
        return os.path.join(self.directory, filename)

    def fill_speeds(self, speeds):
        self.e1_edit.setText(str(speeds[0]))
        self.e2_edit.setText(str(speeds[1]))
        self.e3_edit.setText(str(speeds[2]))
        self.e4_edit.setText(str(speeds[3]))

    def on_save(self):
        try:
            speeds = [float(self.e1_edit.text()), float(self.e2_edit.text()),
                      float(self.e3_edit.text()), float(self.e4_edit.text())]
            with open(self.choosen_file(), 'w') as f:
                f.write(';'.join([str(x) for x in speeds]))
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректный формат!")
        else:
            self.warn('Сохранено!')

    def on_load(self):
        speeds = []
        recipe_file = self.choosen_file()
        try:
            with open(recipe_file) as f:
                speeds = [float(x.strip()) for x in f.read().split(';')]
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Рецепт {recipe_file} не существует!")
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректный формат файла!")
        else:
            self.fill_speeds(speeds)


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
    app = SETKAapp()
    app.run()
