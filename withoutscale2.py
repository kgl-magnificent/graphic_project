from PyQt5 import QtCore, QtWidgets, QtGui
import sys, time, math, codecs, json, copy, os
from MyItem import MyItem
from window_classes import list_objts, Form_bug_in_path, Form_already_exists,\
    From_path_is_possible, From_path_is_inpossible, MyDialog_big, MyDialog, MyDialog_cur_lev


#from globals import positions_big, positions_big2, list_of_obj_from_json, current_level, new_id



positions_big = []
positions_big2 = []

list_of_obj_from_json = [] #справочник всех известных объектов
current_level = 0 #текущий большой объект
new_id = 0

#кастомный класс view
class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args):

        super().__init__(*args)
        # self.setAcceptDrops(True)

    #использется для реализации возможности моздания новых кругов на сцене
    def dragMoveEvent(self, event):
        #определяем место нахождения зажатого круга на сцене
        temp2 = self.mapToScene(event.pos())
        flag_vhocdeniya = 0 #флаг проверки выполнения условия
        if current_level == 0: #проверяем, какой объект ведущий: 0 - Сцена
            #граничные условия: positions_big = [] гругов на сцене нет; positions_big != [[0, 0], []] - на сцене один кркг
            if positions_big != [] and positions_big != [[0, 0], []]:
                #выполняем проверку место нахождения нахождения круга: ЕСЛИ ОН НАД ДРУГИМ КРУГОМ ТО ПЕРЕХОДИМ В МЕТОДЫ MYITEM
                for i in positions_big:

                    if int(i[0]-50) < int(temp2.x()) and int(i[0]+50) > int(temp2.x()) and int(i[1]-50) < int(temp2.y()) and int(i[1]+50) > int(temp2.y()):

                        super(MyGraphicsView, self).dragMoveEvent(event)
                        break
            #если круг один
            elif positions_big == [[0, 0], []]:
                #выполняем проверку место нахождения нахождения круга: ЕСЛИ ОН НАД ДРУГИМ КРУГОМ ТО ПЕРЕХОДИМ В МЕТОДЫ MYITEM
                if int(positions_big[0][0] - 50) < int(temp2.x()) and int(positions_big[0][0] + 50) > int(temp2.x()) and int(positions_big[0][1] - 50) < int(
                    temp2.y()) and int(positions_big[0][1] + 50) > int(temp2.y()):
                    super(MyGraphicsView, self).dragMoveEvent(event)

        else:
            #выполняем проверку место нахождения нахождения круга: ЕСЛИ ОН НАД ДРУГИМ КРУГОМ ТО ПЕРЕХОДИМ В МЕТОДЫ MYITEM
            if temp2.x() > -200 and temp2.y() > -200 and temp2.x() < 200 and temp2.y() < 200:
                super(MyGraphicsView, self).dragMoveEvent(event)
        #это сделано для того, если ни одно из условий не подошло, то есть super'ы не сработали, вызвался бы метод drop event
        if flag_vhocdeniya == 0:
            flag_vhocdeniya = 0



    def dropEvent(self, event):
        temp2 = self.mapToScene(event.pos())
        flag_v_kruge = 0
        #проверка текущего уровня: 0 - сцена
        if current_level == 0:
            print("тут дейсвительно пусто!")
            #граничные условия: positions_big = [] гругов на сцене нет; positions_big != [[0, 0], []] - на сцене один кркг
            if positions_big != [] and positions_big != [[0, 0], []]:
                for i in positions_big:
                    #выполняем проверку место отпускания круга: ЕСЛИ ОН НАД ДРУГИМ КРУГОМ ТО ПЕРЕХОДИМ В МЕТОДЫ MYITEM
                    if int(i[0]-50) < int(temp2.x()) and int(i[0]+50) > int(temp2.x()) and int(i[1]-50) < int(temp2.y()) and int(i[1]+50) > int(temp2.y()):
                        #если отпустили над другим кругом, то обрабатывается в классе MyItem
                        super(MyGraphicsView, self).dropEvent(event)
                        flag_v_kruge = 1
                        break
            #если круг один
            elif positions_big == [[0, 0], []]:
                #выполняем проверку место отпускания круга: ЕСЛИ ОН НАД ДРУГИМ КРУГОМ ТО ПЕРЕХОДИМ В МЕТОДЫ MYITEM
                if int(positions_big[0][0] - 50) < int(temp2.x()) and int(positions_big[0][0] + 50) > int(temp2.x()) and int(positions_big[0][1] - 50) < int(
                    temp2.y()) and int(positions_big[0][1] + 50) > int(temp2.y()):
                     #если отпустили над другим кругом, то обрабатывается в классе MyItem
                    super(MyGraphicsView, self).dropEvent(event)
                    flag_v_kruge = 1

        else:
            #если сцена - не главный объект
            if temp2.x() > -200 and temp2.y() > -200 and temp2.x() < 200 and temp2.y() < 200:
                #обработка в MyItem
                super(MyGraphicsView, self).dropEvent(event)
                flag_v_kruge = 1
        #если отпустили круг не над дркгим кругом, то происходит создание большого круга на сцене
        if flag_v_kruge == 0:
            list_with_data = []
            list_with_data.append(event.mimeData().text())
            positions = self.mapToScene(event.pos())
            list_with_data.append(positions)
            self.scene().newBigCircle.emit(list_with_data)
    #обработка нажатия Ctrl_Z
    def keyPressEvent(self, event):
        if event.key() == (QtCore.Qt.Key_Control and QtCore.Qt.Key_Z):
            #если нажато Ctrl_Z вызываем сигнал
            self.scene().CtrlZpressed.emit(self)
        else:
            #если не Ctrl_Z, то ничего не делаем
            super(MyGraphicsView, self).keyPressEvent(event)



class DataObject:
    #создаем класс для хранения данных об объектах
    def __init__(self, id, name, descript, path = 0):
        self.id = id
        self.name = name
        self.descript = descript
        self.path = path
        #self.connections = []


    def __repr__(self):
        return f' {self.id}, {self.name}'





class Conn:
    #создаем класс для хранения данных о связях
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
    #функция поиска объекта по id (если оббъектов несколько)
    @staticmethod
    def search_for_id(list_obj, id):
        list_result = []

        for i in list_obj:
            if i.conn[1].id == int(id):
                list_result.append(i)


        return list_result

    #функция поиска объекта по id (если объект один)
    @staticmethod
    def search_for_id2(list_obj, id):
        for tempr in list_obj:
            if tempr.conn[0].id == id:
                print("что то там такое")
                return tempr


    #добавляем связь если нет новых объеков
    @staticmethod
    def add_conn(list_obj, id_big, id_small, type, descr):

        global new_id
        #находим данных о связываемых объектах
        for i in list_of_obj_from_json:
            if i.id == id_small:
                id_small = i
                print("что то сделали")
                break
        #находим данных о связываемых объектах
        for j in list_of_obj_from_json:
            if j.id == id_big:
                id_big = j
                print("что то снова сделали")
                break
        #создаем связь
        list_obj.append(Conn(new_id+1, type, [id_small, id_big], {"type": "circle", "params": {"x": 0, "y": 0, "radius":100} }, 0, descr))
        new_id = new_id + 1 #обновили текущий id в базе данных связи

    @staticmethod
    #добавляем связь если есть новый объект
    def add_conn2(list_obj, id_big, name, type, descr, desc_obj, path = 0):

        global new_id

        #создаем объект
        id_small = DataObject(len(list_of_obj_from_json), name, desc_obj, path)
        flag_srabotalo = 0


        #ищем второй связываемый объект в базе
        for j in list_of_obj_from_json:
            if j.id == id_big:
                id_big = j


                break
        #добавляем объект в базу
        list_of_obj_from_json.append(id_small)
        #добавляем связь в базу
        list_obj.append(Conn(new_id + 1, type, [id_small, id_big],
                             {"type": "circle", "params": {"x": 0, "y": 0, "radius": 100}}, 0, descr))
        new_id = new_id + 1


    @staticmethod
    #функция добавления большого круга на сцену
    def add_conn_big_circle_on_scene(list_obj, id_big, name, type, descr, desc_obj, path):
        global list_of_obj_from_json, new_id
        #создаем объект
        id_small = DataObject(len(list_of_obj_from_json), name, desc_obj, path) #создаем объект
        #ищим объект сцены
        for j in list_of_obj_from_json: #ищем сцену
            if int(j.id) == 0:
                id_big = j
                print("что то снова сделали3")
                break
        #добавляем объект в базу
        list_of_obj_from_json.append(id_small) #добавляем элемент
        #добавляем связь в базу
        list_obj.append(Conn(new_id + 1, type, [id_small, id_big],
                             {"type": "circle", "params": {"x": 0, "y": 0, "radius": 100}}, 0, descr))

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

    #функция поиска связи в базе
    @staticmethod
    def search_in_objbase(id):
        for i in list_of_obj_from_json:
            if i.id == id:
                return i


#кастомизировали класс сцены
class Scene(QtWidgets.QGraphicsScene):
    NameItem = 1
    #пробросили сигналы
    selectedIt = QtCore.pyqtSignal(object)
    newIT = QtCore.pyqtSignal(object)
    delobj = QtCore.pyqtSignal(object)
    newBigCircle = QtCore.pyqtSignal(object)
    CtrlZpressed = QtCore.pyqtSignal(object)
    #selectedIt = QtCore.pyqtSignal(object)
    RightButtonClicked = QtCore.pyqtSignal(object)
    NewLevel = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *args, **kwargs)
        self.counterItems = 0


#шлавный класс ОКНО
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
        #self.view = QtWidgets.QGraphicsView()
        #self.setCentralWidget(self.view)

        #пробрасывем сигналы
        self.scene.selectedIt.connect(self.handleSelectIt)
        self.scene.newIT.connect(self.newItem)
        self.scene.delobj.connect(self.delObj)
        self.scene.newBigCircle.connect(self.createNewBigCiecle)
        self.scene.CtrlZpressed.connect(self.CtrlZ)
        self.scene.RightButtonClicked.connect(self.RightButton)
        self.scene.NewLevel.connect(self.NewLevel)



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

        self.menuFile = QtWidgets.QMenu("&File")

        self.actOpen = QtWidgets.QAction(self)
        self.actOpen.setText("&Список объектов")

        self.actOpen.triggered.connect(self.print_list_objs)
        #self.actOpen.hovered.connect(self.on_hovered)
        self.menuFile.addAction(self.actOpen)
        self.actMenuFile = self.menuBar().addMenu(self.menuFile)

        self.show()
    #метод отрисовки данных об объектах принадатии файл->список обхектов
    def print_list_objs(self):

        window_list_obj = list_objts()
        window_list_obj.setGeometry(650, 350, 400, 400)

        text = ""
        for i in list_of_obj_from_json:
            text = text + "id = " + str(i.id) + " name: " + str(i.name) + "\n"
        #window_list_obj.lineEdit_type.setText(text)
        window_list_obj.label.setText(text)
        window_list_obj.exec()

    #главный метод - рисует круги в окне
    def initUI(self, id_big = 0):

        if id_big == 0:
            big_circles = Conn.search_for_id(self.list_of_obj, 0)

            len_of_big = len(big_circles)
            print("big_circles =", len_of_big)
            global positions_big
            global current_level

            #определяем радиус
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
            #рисуем большие круги
            for i in big_circles:
                #print(i)
                i.graph = MyItem(i.conn[0].id, "big", i.conn[0].name, i.id)
                if i.image_flag == 0: #если смещения не было (в ручном режиме)
                    i.graph.setPos(positions_big[k][0], positions_big[k][1])
                    i.image["params"]["x"] = positions_big[k][0] #сохраняем координаты в json
                    i.image["params"]["y"] = positions_big[k][1]
                    i.image["params"]["radius"] = R_Big
                elif i.image_flag == 1: #если смещение было, то вытаскиваем координаты из json
                    i.graph.setPos(i.image["params"]["x"], i.image["params"]["y"])
                    positions_big[k][0] = i.image["params"]["x"]
                    positions_big[k][1] = i.image["params"]["y"]
                self.scene.addItem(i.graph)
                k = k + 1
                #ищем мальнькие круги для большого
                little_circles = Conn.search_for_id(self.list_of_obj, i.conn[0].id)
                len_of_little = len(little_circles)
                positions_add = []
                n = 0
                if len_of_little == 1:
                    positions_add = [[0, 0], []]
                if len_of_little > 1:
                    angle = math.radians((360 / len_of_little))
                    # заполняем список координат используя алгоритм
                    #формируем позиции
                    for m in range(len_of_little):
                        x = R_little * math.cos(m * angle)

                        y = R_little * math.sin(m * angle)

                        positions_add.append([x, y])

                for j in little_circles:
                    #print(j)
                    #отрисовываем мальникие круги
                    j.graph = MyItem(j.conn[0].id, "little", j.conn[0].name, j.id)
                    if j.image_flag == 0: #если сдвига не было, то координаты берем из алгоритма
                        j.graph.setPos(positions_add[n][0], positions_add[n][1])
                        j.image["params"]["x"] = positions_add[n][0]
                        j.image["params"]["y"] = positions_add[n][1]
                        j.image["params"]["radius"] = R_little
                    elif j.image_flag == 1:
                        #если был свиг, то координаты берем из json
                        j.graph.setPos(j.image["params"]["x"], j.image["params"]["y"])


                    j.graph.setParentItem(i.graph)
                    n = n + 1

            self.line = QtWidgets.QLineEdit()
            self.line.resize(200, 30)
            self.line.move(-150, 370)
            self.scene.addWidget(self.line)
            self.btn = QtWidgets.QPushButton("Проверить")
            self.btn.move(50, 370)
            self.btn.resize(100, 30)
            self.scene.addWidget(self.btn)
            self.text = ""
            #добавляем квадрат перехода
            square = MyItem(0, "square", "Переход", 0)
            square.setPos(345, -320)
            self.scene.addItem(square)



            self.btn.clicked.connect(self.BtnClicked)

            self.newJsonObject()
        else:
            big_circles = Conn.search_for_id(self.list_of_obj, int(id_big))
            len_of_big = len(big_circles)
            print("big_circles =", big_circles)
            #global positions_big
            tempr2 = Conn.search_for_id2(self.list_of_obj, id_big)
            #сделал очень большоц круг для наглядности


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
            #рисуем большой круг
            for i in big_circles:
                #print(i)
                i.graph = MyItem(i.conn[0].id, "big", i.conn[0].name, i.id)
                if i.image_flag == 0:
                    i.graph.setPos(positions_big2[k][0], positions_big2[k][1])
                elif i.image_flag == 1:
                    i.graph.setPos(i.image["params"]["x"], i.image["params"]["y"])
                    positions_big[k][0] = i.image["params"]["x"]
                    positions_big[k][1] = i.image["params"]["y"]
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
                    #print(j)
                    j.graph = MyItem(j.conn[0].id, "little", j.conn[0].name, j.id)
                    if j.image_flag == 0:
                        j.graph.setPos(positions_add2[n][0], positions_add2[n][1])

                        j.graph.setParentItem(i.graph)
                    elif j.image_flag == 1:
                         j.graph.setPos(j.image["params"]["x"], j.image["params"]["y"])
                    n = n + 1

            self.line = QtWidgets.QLineEdit()
            self.line.resize(200, 30)
            self.line.move(-150, 370)

            #формируем надпись с пройденными переходами
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

            square = MyItem(0, "square", "Переход", 0)
            square.setPos(345, -320)
            self.scene.addItem(square)




            self.newJsonObject()

    #запускаем файл, характеризующий круги
    def RightButton(self, item):
        print(item.conn_id)
        for i in self.list_of_obj:
            if i.id == item.conn_id:
                #выполняем проверку перед запуском, если путь не заполнен, то было бы 0
                if type(i.conn[0].path) != int:
                    os.startfile(i.conn[0].path)
                #пишем про ошибку пути
                else:
                    print("path=", i.conn[0].path)
                    bug_in_path = Form_bug_in_path()
                    bug_in_path.setGeometry(700, 450, 311, 183)
                    bug_in_path.exec()
    #метод проверки доступности пути
    #
    def BtnClicked(self):
        text = self.line.text()
        #проверка на то, что чисто не одно
        if text.find("/") != -1:
            text_list = text.split("/")
            len_list = len(text_list)-1
            list_result = []
            for j in range(len_list):
                flag = 0
                for i in self.list_of_obj:
                    #сравниваем полученный путь со списком связей
                    if int(text_list[j]) == int(i.conn[1].id) and int(text_list[j + 1]) == int(i.conn[0].id):
                        list_result.append(1)
                        print("есть совпадение")
                        break
            #выводим сообщение о возможности такого пути
            if len(list_result) == len_list:
                path_is_possible = From_path_is_possible()
                path_is_possible.setGeometry(700, 450, 311, 183)
                path_is_possible.exec()
            #выводим сообщение что такой путь не возможен
            else:
                path_is_inpossible = From_path_is_inpossible()
                path_is_inpossible.setGeometry(700, 450, 311, 183)
                path_is_inpossible.exec()


    #метод, который обеспечивает переход на заданный уровень вложенности
    def NewLevel(self):
        dial = MyDialog_cur_lev()
        dial.setGeometry(700, 450, 311, 200)
        dial.exec()
        if dial.fromarg:
            global current_level
            current_level = int(dial.fromarg[0])

            self.scene.clear()
            self.initUI(current_level)

    #метод обеспечивает работу CtrlZ комбинации
    def CtrlZ(self):
        #обеспечивается пктем возвращения списка связей в предыдущее положение
        self.list_of_obj = []
        self.list_of_obj = self.buffer_back
        self.scene.clear()
        self.initUI(current_level)

    #при изменении количесва объектов (создание нового, удаление) происходит изменение базы JSON
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

    #метод обработки добавления нового большого желтого круга на сцену
    def createNewBigCiecle(self, item):
        #копируемп текущую базу для возможности отмены с помощью комбинации CtrlZ
        self.buffer_back = self.list_of_obj.copy()
        list_of_args = item
        #если объект dnd из-вне (файл из проводника переносим на сцену)
        if list_of_args[0].startswith("file"):
            path = list_of_args[0][8:]
            name = list_of_args[0].split("/")[
                -1]  # убираем полный абсолютный путь, оставляем только название файла

            # создаем новый объект
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
            #проверка есть ли уже такой круг на сцене
            temp_circle = Conn.search_in_objbase(int(list_of_args[0].split("/")[0]))
            temp_scene = Conn.search_in_objbase(0)

            for i in self.list_of_obj:
                if i.conn[0] == temp_circle and i.conn[1] == temp_scene:

                    #флаг выполнения условия
                    self.flag_uze_est = 1
                    #обеспечивает сдвиг большого круга
                    #данные нового местоположения записываются в структуру и выставляется флаг отрисовки по координатам
                    i.image["params"]["x"] = list_of_args[1].x()
                    i.image["params"]["y"] = list_of_args[1].y()
                    i.image_flag = 1
                    self.scene.clear()
                    self.initUI(current_level)
                    break

            if self.flag_uze_est == 0:

                # эта ветка отрабатывает случай, если зеленый круг перенести на сцену
                dial = MyDialog_big()
                dial.setGeometry(700, 450, 311, 250)
                dial.exec()
                temp_circle = Conn.search_in_objbase(int(list_of_args[0].split("/")[0]))
                if dial.fromarg:
                    Conn.add_conn_big_circle_on_scene(self.list_of_obj, 0, temp_circle.name, dial.fromarg[0],
                                                      dial.fromarg[1],  dial.fromarg[2], temp_circle.path)  # добавляем обьект в словарь

                self.scene.clear()
                self.initUI(current_level)  # вызываем перерисовку ui

    #метод обработки нажания клавиши del
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
            print(item.id_peretask)
            item.name = item.id_peretask.split("/")[-1] #убираем полный абсолютный путь, оставляем только название файла
            item.id_peretask = len(self.list_of_obj) #присваиваем новому обьекту id
            print("работает эта ветка")

            #проблема все таки здесь
            dial = MyDialog_big()
            dial.setGeometry(700, 450, 311, 250)
            dial.exec()
            if dial.fromarg:
                Conn.add_conn2(self.list_of_obj, int(item.id), item.name, dial.fromarg[0],
                              dial.fromarg[1], dial.fromarg[2], path)  # добавляем обьект в словарь
                self.scene.clear()
                self.initUI(current_level)  # вызываем перерисовку ui

        #это обработка перетаскивания уже сущесвующего круга
        elif int(item.id) != int(item.id_peretask):
            self.flag_uze_est = 0



            for i in self.list_of_obj:



                print("old= ", item.conn_id_old)
                for l in self.list_of_obj:
                    if l.id == int(item.conn_id_old):
                        connection = l

                print("0 =", connection.conn[0].id)
                print("1 =", connection.conn[1].id)


                if int(item.id_peretask) == int(i.conn[0].id) and int(item.id) == int(i.conn[1].id):


                    self.flag_uze_est = 1
                    # already_exists = Form_already_exists()
                    # already_exists.setGeometry(700, 450, 311, 183)
                    # already_exists.exec()
                    print(item.eventPos)
                    print(item.id_peretask)
                    for j in self.list_of_obj:
                        #это смешение если обьект
                        if j.conn[0].id == int(item.id_peretask) and j.conn[1].id == int(item.id) and int(item.id) == int(connection.conn[1].id):
                            j.image["params"]["x"] = (item.eventPos.x())
                            j.image["params"]["y"] = (item.eventPos.y())

                                #print(item.eventPosX, item.eventPosY)
                            j.image_flag = 1
                            self.scene.clear()
                            self.initUI(current_level)

                            break
                        elif j.conn[0].id == int(connection.conn[0].id) and j.conn[1].id == int(connection.conn[1].id):
                            already_exists = Form_already_exists()
                            already_exists.setGeometry(700, 450, 311, 183)
                            already_exists.exec()

                elif int(item.id_peretask) == int(i.conn[0].id) and int(item.id) == int(i.conn[1].id):
                    self.flag_uze_est = 1
                    already_exists = Form_already_exists()
                    already_exists.setGeometry(700, 450, 311, 183)
                    already_exists.exec()

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
