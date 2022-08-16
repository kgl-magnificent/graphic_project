from PyQt5 import QtCore, QtWidgets, QtGui
from my_windows.mydialog_window import Ui_MyDialog
from my_windows.already_exists import Ui_Form
from my_windows.dialog_with_obj import Ui_Form2
from my_windows.path_is_possible import  Ui_Form_Path
from my_windows.path_is_inpossible import  Ui_Form_Path2
from my_windows.bug_in_path import Ui_Form_bug
from my_windows.mydialog_window_current_level import Ui_MyDialog_cur_lev
from my_windows.list_obj import list_objs

#Эти классы используются для отрисовки диалоговых окон
class list_objts(list_objs, QtWidgets.QDialog):
     def __init__(self):
        super(list_objts, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("список объектов")

class Form_bug_in_path(Ui_Form_bug, QtWidgets.QDialog):
    def __init__(self):
        super(Form_bug_in_path, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Предупреждение!")

class Form_already_exists(Ui_Form, QtWidgets.QDialog):
    def __init__(self):
        super(Form_already_exists, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Предупреждение!")

class From_path_is_possible(Ui_Form_Path, QtWidgets.QDialog):
    def __init__(self):
        super(From_path_is_possible, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Успешно!")

class From_path_is_inpossible(Ui_Form_Path2, QtWidgets.QDialog):
    def __init__(self):
        super(From_path_is_inpossible, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Предупреждение!")

class MyDialog_big(Ui_Form2, QtWidgets.QDialog):
    def __init__(self):
        super(Ui_Form2, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Введите данные о связи")
        self.fromarg = []
        self.pushButton.clicked.connect(self.OK)
        self.pushButton_2.clicked.connect(self.Cancel)


    def OK(self):
        self.fromarg = []
        name_type = self.lineEdit.text()
        name_descr = self.lineEdit_2.text()
        obj_descr = self.lineEdit_3.text()
        self.fromarg.append(name_type)
        self.fromarg.append(name_descr)
        self.fromarg.append(obj_descr)
        self.close()


    def Cancel(self):
        self.close()

class MyDialog(Ui_MyDialog,  QtWidgets.QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Введите данные о связи")
        self.fromarg = []
        #6 buttons
        self.pushButton_ok.clicked.connect(self.OK)
        self.pushButton_cancel.clicked.connect(self.Cancel)


    def OK(self):
        self.fromarg = []
        name_type = self.lineEdit_type.text()
        name_descr = self.lineEdit_desc.text()
        self.fromarg.append(name_type)
        self.fromarg.append(name_descr)
        self.close()


    def Cancel(self):
        self.close()

class MyDialog_cur_lev(Ui_MyDialog_cur_lev,  QtWidgets.QDialog):
    def __init__(self):
        super(MyDialog_cur_lev, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Введите ID")
        self.fromarg = []
        #6 buttons
        self.pushButton_ok.clicked.connect(self.OK)
        self.pushButton_cancel.clicked.connect(self.Cancel)


    def OK(self):
        self.fromarg = []
        name_type = self.lineEdit_type.text()

        self.fromarg.append(name_type)

        self.close()


    def Cancel(self):
        self.close()
