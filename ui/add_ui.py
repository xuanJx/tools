# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(336, 451)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(101, 14, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.ser_num_line = QtWidgets.QLineEdit(Form)
        self.ser_num_line.setGeometry(QtCore.QRect(90, 80, 113, 20))
        self.ser_num_line.setObjectName("ser_num_line")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(106, 49, 81, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(47, 111, 221, 21))
        self.label_2.setObjectName("label_2")
        self.mask_line = QtWidgets.QLineEdit(Form)
        self.mask_line.setGeometry(QtCore.QRect(90, 140, 113, 20))
        self.mask_line.setObjectName("mask_line")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(100, 169, 101, 21))
        self.label_3.setObjectName("label_3")
        self.how_many_line = QtWidgets.QLineEdit(Form)
        self.how_many_line.setGeometry(QtCore.QRect(90, 195, 113, 20))
        self.how_many_line.setObjectName("how_many_line")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(24, 224, 281, 221))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.label.setText(_translate("Form", "??????????????????"))
        self.label_2.setText(_translate("Form", "??????????????????(???29???255.255.255.248)"))
        self.label_3.setText(_translate("Form", "?????????????????????"))
