# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(870, 651)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.engines_table = QtWidgets.QTableWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.engines_table.sizePolicy().hasHeightForWidth())
        self.engines_table.setSizePolicy(sizePolicy)
        self.engines_table.setMinimumSize(QtCore.QSize(360, 115))
        self.engines_table.setMaximumSize(QtCore.QSize(16777215, 115))
        self.engines_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.engines_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.engines_table.setWordWrap(False)
        self.engines_table.setCornerButtonEnabled(False)
        self.engines_table.setObjectName("engines_table")
        self.engines_table.setColumnCount(2)
        self.engines_table.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.engines_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.engines_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.engines_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.engines_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.engines_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Е. И")
        self.engines_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.engines_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.engines_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.engines_table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.engines_table.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.engines_table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.engines_table.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.engines_table.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.engines_table.setItem(3, 1, item)
        self.engines_table.horizontalHeader().setVisible(False)
        self.engines_table.horizontalHeader().setDefaultSectionSize(120)
        self.engines_table.horizontalHeader().setMinimumSectionSize(46)
        self.engines_table.horizontalHeader().setStretchLastSection(False)
        self.engines_table.verticalHeader().setVisible(True)
        self.engines_table.verticalHeader().setCascadingSectionResizes(False)
        self.engines_table.verticalHeader().setDefaultSectionSize(27)
        self.engines_table.verticalHeader().setHighlightSections(True)
        self.engines_table.verticalHeader().setMinimumSectionSize(25)
        self.engines_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.engines_table)
        self.label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.data_table = QtWidgets.QTableWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_table.sizePolicy().hasHeightForWidth())
        self.data_table.setSizePolicy(sizePolicy)
        self.data_table.setMinimumSize(QtCore.QSize(360, 115))
        self.data_table.setMaximumSize(QtCore.QSize(16777215, 115))
        self.data_table.setObjectName("data_table")
        self.data_table.setColumnCount(2)
        self.data_table.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.data_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.data_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.data_table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.data_table.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.data_table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.data_table.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.data_table.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.data_table.setItem(3, 1, item)
        self.data_table.horizontalHeader().setVisible(False)
        self.data_table.horizontalHeader().setDefaultSectionSize(120)
        self.data_table.horizontalHeader().setHighlightSections(True)
        self.data_table.horizontalHeader().setMinimumSectionSize(46)
        self.data_table.horizontalHeader().setSortIndicatorShown(False)
        self.data_table.verticalHeader().setDefaultSectionSize(27)
        self.verticalLayout_2.addWidget(self.data_table)
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.misc_table = QtWidgets.QTableWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.misc_table.sizePolicy().hasHeightForWidth())
        self.misc_table.setSizePolicy(sizePolicy)
        self.misc_table.setMinimumSize(QtCore.QSize(360, 100))
        self.misc_table.setMaximumSize(QtCore.QSize(16777215, 115))
        self.misc_table.setObjectName("misc_table")
        self.misc_table.setColumnCount(1)
        self.misc_table.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.misc_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.misc_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.misc_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.misc_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.misc_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.misc_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.misc_table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.misc_table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.misc_table.setItem(3, 0, item)
        self.misc_table.horizontalHeader().setVisible(False)
        self.misc_table.horizontalHeader().setDefaultSectionSize(235)
        self.misc_table.horizontalHeader().setMinimumSectionSize(46)
        self.misc_table.verticalHeader().setDefaultSectionSize(27)
        self.verticalLayout_2.addWidget(self.misc_table)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.temp_scroll = QtWidgets.QScrollArea(self.centralWidget)
        self.temp_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.temp_scroll.setWidgetResizable(True)
        self.temp_scroll.setObjectName("temp_scroll")
        self.temp_area = QtWidgets.QWidget()
        self.temp_area.setGeometry(QtCore.QRect(0, 0, 477, 281))
        self.temp_area.setObjectName("temp_area")
        self.temp_scroll.setWidget(self.temp_area)
        self.verticalLayout.addWidget(self.temp_scroll)
        self.press_scroll = QtWidgets.QScrollArea(self.centralWidget)
        self.press_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.press_scroll.setWidgetResizable(True)
        self.press_scroll.setObjectName("press_scroll")
        self.press_area = QtWidgets.QWidget()
        self.press_area.setGeometry(QtCore.QRect(0, 0, 477, 280))
        self.press_area.setObjectName("press_area")
        self.press_scroll.setWidget(self.press_area)
        self.verticalLayout.addWidget(self.press_scroll)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 870, 25))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "SETKA"))
        self.label_2.setText(_translate("MainWindow", "1. Моторы"))
        item = self.engines_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Экструдер"))
        item = self.engines_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Фильера 1"))
        item = self.engines_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Фильера 2"))
        item = self.engines_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Приемка сетки"))
        item = self.engines_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Моторы"))
        __sortingEnabled = self.engines_table.isSortingEnabled()
        self.engines_table.setSortingEnabled(False)
        item = self.engines_table.item(0, 1)
        item.setText(_translate("MainWindow", "Об./м"))
        item = self.engines_table.item(1, 1)
        item.setText(_translate("MainWindow", "Об./м"))
        item = self.engines_table.item(2, 1)
        item.setText(_translate("MainWindow", "Об./м"))
        item = self.engines_table.item(3, 1)
        item.setText(_translate("MainWindow", "Об./м"))
        self.engines_table.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("MainWindow", "2. Температура и давление"))
        item = self.data_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Температура 1"))
        item = self.data_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Температура 2"))
        item = self.data_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Давление 1"))
        item = self.data_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Давление 2"))
        item = self.data_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "  Температура и давление  "))
        item = self.data_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "  Единицы измерения"))
        __sortingEnabled = self.data_table.isSortingEnabled()
        self.data_table.setSortingEnabled(False)
        item = self.data_table.item(0, 1)
        item.setText(_translate("MainWindow", "°C"))
        item = self.data_table.item(1, 1)
        item.setText(_translate("MainWindow", "°C"))
        item = self.data_table.item(2, 1)
        item.setText(_translate("MainWindow", "Атм"))
        item = self.data_table.item(3, 1)
        item.setText(_translate("MainWindow", "Атм"))
        self.data_table.setSortingEnabled(__sortingEnabled)
        self.label_3.setText(_translate("MainWindow", "3. Состояние"))
        item = self.misc_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Номер рецепта"))
        item = self.misc_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Дата"))
        item = self.misc_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Время"))
        item = self.misc_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Ошибка"))
        __sortingEnabled = self.misc_table.isSortingEnabled()
        self.misc_table.setSortingEnabled(False)
        self.misc_table.setSortingEnabled(__sortingEnabled)
        self.menuFile.setTitle(_translate("MainWindow", "Меню"))
        self.connect_pyboard_button.setText(_translate("MainWindow", "Подключить &Pyboard"))
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

