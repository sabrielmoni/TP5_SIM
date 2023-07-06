from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import math


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Runge Kutta")
        self.resize(1440, 900)
        self.layout = QVBoxLayout()
        self.setModal = True
        
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setLayout(self.layout)
        self.layout.addWidget(self.buttonBox)

        self.tableWidgetRK = QtWidgets.QTableWidget(self)
        self.tableWidgetRK.setGeometry(QtCore.QRect(270, 20, 911, 801))
        self.tableWidgetRK.setObjectName("tableWidgetRK")
        self.tableWidgetRK.setColumnCount(9)
        self.tableWidgetRK.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetRK.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetRK.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetRK.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetRK.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetRK.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetRK.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetRK.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetRK.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetRK.setHorizontalHeaderItem(8, item)
        item = self.tableWidgetRK.horizontalHeaderItem(0)

        self.retranslateUi(CustomDialog)
        
    
    def retranslateUi(self, CustomDialog):
        _translate = QtCore.QCoreApplication.translate
        item = self.tableWidgetRK.horizontalHeaderItem(0)
        item.setText(_translate("CustomDialog", "Descripción"))
        item = self.tableWidgetRK.horizontalHeaderItem(1)
        item.setText(_translate("CustomDialog", "x"))
        item = self.tableWidgetRK.horizontalHeaderItem(2)
        item.setText(_translate("CustomDialog", "y"))
        item = self.tableWidgetRK.horizontalHeaderItem(3)
        item.setText(_translate("CustomDialog", "k1"))
        item = self.tableWidgetRK.horizontalHeaderItem(4)
        item.setText(_translate("CustomDialog", "k2"))
        item = self.tableWidgetRK.horizontalHeaderItem(5)
        item.setText(_translate("CustomDialog", "k3"))
        item = self.tableWidgetRK.horizontalHeaderItem(6)
        item.setText(_translate("CustomDialog", "k4"))
        item = self.tableWidgetRK.horizontalHeaderItem(7)
        item.setText(_translate("CustomDialog", "x(i+1)"))
        item = self.tableWidgetRK.horizontalHeaderItem(8)
        item.setText(_translate("CustomDialog", "y(i+1)"))
        
        
        

    
        