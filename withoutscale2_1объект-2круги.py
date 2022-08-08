
from PyQt5 import QtCore, QtWidgets, QtGui
import sys, openpyxl, time, math, codecs, json
from MyItem import MyItem
from mydialog_window import Ui_MyDialog

class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args):
        super().__init__(*args)


class MyDialog(Ui_MyDialog,  QtWidgets.QDialog):
    def __init__(self):
        super(MyDialog,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Введите данные о связи")
        self.fromarg = []
        #6 buttons
        self.pushButton_ok.clicked.connect(self.OK)
        self.pushButton_cancel.clicked.connect(self.Cancel)

        #6label display label
        #label_name,label_sex,label_age,label_date,label_h,label_w
        #7 A LineEdit edit box is used to input information and has the same function as the button above
        #namelineEdit,sexlineEdit,agelineEdit,datelineEdit,hlineEdit,wlineEdit,lovelineEdit


    def OK(self):
        self.fromarg = []
        name_type = self.lineEdit_type.text()
        name_descr = self.lineEdit_desc.text()
        self.fromarg.append(name_type)
        self.fromarg.append(name_descr)
        self.close()


    def Cancel(self):
        self.close()


class DataOject:

    def __init__(self, id, name, descript):
        self.id = id
        self.name = name

        self.descript = descript
        self.connections = []
        self.graph_obj = []

    def __repr__(self):
        return f' id_obj = {self.id}, conn = {self.connections}, graph_obj = {self.graph_obj}'

    @staticmethod
    def search_for_id(list_of_obj, id):
        new_list = []
        for i in list_of_obj:
            for j in i.connections:
                if id == j.conn[1] and j.conn not in new_list:
                    new_list.append(j.conn[0])
        return new_list

    @staticmethod
    def all_conns(list_of_obj):
        new_list = []
        for i in list_of_obj:
            for j in i.connections:
                if j.conn not in new_list:
                    new_list.append(j.conn)

        return new_list

    @staticmethod
    def add_conn(list_of_obj, id1, id2, type, descr):
        for i in list_of_obj:
            if i.id == id1:
                i.connections.append(Conn(15, type, [int(id2), int(id1)], {"type": "circle", "params": {"x": 0, "y": 0, "radius":100}}, descr))

    @staticmethod
    def big_circles(list_of_obj):
        list_big = []
        for i in list_of_obj:
            if i.connections:
                if i.id == 0:
                    continue
                for j in i.graph_obj:
                    if j.circle_type == "big":
                        list_big.append(j)
        return list_big

    @staticmethod
    def little_circles(list_of_obj, id_big):
        list_little = []
        id_big = id_big.id
        list_of_data = DataOject.search_for_id(list_of_obj, id_big)
        for i in list_of_obj:
            for j in list_of_data:
                if i.id == j:
                    print(i.graph_obj)
                    for k in i.graph_obj:
                        if k.circle_type == "little":
                            list_little.append(k)

        return list_little

    @staticmethod
    def draw_little_circle(list_obj, item):
        for i in list_obj:
            if i.id == int(item.id2):
                for j in list_obj:
                    if j.id == int(item.id2):
                        i.graph_obj.append(MyItem(item.id2, "little", i.name))

    @staticmethod
    def get_object(list_obj, id):
        for i in list_obj:
            if i.id == id:
                return i

    @staticmethod
    def undo_flag_scene(list_obj):
        for i in list_obj:
            for j in i.graph_obj:
                j.flag_scene = 0






class Conn:

    def __init__(self, id, type, conn,image, descr):
        self.id = id
        self.type = type
        self.conn = conn
        self.image = image
        self.descr = descr

    def __repr__(self):
        return f'{self.conn}'
        #return f' id = {self.id}, conn = {self.conn}'


class Scene(QtWidgets.QGraphicsScene):
    NameItem = 1
    #
    selectedIt = QtCore.pyqtSignal(object)
    newIT = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        QtWidgets.QGraphicsScene.__init__(self, *args, **kwargs)
        self.counterItems = 0


class MyMainWindow(QtWidgets.QMainWindow):

    # это нужно для вывода в статус бар
    # def onSelectionChanged(self):
    #     message = "Items selecteds: "
    #     for item in self.scene.selectedItems():
    #         message += " " + item.data(Scene.NameItem)
    #     self.statusBar().showMessage(message)

    #def __init__(self, *args, **kwargs):
    #инициализация конструктора
    #def __init__(self, dict_with_elem_conn, dict_obj_name):
    def __init__(self, list_of_obj):
        super().__init__()
        self.list_of_obj = list_of_obj
        self.message = " "
        #QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        #self.scene = QtWidgets.QGraphicsScene()
        self.scene = Scene()
        self.initGraphicsObject()
        self.initUI()
        self.scene.setSceneRect(-300, -300, 600, 600)
        self.view = QtWidgets.QGraphicsView()
        self.setCentralWidget(self.view)

        #пробрасывем сигналы
        # self.scene.selectedIt.connect(self.handleSelectIt)
        self.scene.newIT.connect(self.newItem)

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
        self.view.resize(600, 600)
        self.view.setScene(self.scene)

        self.show()

    def initGraphicsObject(self):
        for i in self.list_of_obj:
            if i.id == 0:
                continue

            if i.connections:
                i.graph_obj.append(MyItem(i.id, "big", i.name))

            else:
                i.graph_obj.append(MyItem(i.id, "little", i.name))



    def initUI(self, if_repaint = 0):

        if if_repaint == 0:
        #Добавиить в алгаритм проверку . если объектов несколько! графических т.е если объект на сцене
            Radius_main = 100
            k = 0
            positions = []
            count_big_circles = len(DataOject.search_for_id(self.list_of_obj, 0))
            if count_big_circles == 1:
                positions = [[0, 0], []]
            if count_big_circles > 1:
                angle = math.radians((360 / count_big_circles))
                # заполняем список координат используя алгоритм
                for i in range(count_big_circles):
                    x = Radius_main * math.cos(i * angle)

                    y = Radius_main * math.sin(i * angle)

                    positions.append([x, y])


            for i in DataOject.search_for_id(self.list_of_obj, 0):
                print(i)
                obj = DataOject.get_object(self.list_of_obj, i)
                obj.graph_obj[0].setPos(positions[k][0], positions[k][1])
                self.scene.addItem(obj.graph_obj[0])
                k += 1
                positions_add = []
                R = 30
                n = 0

                count = len(DataOject.search_for_id(self.list_of_obj, i))
                if count == 1:
                    positions_add = [[0, 0], []]
                if count > 1:
                    angle = math.radians((360 / count))
                    # заполняем список координат используя алгоритм
                    for m in range(count):
                        x = R * math.cos(m * angle)

                        y = R * math.sin(m * angle)

                        positions_add.append([x, y])

                for j in DataOject.search_for_id(self.list_of_obj, i):
                    obj_add = DataOject.get_object(self.list_of_obj, j)
                    for additionalgraph_obj in obj_add.graph_obj:
                        if additionalgraph_obj.flag_scene == 0:
                            additionalgraph_obj.setPos(positions_add[n][0], positions_add[n][1])
                            additionalgraph_obj.setParentItem(obj.graph_obj[0])
                            additionalgraph_obj.flag_scene = 1
                            break
                    n += 1
        if  if_repaint == "again":
            DataOject.undo_flag_scene(self.list_of_obj)
            Radius_main = 100
            k = 0
            positions = []
            count_big_circles = len(DataOject.search_for_id(self.list_of_obj, 0))
            if count_big_circles == 1:
                positions = [[0, 0], []]
            if count_big_circles > 1:
                angle = math.radians((360 / count_big_circles))
                # заполняем список координат используя алгоритм
                for i in range(count_big_circles):
                    x = Radius_main * math.cos(i * angle)

                    y = Radius_main * math.sin(i * angle)

                    positions.append([x, y])

            for i in DataOject.search_for_id(self.list_of_obj, 0):
                print(i)
                obj = DataOject.get_object(self.list_of_obj, i)
                obj.graph_obj[0].setPos(positions[k][0], positions[k][1])
                self.scene.addItem(obj.graph_obj[0])
                k += 1
                positions_add = []
                R = 30
                n = 0

                count = len(DataOject.search_for_id(self.list_of_obj, i))
                if count == 1:
                    positions_add = [[0, 0], []]
                if count > 1:
                    angle = math.radians((360 / count))
                    # заполняем список координат используя алгоритм
                    for m in range(count):
                        x = R * math.cos(m * angle)

                        y = R * math.sin(m * angle)

                        positions_add.append([x, y])

                for j in DataOject.search_for_id(self.list_of_obj, i):
                    obj_add = DataOject.get_object(self.list_of_obj, j)
                    for additionalgraph_obj in obj_add.graph_obj:
                        if additionalgraph_obj.flag_scene == 0:
                            additionalgraph_obj.setPos(positions_add[n][0], positions_add[n][1])
                            additionalgraph_obj.setParentItem(obj.graph_obj[0])
                            additionalgraph_obj.flag_scene = 1
                            break
                    n += 1

    def initUI3(self):


        print(self.list_of_obj)
        l2 = []
        R2 = 100
        R = 30
        n = 0
        k = 0
        list_of_big_circles = DataOject.big_circles(self.list_of_obj)
        count_big_circles = len(list_of_big_circles)
        if count_big_circles == 1:
            l2 = [[0, 0], []]
        if count_big_circles > 1:
            angle = math.radians((360 / count_big_circles))
            # заполняем список координат используя алгоритм
            for i in range(count_big_circles):
                x = R2 * math.cos(i * angle)

                y = R2 * math.sin(i * angle)

                l2.append([x, y])


        for i in list_of_big_circles:

            i.setPos(l2[k][0], l2[k][1])
            k = k + 1
            self.scene.addItem(i)

            n = 0
            l = []

            list_of_little_circles = DataOject.little_circles(self.list_of_obj, i)
            count = len(list_of_little_circles)
            if count == 1:
                l = [[0, 0], []]
            if count > 1:
                angle = math.radians((360 / count))
                # заполняем список координат используя алгоритм
                for m in range(count):
                    x = R * math.cos(m * angle)

                    y = R * math.sin(m * angle)

                    l.append([x, y])

            for j in list_of_little_circles:
                j.setPos(l[n][0], l[n][1])
                n = n + 1
                j.setParentItem(i)




        #фунция вывода всех больших кругов


    def newItem(self, item):

        print("item1 =", item.id) #ЭТО ИМЯ ОБЬЕКТА НА КОТОРОЕ ПЕРЕМЕШАЕТСЯ ОБЬЕКТ
        print("item2 =", item.id2)  # ЭТО ИМЯ  ПЕРЕМЕЩАЕМОГО ОБЬЕКТА
        #проверка, является ли перетасвиваемый обьект файлом (из проводника папка или файл)
        if item.id2.startswith("file"):
            print("файл!")
            print(item.id2.split("/"))
            #item.id2 = item.id2.split("/")[-1]
            item.name = item.id2.split("/")[-1] #убираем полный абсолютный путь, оставляем только название файла
            item.id2 = len(self.list_of_obj) #присваиваем новому обьекту id

            #проблема все таки здесь
            self.list_of_obj.append(DataOject(item.id2, item.name,  "какое то описание" ))
            #[item.id2] = item.name #добавляем name -id в соответсвующую стурктуру
            #print("новый словарь", self.dict_obj_name)
        if int(item.id) != int(item.id2): #проверяем, не являются ли обьекты одинаковыми
            if int(item.id2) not in  DataOject.search_for_id(self.list_of_obj, item.id): #защита от двойного добавления обьектов
                #здесь сделать окно, с полями ввода
                dial = MyDialog()
                dial.setGeometry(600, 350, 311, 183)
                dial.exec()
                if dial.fromarg:

                    DataOject.add_conn(self.list_of_obj, item.id, item.id2, dial.fromarg[0], dial.fromarg[1]) #добавляем обьект в словарь
                    DataOject.draw_little_circle(self.list_of_obj, item)

                #print("здесь мы помняли словарь", self.dict_with_elem_conn)
                self.initUI("again") #вызываем перерисовку ui







def main(arguments):
    app = QtWidgets.QApplication(arguments)

    list_of_obj = []


    with open("object_base.json", encoding="utf8") as file_objects:
        # считали данные из открвтого файла
        data_objects = json.load(file_objects)

        for i in data_objects:
            data_object = DataOject(i["obj_id"], i["obj_name"],  i["obj_description"])
            list_of_obj.append(data_object)


    #print(list_of_obj)


    # открвли второй файл для работы с данными
    with open("connections_base.json", encoding="utf8") as file_connections:
        # считали данные из открвтого файла
        data_conn = json.load(file_connections)
        for i in list_of_obj:
            for j in data_conn:
                if j["connection_ids"][1] == i.id:
                    data_of_conn = Conn(j["connection_id"], j["connection_type"], j["connection_ids"], j["obj_image"], j["connection_description"])
                    i.connections.append(data_of_conn)



    window = MyMainWindow(list_of_obj)
    window.setWindowTitle("Circles")
    window.setGeometry(450, 200, 600, 600)
    window.show()
    sys.exit(app.exec_())







if __name__ == "__main__":
    main(sys.argv)
