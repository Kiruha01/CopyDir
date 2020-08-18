from PyQt5 import QtWidgets, QtGui, QtCore
from form import Ui_Form  # импорт нашего сгенерированного файла
import sys
from PyQt5.QtWidgets import QTreeWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
import os


class Item:
    def __init__(self, path, num=0, getSource=lambda : "", getTarget=lambda: ""):
        """ root: корневая директория исследование
            path : путь к файлу

            num: 0 - без изменений
                 1 - только в целевой папке
                 2 - только в исходной папке
        """
        #self.root = root
        self.path = path
        self.name = os.path.basename(path)

        self.color = QtGui.QColor(255, 255, 255)
        self.root = getSource()
        if num == 1:
            self.color = QtGui.QColor(100, 255, 100)
            self.root = getTarget()
        elif num == 2:
            self.color = QtGui.QColor(255, 100, 100)


        if os.path.isdir(path):
            self.type = 'icos\\folder.ico'
        elif self.name.split('.')[-1] in ('png', 'jpg', 'jpeg', 'bmp', 'ico'):
            self.type = 'icos\\picture.ico'
        elif self.name.split('.')[-1] in ('mp4', 'avi', 'mov', 'mkv', 'mpg'):
            self.type = 'icos\\video.ico'
        elif self.name.split('.')[-1] in ('mp3', 'wav', 'ogg'):
            self.type = 'icos\\music.ico'
        else:
            self.type = 'icos\\file.ico'



class ClassCopyFiles(QtCore.QObject):
    running = False
    done = QtCore.pyqtSignal()
    
    def __init__(self, listOfCopy, sourceDir, targetDir):
        super(ClassCopyFiles, self).__init__()
        self.listOfCopy = listOfCopy
        self.sourceDir = sourceDir
        self.targetDir = targetDir
 
    # метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        from shutil import copy2
        for file in self.listOfCopy:
            if file.root == self.sourceDir:
                if os.path.isdir(os.path.join(file.root, file.path)):
                    os.makedirs(os.path.join(self.targetDir, file.path))
                else:
                    if not os.path.exists(os.path.dirname(os.path.join(self.targetDir, file.path))):
                        os.makedirs(os.path.dirname(os.path.join(self.targetDir, file.path)))
                    copy2(os.path.join(file.root, file.path), os.path.join(self.targetDir, file.path))
            elif file.root == self.targetDir:
                if os.path.isdir(os.path.join(file.root, file.path)):
                    os.rmdir(os.path.join(file.root, file.path))
                else:
                    os.remove(os.path.join(file.root, file.path))
        self.done.emit()

 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.tree = QTreeWidgetItem(self.ui.treeWidget, ['main'])
        self.tree.setExpanded(True)

        

        self.ui.okbut.clicked.connect(self.checkFiles)
        self.ui.openTarget.clicked.connect(self.openTargetDialog)
        self.ui.openSource.clicked.connect(self.openSourceDialog)
        self.ui.next.clicked.connect(self.page2)

        self.ui.treeWidget.itemDoubleClicked.connect(self.foo)


    def page2(self):
        self.statusBar().showMessage('Завершено')
        if self.ui.TargetPath.text() and self.ui.Sourcepath.text():
            if self.ui.TargetPath.text() == self.ui.Sourcepath.text():
                QMessageBox.warning(self, "Одно и то же", "Целевая и исходная папки не должны совпадать!")
                return 
            self.tree.setText(0, os.path.basename(self.ui.TargetPath.text()))
            self.tree.setIcon(0,  QIcon('icos\\folder.ico'))
            self.ui.stackedWidget.setCurrentIndex(1)
            self.__compareFiles(self.getSource(), self.getTarget(), self.tree)
        else:
            QMessageBox.warning(self, "Нет папок", "Пожалуйста, выберите целевую и исходную папки!")


    def getTarget(self):
        #print(os.path.abspath(self.ui.TargetPath.text()))
        return os.path.abspath(self.ui.TargetPath.text())

    def getSource(self):
        return os.path.abspath(self.ui.Sourcepath.text())


    def checkFiles(self):
        self.statusBar().showMessage('Идёт процесс сканирования...')
        listOfCopy = []
        def recursiveCheck(parent, path):
            for idx in range(parent.childCount()):
                if parent.child(idx).childCount() == 0:
                    if parent.child(idx).background(0) == QtGui.QColor(100, 255, 100) and parent.child(idx).checkState(0) == 0:
                        listOfCopy.append(Item(os.path.join(path, parent.child(idx).text(0)), 1, self.getSource, self.getTarget))
                    elif parent.child(idx).background(0) == QtGui.QColor(255, 100, 100) and parent.child(idx).checkState(0) == 2:
                        listOfCopy.append(Item(os.path.join(path, parent.child(idx).text(0)), 2, self.getSource, self.getTarget))
                else:
                    recursiveCheck(parent.child(idx), os.path.join(path, parent.child(idx).text(0)))
        recursiveCheck(self.tree, '')
        for x in listOfCopy:
            print(x.path)
        self.copyFiles(listOfCopy)



    def copyFiles(self, listOfFiles):
        self.thread = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.coping = ClassCopyFiles(listOfFiles, self.getSource(), self.getTarget())
        # перенесём объект в другой поток
        self.coping.moveToThread(self.thread)
        # после чего подключим все сигналы и слоты
        self.coping.done.connect(self.finish)
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.coping.run)
        # запустим поток
        self.thread.start()
        self.ui.okbut.setEnabled(False)
        self.ui.treeWidget.setEnabled(False)
        self.statusBar().showMessage('Идёт процесс копирования...')


    def finish(self):
        self.statusBar().showMessage('Завершено!')
        print("Copied!")



    def __compareFiles(self, sourceDir, targetDir, parent):
        
        """ sourceDir: исходный корень исследования
            targetDir: целевой корень исследования
            parent:    родитель элемента

        """

        changes = False # флаг на изменения 
        try:
            sourceFiles = os.listdir(sourceDir)
            targetFiles = os.listdir(targetDir)
        except PermissionError:
            return False
        except  FileNotFoundError:
            return False

        for f in targetFiles:
            if f in sourceFiles:
                if os.path.isdir(targetDir + '\\' + f):
                    item = self.__addfile(Item(os.path.join(targetDir, f)), parent)                           # добавим папку на всякий случай
                    changes = True
                    if not self.__compareFiles(os.path.join(sourceDir, f), os.path.join(targetDir, f), item): # а если там нет изменений
                        parent.removeChild(item)                                                              # то удаляем нахер эту грёбанную папку!
                        changes = False
                sourceFiles.remove(f)
            else:
                item = self.__addfile(Item(os.path.join(targetDir, f), 1), parent)
                if os.path.isdir(os.path.join(targetDir, f)):
                    self.loadAll(os.path.join(targetDir, f), item, 1)
                changes = True
                
        for f in sourceFiles:
            item = self.__addfile(Item(os.path.join(sourceDir, f), 2), parent)
            if os.path.isdir(os.path.join(sourceDir, f)):
                    self.loadAll(os.path.join(sourceDir, f), item, 2)
            changes = True
        return changes

    def __addfile(self, file, parent):
        """ file:   instance of Item
            parent: item in tree """
        item = QTreeWidgetItem(parent, [file.name])
        brush = QtGui.QBrush(file.color)
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(0, brush)
        if file.color == QtGui.QColor(255, 255, 255):
            item.setCheckState(0, QtCore.Qt.Unchecked)
        else:
            item.setCheckState(0, QtCore.Qt.Checked)
        item.setIcon(0, QIcon(file.type))
        item.setExpanded(True)
        return item

    def foo(self, item, col):
        if item.checkState(col) == 0:
            item.setCheckState(col, 2)
            lst = [item.child(x) for x in range(item.childCount())]
            while len(lst):
                lst[0].setCheckState(col, 2)
                if lst[0].childCount() > 0:
                    lst.extend([lst[0].child(x) for x in range(lst[0].childCount())])
                lst.pop(0)

        elif item.checkState(col) == 2:
            item.setCheckState(col, 0)
            lst = [item.child(x) for x in range(item.childCount())]
            while len(lst):
                lst[0].setCheckState(col, 0)
                if lst[0].childCount() > 0:
                    lst.extend([lst[0].child(x) for x in range(lst[0].childCount())])
                lst.pop(0)

        




    def loadAll(self, startpath, tree, num):
        try:
            ld = os.listdir(startpath)
        except PermissionError:
            return
        except  FileNotFoundError:
            return
        for element in ld:
            path_info = os.path.join(startpath, element)
            parent_itm = self.__addfile(Item(path_info, num), tree)
            if os.path.isdir(path_info):
                self.loadAll(path_info, parent_itm, num)



    def openTargetDialog(self):
        fname = QFileDialog.getExistingDirectory(self, 'Выбор целевой папки', os.getcwd())
        self.ui.TargetPath.setText(fname)

    def openSourceDialog(self):
        fname = QFileDialog.getExistingDirectory(self, 'Выбор исходной папки', os.getcwd())
        self.ui.Sourcepath.setText(fname)


 
 
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
 
sys.exit(app.exec())