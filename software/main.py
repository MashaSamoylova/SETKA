import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from mainwindow import Ui_MainWindow


class SETKAapp:

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.connect_slots()

    def connect_slots(self):
        slots = [x.triggered for x in [self.ui.connect_pyboard_button,
                                     self.ui.build_graph_button,
                                     self.ui.open_conf_editor_button,
                                     self.ui.settings_button]]
        callbacks = [self.on_connect_button, self.on_build_graph,
                     self.on_open_editor, self.on_open_settings]
        for slot, callback in zip(slots, callbacks):
            slot.connect(callback)

    def on_connect_button(self):
        print('connect')

    def on_build_graph(self):
        print('graph')

    def on_open_editor(self):
        print('open editor')

    def on_open_settings(self):
        print('open settings')

    def run(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = SETKAapp()
    app.run()
