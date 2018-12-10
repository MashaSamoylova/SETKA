# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graphicsdialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GraphicsDialog(object):
    def setupUi(self, GraphicsDialog):
        GraphicsDialog.setObjectName("GraphicsDialog")
        GraphicsDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(GraphicsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.files_list = QtWidgets.QListWidget(GraphicsDialog)
        self.files_list.setObjectName("files_list")
        self.verticalLayout.addWidget(self.files_list)
        self.status_label = QtWidgets.QLabel(GraphicsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy)
        self.status_label.setText("")
        self.status_label.setObjectName("status_label")
        self.verticalLayout.addWidget(self.status_label)
        self.open_butt = QtWidgets.QPushButton(GraphicsDialog)
        self.open_butt.setObjectName("open_butt")
        self.verticalLayout.addWidget(self.open_butt)
        self.buttonBox = QtWidgets.QDialogButtonBox(GraphicsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GraphicsDialog)
        self.buttonBox.accepted.connect(GraphicsDialog.accept)
        self.buttonBox.rejected.connect(GraphicsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GraphicsDialog)

    def retranslateUi(self, GraphicsDialog):
        _translate = QtCore.QCoreApplication.translate
        GraphicsDialog.setWindowTitle(_translate("GraphicsDialog", "Выберите график"))
        self.open_butt.setText(_translate("GraphicsDialog", "Открыть"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GraphicsDialog = QtWidgets.QDialog()
    ui = Ui_GraphicsDialog()
    ui.setupUi(GraphicsDialog)
    GraphicsDialog.show()
    sys.exit(app.exec_())

