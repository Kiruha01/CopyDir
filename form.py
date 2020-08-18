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
        Form.resize(746, 687)
        Form.setMaximumSize(QtCore.QSize(746, 687))
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.setFont(font)
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        self.stackedWidget.setGeometry(QtCore.QRect(11, 11, 731, 671))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.Sourcepath = QtWidgets.QLineEdit(self.page)
        self.Sourcepath.setGeometry(QtCore.QRect(100, 180, 351, 21))
        self.Sourcepath.setObjectName("Sourcepath")
        self.next = QtWidgets.QPushButton(self.page)
        self.next.setGeometry(QtCore.QRect(620, 620, 93, 28))
        self.next.setMaximumSize(QtCore.QSize(93, 28))
        self.next.setObjectName("next")
        self.openSource = QtWidgets.QPushButton(self.page)
        self.openSource.setGeometry(QtCore.QRect(460, 180, 171, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.openSource.setFont(font)
        self.openSource.setObjectName("openSource")
        self.TargetPath = QtWidgets.QLineEdit(self.page)
        self.TargetPath.setGeometry(QtCore.QRect(100, 250, 351, 22))
        self.TargetPath.setObjectName("TargetPath")
        self.openTarget = QtWidgets.QPushButton(self.page)
        self.openTarget.setGeometry(QtCore.QRect(460, 250, 171, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.openTarget.setFont(font)
        self.openTarget.setObjectName("openTarget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.page)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 20, 651, 111))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.page_2)
        self.treeWidget.setGeometry(QtCore.QRect(20, 120, 701, 401))
        self.treeWidget.setObjectName("treeWidget")
        self.okbut = QtWidgets.QPushButton(self.page_2)
        self.okbut.setGeometry(QtCore.QRect(610, 610, 93, 28))
        self.okbut.setObjectName("okbut")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.page_2)
        self.plainTextEdit_2.setEnabled(False)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(20, 10, 701, 101))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.label = QtWidgets.QLabel(self.page_2)
        self.label.setGeometry(QtCore.QRect(10, 550, 711, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.next.setText(_translate("Form", "next"))
        self.openSource.setText(_translate("Form", "Выбор исходной папки"))
        self.openTarget.setText(_translate("Form", "Выбор целевой папки"))
        self.plainTextEdit.setPlainText(_translate("Form", "Эта утилита предназначена для копирования недостающих файлов из исходной папки в целевую."))
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.headerItem().setText(0, _translate("Form", "Имя"))
        self.okbut.setText(_translate("Form", "ok"))
        self.plainTextEdit_2.setPlainText(_translate("Form", "Красным цветом обозначены файлы, которых нет в целевой папке, но есть в исходной\n"
"\n"
"Зелёным цветом обозначены файлы, которые есть в целевой папке, но нет в исходной"))
        self.label.setText(_translate("Form", "Выберете галочкой файлы, которые необходимо оставить в целевой папке и нажмите ok"))
