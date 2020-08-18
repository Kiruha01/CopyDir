from PyQt5 import QtWidgets, QtGui, QtCore
from form import Ui_Form  # импорт нашего сгенерированного файла
import sys
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QIcon
import os


class Item:
    def __init__(self, path, num=0):
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
        if num == 1:
            self.color = QtGui.QColor(100, 255, 100)
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


 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.tree = QTreeWidgetItem(self.ui.treeWidget, ['main'])
        self.tree.setExpanded(True)

        self.__compareFiles("C:\\Users\\liss-\\Desktop\\dist", "C:\\Users\\liss-\\Desktop\\dist2", self.tree)
        #self.load_project_structure("D:\\script\\findFile", self.tree)

        ##self.ui.okbut.clicked.connect(self.check_files)



    def __compareFiles(self, sourceDir, targetDir, parent):
        """ sourceDir: исходный корень исследования
            targetDir: целевой корень исследования
            parent:    родитель элемента

        """

        changes = False # флаг на изменения 

        sourceFiles = os.listdir(sourceDir)
        targetFiles = os.listdir(targetDir)

        for f in targetFiles:
            if f in sourceFiles:
                if os.path.isdir(targetDir + '\\' + f):
                    item = self.__addfile(Item(targetDir + '\\' + f), parent)                     # добавим папку на всякий случай
                    changes = True
                    if not self.__compareFiles(sourceDir + '\\' + f, targetDir + '\\' + f, item): # а если там нет изменений
                        parent.removeChild(item) 
                        print(item.text(0))                             # то удаляем нахер эту грёбанную папку!
                        changes = False
                sourceFiles.remove(f)
            else:
                item = self.__addfile(Item(targetDir + '\\' + f, 1), parent)
                if os.path.isdir(targetDir + '\\' + f):
                    self.loadAll(targetDir + '\\' + f, item, 1)
                changes = True
                
        for f in sourceFiles:
            item = self.__addfile(Item(sourceDir + '\\' + f, 2), parent)
            if os.path.isdir(sourceDir + '\\' + f):
                    self.loadAll(sourceDir + '\\' + f, item, 2)
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



    def loadAll(self, startpath, tree, num):
        for element in os.listdir(startpath):
            path_info = startpath + "/" + element
            parent_itm = self.__addfile(Item(path_info, num), tree)
            if os.path.isdir(path_info):
                self.loadAll(path_info, parent_itm, num)


 
 
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
 
sys.exit(app.exec())