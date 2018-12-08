import sys
import os
import platform
import threading
import re
import subprocess


from mainwindow import Ui_MainWindow
from loginwindow import Ui_LoginWindow
from vk_api8 import VKApi
from GroupMethods import GroupMethods
from UserMethods import UserMethods

class VKInf():
    class VKInfLogin(QtWidgets.QMainWindow):
        log_in_finish_signal = QtCore.pyqtSignal(int, name='log_in_finish_signal')
        def __init__(self, client, version, on_finish):
            super().__init__()
            self.log_in_successful = False
            self.login = ''
            self.password = ''
            self.token = ''
            self.client = client
            self.version = version
            self.on_finish = on_finish

            self.ui.login_butt.clicked.connect(self.on_log_in_butt)
            self.ui.login_edit.returnPressed.connect(self.on_log_in_butt)
            self.ui.pass_edit.returnPressed.connect(self.on_log_in_butt)
            self.log_in_finish_signal.connect(self.log_in_finish_signal_handler, QtCore.Qt.QueuedConnection)
    
        def on_log_in_butt(self):
            self.ui.login_butt.setEnabled(False)
            self.login = self.ui.login_edit.text().replace(' ', '')
            self.password = self.ui.pass_edit.text()
            self.ui.status_label.setText("Trying to log in, please wait...")
            thread = threading.Thread(target=self.log_in, args=(self.on_log_in_finished,))
            thread.daemon = True
            thread.start()

        def log_in_finish_signal_handler(self, status):
            if(not status):
                self.log_in_successful = True
                self.ui.status_label.setText("Success!")
                self.on_finish()
            elif(status == 2):
                 self.ui.status_label.setText("Your accocunt is not in our database,\n please contact us to insert your account.")
            else:
                self.ui.status_label.setText("Error while authorizing\nWrong login or password or internet issues")            
            self.ui.login_butt.setEnabled(True)

        def on_log_in_finished(self, status):
            self.log_in_finish_signal.emit(status)

    class VKInfMain(QtWidgets.QMainWindow):
        log_signal = QtCore.pyqtSignal(str, name='log_signal')
        method_finish_signal = QtCore.pyqtSignal(str, int, name='method_finish_signal')
        progress_signal = QtCore.pyqtSignal(float, name='progress_signal')

        def __init__(self, on_go, on_cancel):
            super().__init__()
            self.cur_tab = 0
            self.cur_method = 0
            self.files_dir = ''            
            self.on_go = on_go
            self.on_cancel = on_cancel

            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.setWindowIcon(QtGui.QIcon('icon.gif'))
            self.move(QtWidgets.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
            
            self.input_data = self.ui.input_edit.toPlainText();
            self.on_go = on_go
            self.ui.help_button.clicked.connect(self.show_help)
            self.ui.groups_box.currentIndexChanged.connect(self.on_combo_box_changed)
            self.ui.users_box.currentIndexChanged.connect(self.on_combo_box_changed)
            self.ui.tabWidget.currentChanged.connect(self.on_tab_changed)
            self.ui.input_edit.textChanged.connect(self.on_input_data_changed)
            self.ui.open_button.clicked.connect(self.open_files_folder)
            self.ui.go_button.clicked.connect(self.on_go_button)
            self.method_finish_signal.connect(self.method_finifsh_signal_handler, QtCore.Qt.QueuedConnection)
            self.progress_signal.connect(self.progress_signal_handler, QtCore.Qt.QueuedConnection)
            self.log_signal.connect(self.log_signal_handler, QtCore.Qt.QueuedConnection)

        def on_go_button(self):
            if(self.ui.input_edit.toPlainText() == ''):
                print('Пожалуйста, заполните поле входных данных')
            else:
                self.disable_go_button()
                self.ui.open_button.setEnabled(False)
                self.update_progress_bar(0)
                self.on_go()

        def on_files_ready(self, dir_path, status=0):
            self.method_finish_signal.emit(dir_path, status)

        def open_files_folder(self):
            try:
                if platform.system() == "Windows":
                    os.startfile(self.files_dir)
                elif platform.system() == "Darwin":
                    subprocess.Popen(["open", self.files_dir])
                else:
                    subprocess.Popen(["xdg-open", self.files_dir])
            except:
                print('Ошибка при открытии директории с файлами, пожалуйста откройте ее самостоятельно: ' + self.files_dir)

        def on_input_data_changed(self):
            self.input_data = self.ui.input_edit.toPlainText()

        def on_combo_box_changed(self, index):
            self.cur_method = index

        def on_tab_changed(self, index):
            self.cur_tab = index
            self.cur_method = self.ui.tabWidget.currentWidget().findChild(QtWidgets.QComboBox).currentIndex()
            if(index == 1):
                self.ui.input_edit.setPlaceholderText(self.user_methods.methods[self.cur_method]['format'])
            elif(index == 0):
                self.ui.input_edit.setPlaceholderText(self.group_methods.methods[self.cur_method]['format'])
    
        def show_help(self):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            if(self.cur_tab == 1):
                msgBox.setWindowTitle(self.ui.users_box.itemText(self.cur_method))
                msgBox.setText(self.user_methods.methods[self.cur_method]['info'])
            elif(self.cur_tab == 0):
                msgBox.setWindowTitle(self.ui.groups_box.itemText(self.cur_method))
                msgBox.setText(self.group_methods.methods[self.cur_method]['info'])
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()

        def write(self, text):
            self.log_signal.emit(text)

        def log_signal_handler(self, text):
            self.ui.log_edit.insertPlainText(text)
            self.ui.log_edit.moveCursor(QtGui.QTextCursor.End)

        def progress_signal_handler(self, value):
            self.ui.progressBar.setValue(value)

        def method_finifsh_signal_handler(self, dir_path, status):
            if(not status):
                self.files_dir = dir_path
                print('Method finished, you can get results at: \n' + self.files_dir + '\nOr you can press "Open" button')
                self.ui.open_button.setEnabled(True)
            self.enable_go_button()
    
    def __init__(self):
        self.client = '5455153'
        self.version = '5.69'
        
    def _start_method(self):
        self.main_window.disable_go_button()
        group, method = self.main_window.cur_tab, self.main_window.cur_method
        if(group == 1):
            func = self.user_methods.methods[method]['method']
        elif(group == 0):
            func = self.group_methods.methods[method]['method']
        args = (self.main_window.input_data,)
        self.thread = threading.Thread(target=self.execute_in_back_thread, args=(func, *args))
        self.thread.daemon = True
        self.thread.start()

    def execute_in_back_thread(self, func, *args):
        try:
            func(*args)
        except Exception as e:
            print(e)
            self.main_window.on_files_ready('', 1)

    def cancel_thread(self):
        print('Sorry that feature doesn\'t work. -_0_0_-')

    def _on_method_finished(self, status, filenames='', error_message=''):
        if(not status):
            self.main_window.on_files_ready(filenames)
        else:
            self.main_window.on_files_ready(filenames, 1)
            print(error_message)

    def _on_login_finished(self):
        self.login_window.close()
        self.vkApi8 = self.login_window.vkApi8

    def run(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.login_window = self.VKInfLogin(self.client, self.version, self._on_login_finished)
        self.login_window.show()
        self.app.exec_()

        del self.login_window
        del self.app

        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = self.VKInfMain(self._start_method, self.cancel_thread)
        self.group_methods = GroupMethods(self.vkApi8, self.main_window.update_progress_bar, self.main_window.on_files_ready)
        self.user_methods = UserMethods(self.vkApi8, self.main_window.update_progress_bar, self.main_window.on_files_ready)
        self.main_window.set_methods(self.group_methods, self.user_methods)
        sys.stdout = self.main_window
        sys.stderr = self.main_window
        self.main_window.show()
        self.app.exec_()
    
app = VKInf()
app.run()

