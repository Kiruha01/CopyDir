# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v0.2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(586, 554)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.setFont(font)
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setGeometry(QtCore.QRect(10, 20, 561, 421))
        self.treeWidget.setObjectName("treeWidget")
        self.okbut = QtWidgets.QPushButton(Form)
        self.okbut.setGeometry(QtCore.QRect(440, 490, 93, 28))
        self.okbut.setObjectName("okbut")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget.setSortingEnabled(True)
        self.okbut.setText(_translate("Form", "ok"))
