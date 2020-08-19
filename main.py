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
    amount = QtCore.pyqtSignal(int)
    
    def __init__(self, listOfCopy, sourceDir, targetDir):
        super(ClassCopyFiles, self).__init__()
        self.listOfCopy = listOfCopy
        self.sourceDir = sourceDir
        self.targetDir = targetDir
 
    # метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        from shutil import copy2
        for i, file in enumerate(self.listOfCopy):
            self.amount.emit(int(i*100/len(self.listOfCopy)))
            print(int(1*100/len(self.listOfCopy)))
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
        print("Copied!")



class ClassResearchFiles(QtCore.QObject):
    running = False
    done = QtCore.pyqtSignal(list)
    info = QtCore.pyqtSignal(str)
    
    def __init__(self, sourceDir, targetDir):
        super(ClassResearchFiles, self).__init__()
        self.sourceDir = sourceDir
        self.targetDir = targetDir
 
    # метод, который будет выполнять алгоритм в другом потоке

    def NloadAll(self, startpath, num):
        lst = []
        try:
            ld = os.listdir(startpath)
            for element in ld:
                path_info = os.path.join(startpath, element)
                if os.path.isdir(path_info):
                    lst.append([Item(path_info, num),])
                    lst[-1].extend(self.NloadAll(path_info, num))
                else:
                    lst.append(Item(path_info, num))
        except PermissionError:
            return []
        except FileNotFoundError:
            return []
        return lst


    def test(self, sourceDir, targetDir):
        try:
            sourceFiles = os.listdir(sourceDir)
            targetFiles = os.listdir(targetDir)
        except PermissionError:
            return []
        except  FileNotFoundError:
            return []

        lst = []


        for f in targetFiles:
            self.info.emit(os.path.join(targetDir, f))
            if f in sourceFiles:
                if os.path.isdir(targetDir + '\\' + f):
                    #item = self.__addfile(Item(os.path.join(targetDir, f)), parent)                           # добавим папку на всякий случай
                    lst.append([Item(os.path.join(targetDir, f)),])
                    res = self.test(os.path.join(sourceDir, f), os.path.join(targetDir, f))
                    if not res: # а если там нет изменений
                        lst.pop(-1)                                                              # то удаляем нахер эту грёбанную папку!
                    else:
                        lst[-1].extend(res)
                sourceFiles.remove(f)
            else:

                if os.path.isdir(os.path.join(targetDir, f)):
                    lst.append([Item(os.path.join(targetDir, f), 1),])
                    lst[-1].extend(self.NloadAll(os.path.join(targetDir, f), 1))
                else:
                    lst.append(Item(os.path.join(targetDir, f), 1))
                
        for f in sourceFiles:
            self.info.emit(os.path.join(sourceDir, f))
            if os.path.isdir(os.path.join(sourceDir, f)):
                lst.append([Item(os.path.join(sourceDir, f), 2),])
                lst[-1].extend(self.NloadAll(os.path.join(sourceDir, f), 2))
            else:
                lst.append(Item(os.path.join(sourceDir, f), 2))

        return lst


    def run(self):
        lst = self.test(self.sourceDir, self.targetDir)
        print("Researhed!")
        self.done.emit(lst)


 
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
        self.coping.amount.connect(self.setProgress)
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.coping.run)
        # запустим поток
        self.thread.start()
        self.ui.okbut.setEnabled(False)
        self.ui.treeWidget.setEnabled(False)
        self.ui.progressBar.show()
        self.statusBar().showMessage('Идёт процесс копирования...')



    def finish(self):
        self.statusBar().showMessage('Завершено!')
        self.ui.progressBar.setProperty("value", 100)

    
    def setProgress(self, am):
        self.ui.progressBar.setProperty("value", am)



    def __compareFiles(self, sourceDir, targetDir, parent):
        
        """ sourceDir: исходный корень исследования
            targetDir: целевой корень исследования
            parent:    родитель элемента

        """
        from random import choice
        self.ui.say.setText(choice([
            "Ждать — значит обгонять, значит чувствовать время и настоящее не как дар, а как препятствие. (c)",
            "Науке пока неизвестно, сколько может ждать человек. (c)",
            "Как бы ни было коротко время ожидания, оно растягивается, когда находишься в неизвестности. (c)",
            "Ожидай всегда самого худшего, и тогда будет тебе приятный сюрприз. (c)",
            "Ждать невозможно лишь тогда, когда ничего не делаешь. (c)",
            "Ожидание счастливых дней бывает иногда лучше этих самых дней. (c)",
            "Нетерпение — ожидание в спешке. (c)",
            "Ожидание радости тоже есть радость. (c)",
            "Человек жив, пока ждет. (c)",
            "Живут — ожидая хорошего, а если нечего ждать — какая жизнь? (c)",
            "Страх ожидания — одна из самых тяжких мук человеческих. (c)"]))
        self.thread2 = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.research = ClassResearchFiles(sourceDir, targetDir)
        # перенесём объект в другой поток
        self.research.moveToThread(self.thread2)
        # после чего подключим все сигналы и слоты
        self.research.done.connect(self.startAdding)
        self.research.info.connect(self.printInfo)
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread2.started.connect(self.research.run)
        # запустим поток
        self.thread2.start()
        self.statusBar().showMessage('Идёт процесс cscan...')


    def printInfo(self, inf):
       # print(inf)
        self.ui.logging.appendPlainText(inf)


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


    def startAdding(self, lst):
        self.statusBar().showMessage('Идёт процесс построения дерева. Пожалуйста, подождите...')
        self.parseAndAdd(lst, self.tree)
        self.ui.stackedWidget.setCurrentIndex(2)
        self.statusBar().showMessage('')

    def parseAndAdd(self, lst, parent): # [ 1.txt, 2.txt, [New folder, 3.txt, 4.txt], 5.txt, [New folder 2]]
        for x in lst:
            if type(x) is list:
                item = self.__addfile(x[0], parent)
                self.parseAndAdd(x[1:], item)
            else:
                item = self.__addfile(x, parent)

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
            for element in ld:
                path_info = os.path.join(startpath, element)
                parent_itm = self.__addfile(Item(path_info, num), tree)
                if os.path.isdir(path_info):
                    self.loadAll(path_info, parent_itm, num)
        except PermissionError:
            return
        except FileNotFoundError:
            return



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