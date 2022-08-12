from PyQt5 import QtCore, QtWidgets, QtGui
import sys, time, math, codecs, json, copy, os
from MyItem import MyItem
from mydialog_window import Ui_MyDialog
from already_exists import Ui_Form
from dialog_with_obj import Ui_Form2
from path_is_possible import  Ui_Form_Path
from path_is_inpossible import  Ui_Form_Path2
from bug_in_path import Ui_Form_bug



positions_big = []
positions_big2 = []
list_of_obj_from_json = [] #справочник всех известных объектов
current_level = 0 #текущий большой объект
new_id = 0

class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args):

        super().__init__(*args)
        # self.setAcceptDrops(True)


    def dragMoveEvent(self, event):

        temp2 = self.mapToScene(event.pos()) #тут сделать проверку, почитать про itemAt как раз
        flag_vhocdeniya = 0
        #print(positions_big)
        #print(len(positions_big))
        if current_level == 0:
            if positions_big != [] and positions_big != [[0, 0], []]:
                for i in positions_big:

                    if int(i[0]-50) < int(temp2.x()) and int(i[0]+50) > int(temp2.x()) and int(i[1]-50) < int(temp2.y()) and int(i[1]+50) > int(temp2.y()):

                        super(MyGraphicsView, self).dragMoveEvent(event)
                        break

            elif positions_big == [[0, 0], []]:

                if int(positions_big[0][0] - 50) < int(temp2.x()) and int(positions_big[0][0] + 50) > int(temp2.x()) and int(positions_big[0][1] - 50) < int(
                    temp2.y()) and int(positions_big[0][1] + 50) > int(temp2.y()):
                    super(MyGraphicsView, self).dragMoveEvent(event)

        else:
            if temp2.x() > -200 and temp2.y() > -200 and temp2.x() < 200 and temp2.y() < 200:
                super(MyGraphicsView, self).dragMoveEvent(event)

        if flag_vhocdeniya == 0:
            flag_vhocdeniya = 0



    def dropEvent(self, event):
        temp2 = self.mapToScene(event.pos())
        flag_v_kruge = 0

        if current_level == 0:
            print("тут дейсвительно пусто!")
            if positions_big != [] and positions_big != [[0, 0], []]:
                for i in positions_big:

                    if int(i[0]-50) < int(temp2.x()) and int(i[0]+50) > int(temp2.x()) and int(i[1]-50) < int(temp2.y()) and int(i[1]+50) > int(temp2.y()):

                        super(MyGraphicsView, self).dropEvent(event)
                        flag_v_kruge = 1
                        break

            elif positions_big == [[0, 0], []]:

                if int(positions_big[0][0] - 50) < int(temp2.x()) and int(positions_big[0][0] + 50) > int(temp2.x()) and int(positions_big[0][1] - 50) < int(
                    temp2.y()) and int(positions_big[0][1] + 50) > int(temp2.y()):
                    super(MyGraphicsView, self).dropEvent(event)
                    flag_v_kruge = 1

        else:
            if temp2.x() > -200 and temp2.y() > -200 and temp2.x() < 200 and temp2.y() < 200:
                super(MyGraphicsView, self).dropEvent(event)
                flag_v_kruge = 1

        if flag_v_kruge == 0:
            self.scene().newBigCircle.emit(event.mimeData().text())

    def keyPressEvent(self, event):
        if event.key() == (QtCore.Qt.Key_Control and QtCore.Qt.Key_Z):
            print("нажатие")
            self.scene().CtrlZpressed.emit(self)
        else:
            super(MyGraphicsView, self).keyPressEvent(event)


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

class DataObject:

    def __init__(self, id, name, descript, path = 0):
        self.id = id
        self.name = name
        self.descript = descript
        self.path = path
        #self.connections = []


    def __repr__(self):
        return f' {self.id}, {self.name}'





class Conn:

    def __init__(self, id, type, conn,image, flag, descr):
        self.id = id
        self.type = type
        self.conn = conn
        self.image = image
        self.image_flag = flag
        self.descr = descr
        self.graph = []


    def __repr__(self):
        return f'{self.id}, {self.conn}'
        #return f' id = {self.id}, conn = {self.conn}'

    @staticmethod
    def search_for_id(list_obj, id):
        list_result = []

        for i in list_obj:
            if i.conn[1].id == int(id):
                list_result.append(i)


        return list_result


    @staticmethod
    def search_for_id2(list_obj, id):
        for tempr in list_obj:
            if tempr.conn[0].id == id:
                print("что то там такое")
                return tempr



    @staticmethod
    def add_conn(list_obj, id_big, id_small, type, descr):

        global new_id

        for i in list_of_obj_from_json:
            if i.id == id_small:
                id_small = i
                print("что то сделали")
                break

        for j in list_of_obj_from_json:
            if j.id == id_big:
                id_big = j
                print("что то снова сделали")
                break

        list_obj.append(Conn(new_id+1, type, [id_small, id_big], {"type": "circle", "params": {"x": 0, "y": 0, "radius":100} }, 0, descr))
        new_id = new_id + 1

    @staticmethod
    def add_conn2(list_obj, id_big, name, type, descr, desc_obj, path = 0):

        global new_id

        #id_small = DataObject(Conn.search_maximum(list_obj), name, desc_obj)
        id_small = DataObject(len(list_of_obj_from_json), name, desc_obj, path)
        flag_srabotalo = 0
        print("id_small", id_small)

        if flag_srabotalo == 0:
            for j in list_of_obj_from_json:
                if j.id == id_big:
                    id_big = j
                    print("что то снова сделали2")
                    flag_srabotalo = 1
                    break
        if flag_srabotalo == 0:
            print("все не так")
        list_of_obj_from_json.append(id_small)
        list_obj.append(Conn(new_id + 1, type, [id_small, id_big],
                             {"type": "circle", "params": {"x": 0, "y": 0, "radius": 100}}, 0, descr))
        new_id = new_id + 1


    @staticmethod
    def add_conn_big_circle_on_scene(list_obj, id_big, name, type, descr, desc_obj, path):
        global list_of_obj_from_json, new_id
        print("add_conn_big_circle_on_scene")
        print(list_of_obj_from_json)
        id_small = DataObject(len(list_of_obj_from_json), name, desc_obj, path) #создаем объект

        for j in list_of_obj_from_json: #ищем сцену
            if int(j.id) == 0:
                id_big = j
                print("что то снова сделали3")
                break

        list_of_obj_from_json.append(id_small) #добавляем элемент
        list_obj.append(Conn(new_id + 1, type, [id_small, id_big],
                             {"type": "circle", "params": {"x": 0, "y": 0, "radius": 100}}, 0, descr))
        print("list_obj", list_obj)
        new_id = new_id + 1


    @staticmethod
    def search_maximum(list_obj):
        local_max = 0
        for i in list_obj:
            if i.conn[0].id > local_max:
                local_max = i.conn[0].id

            if i.conn[1].id > local_max:
                local_max = i.conn[1].id
        return local_max+1

    @staticmethod
    def search_in_objbase(id):
        for i in list_of_obj_from_json:
            if i.id == id:
                return i


class Scene(QtWidgets.QGraphicsScene):
    NameItem = 1
    #
    selectedIt = QtCore.pyqtSignal(object)
    newIT = QtCore.pyqtSignal(object)
    delobj = QtCore.pyqtSignal(object)
    newBigCircle = QtCore.pyqtSignal(object)
    CtrlZpressed = QtCore.pyqtSignal(object)
    selectedIt = QtCore.pyqtSignal(object)
    RightButtonClicked = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *args, **kwargs)
        self.counterItems = 0



class MyMainWindow(QtWidgets.QMainWindow):

    def __init__(self, list_of_obj):
        super().__init__()
        self.list_of_obj = list_of_obj
        self.message = " "
        self.text = ""
        self.flag_uze_est = 0

        self.scene = Scene()
        self.buffer_back = []
        self.initUI(current_level)
        self.scene.setSceneRect(-400, -400, 800, 800)
        self.view = QtWidgets.QGraphicsView()
        self.setCentralWidget(self.view)

        #пробрасывем сигналы
        self.scene.selectedIt.connect(self.handleSelectIt)
        self.scene.newIT.connect(self.newItem)
        self.scene.delobj.connect(self.delObj)
        self.scene.newBigCircle.connect(self.createNewBigCiecle)
        self.scene.CtrlZpressed.connect(self.CtrlZ)
        self.scene.RightButtonClicked.connect(self.RightButton)





        self.view = MyGraphicsView(self.scene, self)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setAlignment(QtCore.Qt.AlignCenter)
        self.view.setScene(self.scene)
        self.view.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.view.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.view.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.view.resize(800, 800)
        self.view.setScene(self.scene)

        self.show()


    def initUI(self, id_big = 0):

        if id_big == 0:
            big_circles = Conn.search_for_id(self.list_of_obj, 0)

            len_of_big = len(big_circles)
            print("big_circles =", len_of_big)
            global positions_big
            global current_level


            positions_big = []
            k = 0
            R_Big = 100
            if len_of_big > 5:
                R_Big = 150
            if len_of_big > 8:
                R_Big = 200

            if len_of_big > 12:
                R_Big = 250
            R_little = 30
            if len_of_big == 1:
                positions_big = [[0, 0], []]
            if len_of_big > 1:
                angle = math.radians((360 / len_of_big))
                # заполняем список координат используя алгоритм
                for i in range(len_of_big):
                    x = R_Big * math.cos(i * angle)

                    y = R_Big * math.sin(i * angle)

                    positions_big.append([x, y])

            for i in big_circles:
                print(i)
                i.graph = MyItem(i.conn[0].id, "big", i.conn[0].name, i.id)
                i.graph.setPos(positions_big[k][0], positions_big[k][1])
                i.image["params"]["x"] = positions_big[k][0]
                i.image["params"]["y"] = positions_big[k][1]
                i.image["params"]["radius"] = R_Big
                self.scene.addItem(i.graph)
                k = k + 1
                little_circles = Conn.search_for_id(self.list_of_obj, i.conn[0].id)
                len_of_little = len(little_circles)
                positions_add = []
                n = 0
                if len_of_little == 1:
                    positions_add = [[0, 0], []]
                if len_of_little > 1:
                    angle = math.radians((360 / len_of_little))
                    # заполняем список координат используя алгоритм
                    for m in range(len_of_little):
                        x = R_little * math.cos(m * angle)

                        y = R_little * math.sin(m * angle)

                        positions_add.append([x, y])

                for j in little_circles:
                    print(j)
                    j.graph = MyItem(j.conn[0].id, "little", j.conn[0].name, j.id)
                    if j.image_flag != 1:
                        j.graph.setPos(positions_add[n][0], positions_add[n][1])
                        j.image["params"]["x"] = positions_add[n][0]
                        j.image["params"]["y"] = positions_add[n][1]
                        j.image["params"]["radius"] = R_little
                    elif j.image_flag == 1:
                        j.graph.setPos(j.image["params"]["x"], j.image["params"]["y"])
                        print(j.image["params"]["x"], j.image["params"]["y"])
                        print("отрисовали по дркгому")

                    j.graph.setParentItem(i.graph)
                    n = n + 1

            #buffer_back = self.list_of_obj.copy()
            #self.line.setText(self.text)
            self.line = QtWidgets.QLineEdit()
            self.line.resize(200, 30)
            self.line.move(-150, 370)
            self.scene.addWidget(self.line)
            self.btn = QtWidgets.QPushButton("Проверить")
            self.btn.move(50, 370)
            self.btn.resize(100, 30)
            self.scene.addWidget(self.btn)
            self.btn.clicked.connect(self.BtnClicked)
            self.newJsonObject()
        else:
            big_circles = Conn.search_for_id(self.list_of_obj, int(id_big))
            len_of_big = len(big_circles)
            print("big_circles =", big_circles)
            #global positions_big
            tempr2 = Conn.search_for_id2(self.list_of_obj, id_big)

            grand_big = MyItem(tempr2.conn[0].id, "grand", tempr2.conn[0].name, tempr2.id)
            grand_big.setPos(0, 0)
            self.scene.addItem(grand_big)
            global positions_big2
            positions_big2 = []
            k = 0
            R_Big = 100
            if len_of_big > 5:
                R_Big = 150
            if len_of_big > 8:
                R_Big = 200

            if len_of_big > 12:
                R_Big = 250
            R_little = 30
            if len_of_big == 1:
                positions_big2 = [[0, 0], []]
            if len_of_big > 1:
                angle = math.radians((360 / len_of_big))
                # заполняем список координат используя алгоритм
                for i in range(len_of_big):
                    x = R_Big * math.cos(i * angle)

                    y = R_Big * math.sin(i * angle)

                    positions_big2.append([x, y])

            for i in big_circles:
                print(i)
                i.graph = MyItem(i.conn[0].id, "big", i.conn[0].name, i.id)
                i.graph.setPos(positions_big2[k][0], positions_big2[k][1])
                i.graph.setParentItem(grand_big)
                k = k + 1
                little_circles = Conn.search_for_id(self.list_of_obj, i.conn[0].id)
                len_of_little = len(little_circles)
                positions_add2 = []
                n = 0
                if len_of_little == 1:
                    positions_add2 = [[0, 0], []]
                if len_of_little > 1:
                    angle = math.radians((360 / len_of_little))
                    # заполняем список координат используя алгоритм
                    for m in range(len_of_little):
                        x = R_little * math.cos(m * angle)

                        y = R_little * math.sin(m * angle)

                        positions_add2.append([x, y])

                for j in little_circles:
                    print(j)
                    j.graph = MyItem(j.conn[0].id, "little", j.conn[0].name, j.id)
                    j.graph.setPos(positions_add2[n][0], positions_add2[n][1])

                    j.graph.setParentItem(i.graph)
                    n = n + 1

            self.line = QtWidgets.QLineEdit()
            self.line.resize(200, 30)
            self.line.move(-150, 370)
            text2 = self.text.split("/")
            if self.text == "":
                self.text = str(current_level)
            elif int(text2[-1]) == int(current_level):
                pass
            else:
                self.text = self.text + "/" + str(current_level)

            self.line.setText(self.text)
            self.scene.addWidget(self.line)
            self.btn = QtWidgets.QPushButton("Проверить")
            self.btn.move(50, 370)
            self.btn.resize(100, 30)
            self.scene.addWidget(self.btn)
            self.btn.clicked.connect(self.BtnClicked)



            self.newJsonObject()


    def RightButton(self, item):
        print(item.conn_id)
        for i in self.list_of_obj:
            if i.id == item.conn_id:

                if type(i.conn[0].path) != int:
                    os.startfile(i.conn[0].path)
                else:
                    print("path=", i.conn[0].path)
                    bug_in_path = Form_bug_in_path()
                    bug_in_path.setGeometry(700, 450, 311, 183)
                    bug_in_path.exec()

    def BtnClicked(self):
        print(33)
        text = self.line.text()
        if text.find("/") != -1:
            text_list = text.split("/")
            len_list = len(text_list)-1
            list_result = []
            for j in range(len_list):
                flag = 0
                for i in self.list_of_obj:

                    if int(text_list[j]) == int(i.conn[1].id) and int(text_list[j + 1]) == int(i.conn[0].id):
                        list_result.append(1)
                        print("есть совпадение")
                        break

            if len(list_result) == len_list:
                path_is_possible = From_path_is_possible()
                path_is_possible.setGeometry(700, 450, 311, 183)
                path_is_possible.exec()
            else:
                path_is_inpossible = From_path_is_inpossible()
                path_is_inpossible.setGeometry(700, 450, 311, 183)
                path_is_inpossible.exec()
        else:
            print("hello")



    def CtrlZ(self):
        self.list_of_obj = []
        self.list_of_obj = self.buffer_back
        print("buffer_back", self.buffer_back)
        self.scene.clear()
        self.initUI(current_level)

    def newJsonObject(self):
        print("new Json object")

        with open("object_base2.json", 'w', encoding="utf8") as file_objects:
            # считали данные из открвтого файла
            data = []
            #формируем словарь для json
            for obj in list_of_obj_from_json:
                data2 = {}
                data2["obj_id"] = obj.id
                data2["obj_name"] = obj.name

                data2["obj_description"] = obj.descript
                data2["path"] = obj.path

                data.append(data2)

            # сохраняем данные в json
            data_objects = json.dump(data, file_objects, ensure_ascii=False, indent=4)
        data = []

        #формируем новый json файл со связями
        with open("connections_base2.json", 'w', encoding="utf8") as file_conn:
            data = []

            for conns in self.list_of_obj:

                data2 = {}
                data2["connection_id"] = conns.id
                data2["connection_type"] = conns.type
                data2["connection_ids"] = [conns.conn[0].id, conns.conn[1].id]
                data2["obj_image"] = conns.image
                data2["image_flag"] = conns.image_flag
                data2["connection_description"] = conns.descr

                data.append(data2)

            data_objects = json.dump(data, file_conn, ensure_ascii=False, indent=4)

    #отрисовываем большой желтый круг на сцене
    def createNewBigCiecle(self, item):
        self.buffer_back = self.list_of_obj.copy()
        print(self.buffer_back)

        if item.startswith("file"):
            print(item.split("/"))
            path = item[8:]
            print(path)
            # item.id2 = item.id2.split("/")[-1]
            name = item.split("/")[
                -1]  # убираем полный абсолютный путь, оставляем только название файла

            # проблема все таки здесь
            dial = MyDialog_big()
            dial.setGeometry(700, 450, 311, 250)
            dial.exec()
            if dial.fromarg:
                Conn.add_conn_big_circle_on_scene(self.list_of_obj, 0, name, dial.fromarg[0],
                               dial.fromarg[1], dial.fromarg[2], path)  # добавляем обьект в словарь
                self.scene.clear()
                self.initUI(current_level)  # вызываем перерисовку ui

        else:
            self.flag_uze_est = 0
            print("вот это вот в item:", item)
            temp_circle = Conn.search_in_objbase(int(item))
            temp_scene = Conn.search_in_objbase(0)

            for i in self.list_of_obj:
                if i.conn[0] == temp_circle and i.conn[1] == temp_scene:


                        self.flag_uze_est = 1
                        already_exists = Form_already_exists()
                        already_exists.setGeometry(700, 450, 311, 183)
                        already_exists.exec()
                        break

            if self.flag_uze_est == 0:

                # здесь сделать окно, с полями ввода
                dial = MyDialog_big()
                dial.setGeometry(700, 450, 311, 250)
                dial.exec()
                temp_circle = Conn.search_in_objbase(int(item))
                if dial.fromarg:
                    Conn.add_conn_big_circle_on_scene(self.list_of_obj, 0, temp_circle.name, dial.fromarg[0],
                                                      dial.fromarg[1],  dial.fromarg[2], temp_circle.path)  # добавляем обьект в словарь

                self.scene.clear()
                self.initUI(current_level)  # вызываем перерисовку ui

    #
    def delObj(self, item):
        print(item.conn_id)

        self.buffer_back = self.list_of_obj.copy()
        for i in self.list_of_obj:
            if i.id == item.conn_id:
                print("item.conn_id", item.conn_id)
                self.list_of_obj.remove(i)


        self.scene.clear()
        self.initUI(current_level)

    def newItem(self, item):
        print("newItem")

        print("item1 =", item.id) #ЭТО ИМЯ ОБЬЕКТА НА КОТОРОЕ ПЕРЕМЕШАЕТСЯ ОБЬЕКТ
        print("item2 =", item.id_peretask)  # ЭТО ИМЯ  ПЕРЕМЕЩАЕМОГО ОБЬЕКТА
        self.buffer_back = self.list_of_obj.copy()
        #проверка, является ли перетасвиваемый обьект файлом (из проводника папка или файл)

        #ЭТО ДОБАВЛЕНИЕ НОВОГО ФАЙЛА
        if item.id_peretask.startswith("file"):
            print("файл!")
            path = item.id_peretask[8:]
            print(item.id_peretask.split("/"))
            item.name = item.id_peretask.split("/")[-1] #убираем полный абсолютный путь, оставляем только название файла
            item.id_peretask = len(self.list_of_obj) #присваиваем новому обьекту id

            #проблема все таки здесь
            dial = MyDialog_big()
            dial.setGeometry(700, 450, 311, 250)
            dial.exec()
            if dial.fromarg:
                Conn.add_conn2(self.list_of_obj, int(item.id), item.name, dial.fromarg[0],
                              dial.fromarg[1], dial.fromarg[2], path)  # добавляем обьект в словарь
                self.scene.clear()
                self.initUI(current_level)  # вызываем перерисовку ui
        elif int(item.id) != int(item.id_peretask):
            self.flag_uze_est = 0

            for i in self.list_of_obj:

                if int(item.id_peretask) == int(i.conn[0].id):
                    if int(item.id) == int(i.conn[1].id):
                        self.flag_uze_est = 1
                        # already_exists = Form_already_exists()
                        # already_exists.setGeometry(700, 450, 311, 183)
                        # already_exists.exec()
                        print(item.eventPos)
                        print(item.id_peretask)
                        for j in self.list_of_obj:
                            if j.conn[0].id == int(item.id_peretask):
                                j.image["params"]["x"] = (item.eventPos.x())
                                j.image["params"]["y"] = (item.eventPos.y())

                                #print(item.eventPosX, item.eventPosY)
                                j.image_flag = 1
                                self.scene.clear()
                                self.initUI(current_level)

                        break

            if self.flag_uze_est == 0:

                #здесь сделать окно, с полями ввода
                dial = MyDialog()
                dial.setGeometry(700, 450, 311, 183)
                dial.exec()
                if dial.fromarg:

                    Conn.add_conn(self.list_of_obj, int(item.id), int(item.id_peretask), dial.fromarg[0], dial.fromarg[1]) #добавляем обьект в словарь

                self.scene.clear()
                self.initUI(current_level) #вызываем перерисовку ui
        else:
            already_exists = Form_already_exists()
            already_exists.setGeometry(700, 450, 311, 183)
            already_exists.exec()
            #видимо здесь сделать надо обработку
            print(item.eventPosX)
            print(item.eventPosY)

    def handleSelectIt(self, item):
        print("нажали")
        global current_level
        flag = 0
        #print(type(item.conn_id))
        for i in self.list_of_obj:
            if item.conn_id == i.id:
                current_level = i.conn[0].id
                flag = 1
                break
        if flag == 1:
            self.scene.clear()

            self.initUI(current_level)


def main(arguments):
    app = QtWidgets.QApplication(arguments)

    list_of_conns = []
    global list_of_obj_from_json, new_id
    list_of_obj_from_json = []
    with open("object_base.json", encoding="utf8") as file_objects:
        # считали данные из открвтого файла
        data_objects = json.load(file_objects)
        for i in data_objects:
            data = DataObject(i["obj_id"], i["obj_name"], i["obj_description"], i["path"])
            list_of_obj_from_json.append(data)

    with open("connections_base.json", encoding="utf8") as file_connections:
        # считали данные из открвтого файла
        data_conn = json.load(file_connections)
        for i in data_conn:
            data = Conn(i["connection_id"], i["connection_type"], i["connection_ids"], i["obj_image"], i["image_flag"], i["connection_description"])
            list_of_conns.append(data)

    for i in list_of_conns:
        for j in list_of_obj_from_json:
            if i.conn[0] == j.id:
                i.conn[0] = j
            if i.conn[1] == j.id:
                i.conn[1] = j

    print(list_of_conns)

    # print(list_of_obj)
    new_id = len(list_of_conns)
    window = MyMainWindow(list_of_conns)
    window.setWindowTitle("Connecton search")
    #window.setGeometry(450, 200, 600, 600)
    window.setGeometry(450, 200, 800, 800)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)
