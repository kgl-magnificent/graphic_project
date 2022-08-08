# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
import sys

#Изменил правила формирования из json
mScale = 1.2

#служебный слот для определения местоположения объектов
def on_changed(arr):
    print("on_changed", arr)

#в корне не правильно
#Класс реализации объекта круга ()
class MyItem(QtWidgets.QGraphicsItem):
    pen_width = 1.2
    def __init__(self, a, b, c):
        super().__init__()
        self.main_circle = a
        self.add_circle = b
        self.info = c
        self.len_main = 1 #len(list(self.main_circle)) #ТУТ ГОВНА
        self.len_add = len(self.add_circle)
        self.list3 = [[-35, -35], [5, -15], [-35, 10]]
        self.list_text = [[-75, -70], [-40, -45], [-5, 5], [-50, -5]]
        self.check()



    def check(self):
        pass
        #print("hello")
        #здесь надо сделать обработку кругов

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-50, -48, 100, 100)
        return path



    def boundingRect(self):
        return QtCore.QRectF(-60 - MyItem.pen_width, -60 - MyItem.pen_width, 115 + MyItem.pen_width*2, 115 + MyItem.pen_width*2)


    def paint(self, painter, option, widget):
        painter.save()
        yellow = QtGui.QColor(245, 233, 77)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.setBrush(yellow)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawEllipse(-50, -48, 100, 100)
        #self.rect = QRect(-50, -25, 100, 25)
        painter.setFont(QtGui.QFont("Tahoma", 10))
        painter.drawText( QtCore.QRect(-75, -70, 150, 25), QtCore.Qt.AlignCenter, self.info.get(self.main_circle))

        red = QtGui.QColor(255, 127, 80)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.setBrush(red)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setFont(QtGui.QFont("Tahoma", 6))


        for i in range(self.len_add):
                painter.drawEllipse(self.list3[i][0], self.list3[i][1], 30, 30)
                painter.drawText(QtCore.QRect(self.list_text[i+1][0], self.list_text[i+1][1], 70, 25), QtCore.Qt.AlignCenter, self.info.get(self.add_circle[i]))


        painter.restore()

    def wheelEvent(self, e):
        global mScale
        if int(e.delta()) > 0:
            mScale += 0.2
        else:
            mScale -= 0.2

        self.matrix = QtGui.QTransform()
        self.matrix.scale(mScale, mScale)
        self.setTransform(self.matrix, False)
        print(mScale)



class MyMainWindow(QtWidgets.QWidget):

    def __init__(self, dict_with_elem_conn, dict_obj_name, main_circles):
        super().__init__()
        self.dict_with_elem_conn = dict_with_elem_conn
        self.dict_obj_name = dict_obj_name
        self.main_circle = main_circles
        self.initUI()

    def initUI(self):
        self.locations = [[-120, -110], [0, -110], [140, -110], [-120, 0], [-120, 0]]
        self.scene = QtWidgets.QGraphicsScene(-300, -300, 600, 600)
        self.scene.setBackgroundBrush(QtCore.Qt.white)
        for i in range(len(self.dict_with_elem_conn)):
            print("len =", len(self.dict_with_elem_conn))
            print(self.dict_with_elem_conn.get(self.main_circle[i]))

            self.ellipse = MyItem(self.main_circle[i], (self.dict_with_elem_conn.get(self.main_circle[i])), self.dict_obj_name)
            self.ellipse.setPos(self.locations[i][0], self.locations[i][1])
            self.scene.addItem(self.ellipse)
            self.ellipse.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
            self.ellipse.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
            self.ellipse.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)


        self.view = QtWidgets.QGraphicsView(self.scene)

        self.box = QtWidgets.QVBoxLayout(self)
        self.box.addWidget(self.view)
        self.setWindowTitle("Графический проект")
        self.show()

    # def wheelEvent(self, e):
    #     global mScale
    #     # if int(e.delta()) > 0:
    #     mScale += 0.2
    #     # else:
    #     #     mScale -= 0.2
    #
    #     self.matrix = QtGui.QTransform()
    #     self.matrix.scale(mScale, mScale)
    #     self.setTransform(self.matrix, False)
    #     #print(e.delta().y())




def main(arguments):

    list_of_conn = []
    with open("object_base.json", encoding="utf8") as file_objects:
        data_objects = json.load(file_objects)

    with open("connections_base.json", encoding="utf8") as file_connections:
        data_conn = json.load(file_connections)

    # print(data_objects[2]["obj_image"]["type"])

    for i in data_conn:
        list_of_conn.append(i["connection_ids"])

    print(list_of_conn)

    a = []
    b = []
    main_circles = set()  # перечисление внешних кругов
    additional_circles = set()  # перечисление внутренних кругов

    for j in data_objects:
        a.append(j["obj_id"])
        b.append(j["obj_name"])

    dict_obj_name = dict(zip(a, b))  # сть словарь: id и название

    print(dict_obj_name)
    list_of_conn2 = list_of_conn
    for i in range(len(list_of_conn)):
        main_circles.add(list_of_conn[i][1])
        additional_circles.add(list_of_conn[i][0])
        # list_of_conn2[i][0] = dict_obj_name.get(list_of_conn[i][0])
        # list_of_conn2[i][1] = dict_obj_name.get(list_of_conn[i][1])

    a = []
    b = []

    for i in additional_circles:
        a.append(dict_obj_name.get(i))
    for j in main_circles:
        b.append(dict_obj_name.get(j))
    print(a)
    print(b)

    dict_with_elem_conn = {}
    print(list_of_conn)
    for i in list_of_conn:
        if i[1] in dict_with_elem_conn:
            (dict_with_elem_conn.get(i[1])).append(i[0])
        else:
            dict_with_elem_conn[i[1]] = []
            dict_with_elem_conn[i[1]].append(i[0])
    print(dict_with_elem_conn)

    #main_circle = []
    main_circle = list(main_circles)

    app = QtWidgets.QApplication(arguments)

    window = MyMainWindow(dict_with_elem_conn, dict_obj_name, main_circle)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import json
    main(sys.argv)












