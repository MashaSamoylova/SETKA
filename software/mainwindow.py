# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(758, 651)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_table = QtWidgets.QTableWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_table.sizePolicy().hasHeightForWidth())
        self.main_table.setSizePolicy(sizePolicy)
        self.main_table.setMinimumSize(QtCore.QSize(367, 0))
        self.main_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.main_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.main_table.setCornerButtonEnabled(False)
        self.main_table.setObjectName("main_table")
        self.main_table.setColumnCount(2)
        self.main_table.setRowCount(15)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(0, 0, 0))
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.main_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.main_table.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.main_table.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Е. И")
        self.main_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(7, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(8, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(9, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(10, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(10, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(11, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(11, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(12, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(12, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(13, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(13, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(14, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.main_table.setItem(14, 1, item)
        self.verticalLayout_2.addWidget(self.main_table)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.temp_graph = QtWidgets.QGraphicsView(self.centralWidget)
        self.temp_graph.setObjectName("temp_graph")
        self.verticalLayout.addWidget(self.temp_graph)
        self.pressuare_graph = QtWidgets.QGraphicsView(self.centralWidget)
        self.pressuare_graph.setObjectName("pressuare_graph")
        self.verticalLayout.addWidget(self.pressuare_graph)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 758, 25))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.connect_pyboard_button = QtWidgets.QAction(MainWindow)
        self.connect_pyboard_button.setObjectName("connect_pyboard_button")
        self.build_graph_button = QtWidgets.QAction(MainWindow)
        self.build_graph_button.setObjectName("build_graph_button")
        self.open_conf_editor_button = QtWidgets.QAction(MainWindow)
        self.open_conf_editor_button.setObjectName("open_conf_editor_button")
        self.settings_button = QtWidgets.QAction(MainWindow)
        self.settings_button.setObjectName("settings_button")
        self.menuFile.addAction(self.connect_pyboard_button)
        self.menuFile.addAction(self.build_graph_button)
        self.menuFile.addAction(self.open_conf_editor_button)
        self.menuFile.addAction(self.settings_button)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.main_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1."))
        item = self.main_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Экструдер"))
        item = self.main_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Фильера 1"))
        item = self.main_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Фильера 2"))
        item = self.main_table.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Приемка сетки"))
        item = self.main_table.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "2."))
        item = self.main_table.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "Температура 1"))
        item = self.main_table.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "Температура 2"))
        item = self.main_table.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "Давление 1"))
        item = self.main_table.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "Давление 2"))
        item = self.main_table.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "3."))
        item = self.main_table.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "Толщина рукава"))
        item = self.main_table.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "Имя файла с рецептами"))
        item = self.main_table.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "Время"))
        item = self.main_table.verticalHeaderItem(14)
        item.setText(_translate("MainWindow", "Дата"))
        item = self.main_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Кол-во"))
        __sortingEnabled = self.main_table.isSortingEnabled()
        self.main_table.setSortingEnabled(False)
        item = self.main_table.item(0, 0)
        item.setText(_translate("MainWindow", "Моторы"))
        item = self.main_table.item(1, 1)
        item.setText(_translate("MainWindow", "Об./м"))
        item = self.main_table.item(2, 1)
        item.setText(_translate("MainWindow", "Об./м"))
        item = self.main_table.item(3, 1)
        item.setText(_translate("MainWindow", "Об./м"))
        item = self.main_table.item(4, 1)
        item.setText(_translate("MainWindow", "Об./м"))
        item = self.main_table.item(5, 0)
        item.setText(_translate("MainWindow", "Температура и давление расплава"))
        item = self.main_table.item(6, 1)
        item.setText(_translate("MainWindow", "°C"))
        item = self.main_table.item(7, 1)
        item.setText(_translate("MainWindow", "°C"))
        item = self.main_table.item(8, 1)
        item.setText(_translate("MainWindow", "атм"))
        item = self.main_table.item(9, 1)
        item.setText(_translate("MainWindow", "атм"))
        item = self.main_table.item(11, 1)
        item.setText(_translate("MainWindow", "мкм"))
        self.main_table.setSortingEnabled(__sortingEnabled)
        self.menuFile.setTitle(_translate("MainWindow", "Меню"))
        self.connect_pyboard_button.setText(_translate("MainWindow", "Подключить Pyboard"))
        self.build_graph_button.setText(_translate("MainWindow", "Просмотреть графики"))
        self.open_conf_editor_button.setText(_translate("MainWindow", "Редактор рецептов"))
        self.settings_button.setText(_translate("MainWindow", "Настройки"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

