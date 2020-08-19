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

        #self.color = QtGui.QColor(255, 255, 255)
        self.root = getSource()
        if num == 1:
            #self.color = QtGui.QColor(100, 255, 100)
            self.root = getTarget()
        elif num == 2:
            pass#self.color = QtGui.QColor(255, 100, 100)


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
    def __str__(self):
        return self.name

'''
[ 1.txt, 2.txt, [New folder, 3.txt, 4.txt], 5.txt, New folder 2]

'''

def loadAll(startpath, num):
    lst = []
    try:
        ld = os.listdir(startpath)
        for element in ld:
            path_info = os.path.join(startpath, element)
            if os.path.isdir(path_info):
                lst.append([Item(path_info, num),])
                lst[-1].extend(loadAll(path_info, num))
            else:
                lst.append(Item(path_info, num))
    except PermissionError:
        return []
    except FileNotFoundError:
        return []
    return lst


def test(sourceDir, targetDir):
    changes = False # флаг на изменения 
    try:
        sourceFiles = os.listdir(sourceDir)
        targetFiles = os.listdir(targetDir)
    except PermissionError:
        return False
    except  FileNotFoundError:
        return False

    lst = []


    for f in targetFiles:
        if f in sourceFiles:
            if os.path.isdir(targetDir + '\\' + f):
                #item = self.__addfile(Item(os.path.join(targetDir, f)), parent)                           # добавим папку на всякий случай
                lst.append([Item(os.path.join(targetDir, f)),])

                changes = True
                res = test(os.path.join(sourceDir, f), os.path.join(targetDir, f))
                if not res: # а если там нет изменений
                    lst.pop(-1)                                                              # то удаляем нахер эту грёбанную папку!
                    changes = False
                else:
                    lst[-1].extend(res)
            sourceFiles.remove(f)
        else:
            if os.path.isdir(os.path.join(targetDir, f)):
                lst.append([Item(os.path.join(targetDir, f), 1),])
                lst[-1].extend(loadAll(os.path.join(targetDir, f), 1))
            else:
                lst.append(Item(os.path.join(targetDir, f), 1))
            changes = True
            
    for f in sourceFiles:
        if os.path.isdir(os.path.join(sourceDir, f)):
            lst.append([Item(os.path.join(sourceDir, f), 2),])
            lst[-1].extend(loadAll(os.path.join(sourceDir, f), item, 2))
        else:
            lst.append(Item(os.path.join(sourceDir, f), 2))
        
        changes = True
    return lst



print(test('C:\\Users\\liss-\\Desktop\\dist', 'C:\\Users\\liss-\\Desktop\\dist2')[-1])
