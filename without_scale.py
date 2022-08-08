from PyQt5 import QtCore, QtWidgets, QtGui
import sys, openpyxl

mScale = 0.5
globalScale = 0
# https://qtcentre.org/threads/67783-PyQt-zooming-with-QGraphicsSceneWheelEvent
# https://www.cyberforum.ru/qt/thread2229093.html
# https://stackoverflow.com/questions/40680065/qgraphicsscene-view-scale-understanding
#https://github.com/trufont/defconQt/blob/master/Lib/defconQt/controls/glyphLineView.py


class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args):
        super().__init__(*args)
        #self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    # ПЕРЕОПЕРЕДЕЛИЛ МЕТОД ВРАЩЕНИЯ КОЛЕСИКА ПРЕДСТАВЛЕНИЯ
    # def wheelEvent(self, event):
    #     global globalScale
    #     adj = (event.angleDelta().y() / 120) * 0.1
    #     print(adj)
    #     if adj > 0:
    #         self.scale(1 + adj, 1 + adj) # работает нормально!
    #         # self.scale(1.5, 1.5)
    #     if adj < 0:
    #         # работает нормально
    #         self.scale(0.91, 0.91)  # Скорректировал значение масштаба
    #         # self.scale(0.75, 0.75)
    #     if adj > 0:
    #         globalScale += 1
    #
    #     if adj < 0:
    #         globalScale -= 1
    #     print(globalScale)


# СОЗДАЛ КЛАСС, КОТОРЫЙ ФОРМИРУЕТ ОБЬЕКТЫ СЦЕНЫ
#ЕСЛИ В КАЧЕСВЕ АРГУМЕНТА ПРИ ИНИЦИАЛИЗАЦИИ ОБЕКТА ПЕРЕДАТЬ СТРОКИ "big", "little" или vvLittle
#ТО будет создан эллипс (круг)

#ЕСЛИ В качесвтве аргумента указать "text", а затем уровень вложенности, а затем сам текст,
#ТО будет добавлена надпись определеноого уровня вложенности
class MyItem(QtWidgets.QGraphicsItem):
    global globalScale
    pen_width = 1.2
    def __init__(self, a, b, f = 0):
        super().__init__()
        self.type_of_obj = a #тип обьекта
        self.level_nested = b #уровень вложенности
        self.msg = f #текст для обьекта типа текст
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)

        if self.level_nested == 0:
            self._brush = QtGui.QBrush(QtCore.Qt.yellow)
            self.rectF = QtCore.QRectF(0, 0, 100, 100)
        if self.level_nested == 1:
            self._brush = QtGui.QBrush(QtCore.Qt.green)
            self.rectF = QtCore.QRectF(0, 0, 35, 35)

    def boundingRect(self):
        return self.rectF
        #от кругов осталось
        #return QtCore.QRectF(-55.5, -55.5, 110.5, 110.5)

    def setBrush(self, brush):
        self._brush = brush
        self.update()
        #self.repaint()

#В методе paint происходит непостредсвенное рисование обектов
# Причем в зависимости от значения глобальной переменной (флага) будет видны только оперделенные круги

    def paint(self, painter, option = None, style = None, widget = None):
        painter.setBrush(self._brush)
        if self.level_nested == 0:
            painter.drawEllipse(0, 0, 100, 100)
        if self.level_nested == 1:
            painter.drawEllipse(0, 0, 35, 35)

#Убери единичку, чтобы все заработало!!!
    def paint1(self, painter, option, widget):
        # painter.save()
        #print("Вызов метода paint")
        yellow = QtGui.QColor(245, 233, 77)
        red = QtGui.QColor(255, 127, 80)
        green = QtGui.QColor(197, 219, 50)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        if self.type_of_obj == "circle" and self.level_nested == 0:
            painter.setBrush(yellow)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.drawEllipse(0, 0, 100, 100)
           


        if self.type_of_obj == "circle" and self.level_nested == 1:
            painter.setPen(QtGui.QPen(QtCore.Qt.black))
            painter.setBrush(red)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.drawEllipse(0, 0, 35, 35)

    def onClicked(self):
        print("Сигнал сработал")
        #for item in self.scene.items(-200, -200, 0, 0):
        #    print(item)
        self.setBrush(QtGui.QColor("red"))

    def mousePressEvent(self, event):
        self.onClicked()




#ОСТАЛОСЬ ОТ МАСШТАБИРОВАНИЯ (продолжение старого painta
        # if self.type_of_obj == "circle" and self.level_nested == 0:
        #     painter.setBrush(yellow)
        #     painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #     painter.drawEllipse(0, 0, 100, 100)
        #
        # if globalScale > - 10:
        #     if self.type_of_obj == "circle" and self.level_nested == 1:
        #         painter.setPen(QtGui.QPen(QtCore.Qt.black))
        #         painter.setBrush(red)
        #         painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #         painter.drawEllipse(0, 0, 35, 35)
        #
        # # if globalScale <= -10:
        # #     if self.type_of_obj == "little":
        # #         selfb = "1"
        # #         font = QtGui.QFont("Times", 20)
        # #         painter.setFont(font)
        # #         painter.drawText(12, 15, self.b)
        #
        # if globalScale > 5:
        #     if self.type_of_obj == "circle" and self.level_nested == 2:
        #         painter.setPen(QtGui.QPen(QtCore.Qt.black))
        #         painter.setBrush(green)
        #         painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #         painter.drawEllipse(5, 5, 15, 15)
        #         #Смысл маштабирования был в том, о какой точки происходит машбабирование (какая точка задается в drawEllipse)
        #         # if globalScale > 7:
        #         #     painter.setPen(QtGui.QPen(QtCore.Qt.black))
        #         #     painter.setBrush(green)
        #         #     painter.drawEllipse
        #
        # #Это цифырки которые говорят о том сколько кругов сейчас
        # # if globalScale <= 5 and globalScale > -10:
        # #     self.b = "1"
        # #     if self.type_of_obj == "vlittle":
        # #         font = QtGui.QFont("Times", 7)
        # #         painter.setFont(font)
        # #         painter.drawText(10, 10, self.b)
        # # if globalScale > 7 and globalScale <= 25:
        # #     if self.type_of_obj == "vlittle":
        # #         font = QtGui.QFont("Times", 7)
        # #         painter.setFont(font)
        # #         painter.drawText(12, 15, self.b)
        #
        # if globalScale > 25:
        #     if self.type_of_obj == "circle" and self.level_nested == 3:
        #         painter.setPen(QtGui.QPen(QtCore.Qt.black))
        #         painter.setBrush(yellow)
        #         painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #         painter.drawEllipse(10, 10, 5, 5)
        #
        # if self.type_of_obj == "text":
        #     if self.level_nested == 0:
        #         if globalScale >-5:
        #             font = QtGui.QFont("Times", 11)
        #             painter.setFont(font)
        #             painter.drawText(QtCore.QRect(0, -12, 100, 12), QtCore.Qt.AlignCenter, self.msg)
        #             #painter.drawText(0, 0, self.msg)
        #     if self.level_nested == 1:
        #         if globalScale > 0 and globalScale < 25:
        #             font = QtGui.QFont("Times", 8)
        #             painter.setFont(font)
        #             painter.drawText(0, 0, self.msg)
        #
        #     if self.level_nested == 2:
        #         if globalScale > 5 and globalScale <= 30:
        #             font = QtGui.QFont("Times", 5)
        #             painter.setFont(font)
        #             painter.drawText(0, 10, self.msg)
        #
        #     if self.level_nested == 3:
        #         if globalScale > 25:
        #             font = QtGui.QFont("Times", 2)
        #             painter.setFont(font)
        #             painter.drawText(10, 17, self.msg)

        # else:
        #     pass
        # painter.restore()

#Рабочий метод для кругов отдельно
    #Но в данный момент не работает!
    # def wheelEvent(self, e):
    #     global mScale
    #     if int(e.delta()) > 0:
    #         mScale += 0.2
    #     else:
    #         mScale -= 0.2
    #     e.ignore()
    #     self.matrix = QtGui.QTransform()
    #     self.matrix.scale(mScale, mScale)
    #     self.setTransform(self.matrix, False)
    #     print(mScale)

# class QGraphicsItemGroup(QtWidgets.QGraphicsItemGroup):
#     def __init__(self, *args):
#         super().__init__(*args)
#
#     def mousePressEvent(self, event):
#         super().mousePressEvent(event)
#         self.setCursor(QtCore.Qt.ClosedHandCursor)
#
#     def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
#         super().mouseReleaseEvent(event)
#         self.setCursor(QtCore.Qt.OpenHandCursor)

class MyMainWindow(QtWidgets.QWidget):
    def __init__(self, dict_with_elem_con):
        super().__init__()
        self.dict_with_elem_conn = dict_with_elem_con
        self.initUI()


    def initUI(self):
        global globalScale
        print("initUI работает")
        self.zoom = 1
        self.group = QtWidgets.QGraphicsItemGroup()
        self.scene = QtWidgets.QGraphicsScene(-200, -200, 400, 400)

        self.len_dict = len(self.dict_with_elem_conn)
        l = [[15, 15], [55, 25], [30, 55]]

        self.ellipse = MyItem("circle", 0)
        # self.group.addToGroup(self.ellipse)
        self.ellipse.setPos(-175, -175)
        #self.ellipse.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.ellipse)

        self.ellipse2 = MyItem("circle", 1)
        # self.group.addToGroup(self.ellipse)
        self.ellipse2.setPos(-150, -150)
        #self.ellipse2.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.ellipse2)

        # self.ellipse = MyItem("circle", 1)
        # self.ellipse.setPos(-175, -175)
        # self.scene.addItem(self.ellipse)

        #  #КРУГ 2

        self.group2 = QtWidgets.QGraphicsItemGroup()
        self.ellipse2 = MyItem("circle", 0)


        self.group2.addToGroup(self.ellipse2)
        l = [[15, 15], [55, 25], [30, 55]]

        for i in range(3):
            self.ellipse2 = MyItem("circle", 1)
            self.ellipse2.setPos(l[i][0], l[i][1])
            self.group2.addToGroup(self.ellipse2)
            #self.text22 =
        self.group2.setPos(0, -175)
        self.group2.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.group2)



        #временно удрали для работы с нажатием!
        # # круг 1 новый
        # for key in self.dict_with_elem_conn.keys():
        #     #print("key =", key, "; value = ", self.dict_with_elem_conn[key])
        #     self.ellipse = MyItem("circle", 0) # типа создал круг главный
        #     self.group.addToGroup(self.ellipse)
        #     i = 0
        #     for value in self.dict_with_elem_conn[key]:
        #         self.ellipse = MyItem("circle", 1) #типа создал маленький круг
        #         self.ellipse.setPos(l[i][0], l[i][1])
        #         i = i + 1
        #         self.group.addToGroup(self.ellipse)
        # #self.group.setPos(-175, -175) #Убрал новый способ формирования круга для отладки исчезнавений
        # self.group.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        # #КРУГ 1
        #
        # self.group4 = QtWidgets.QGraphicsItemGroup()
        # #self.view = MyGraphicsView(self.scene)
        # #self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        # #self.view.setSceneRect(scene_rect)
        # self.scene.setBackgroundBrush(QtCore.Qt.white)
        # self.ellipse = MyItem("circle", 0)
        #
        # self.group4.addToGroup(self.ellipse)
        #
        #
        # l = [[15, 15], [55, 25], [30, 55]]
        # for i in range(3):
        #     self.ellipse = MyItem("circle", 1)
        #     self.ellipse.setPos(l[i][0], l[i][1])
        #     self.group4.addToGroup(self.ellipse)
        #
        # #if globalScale > 5:
        # for i in range(3):
        #     self.ellipse = MyItem("circle", 2)
        #     self.ellipse.setPos(l[i][0], l[i][1])
        #     self.group4.addToGroup(self.ellipse)
        #
        # for i in range(3):
        #     self.ellipse = MyItem("circle", 3)
        #     self.ellipse.setPos(l[i][0], l[i][1])
        #     self.group4.addToGroup(self.ellipse)
        # #self.group4.setPos(-175, -175) #УБРАЛ КРУГ 1
        # self.group4.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        # self.scene.addItem(self.group)


       #  #КРУГ 2
       #
       #  self.group2 = QtWidgets.QGraphicsItemGroup()
       #  self.ellipse2 = MyItem("circle", 0)
       #
       #
       #  self.group2.addToGroup(self.ellipse2)
       # #l = [[15, 15], [55, 25], [30, 55]]
       #
       #  for i in range(3):
       #      self.ellipse2 = MyItem("circle", 1)
       #      self.ellipse2.setPos(l[i][0], l[i][1])
       #      self.group2.addToGroup(self.ellipse2)
       #      #self.text22 =
       #  #self.group2.setPos(0, -175)
       #  self.group2.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
       #  self.scene.addItem(self.group2)

        # # КРУГ 3
        # self.c = ["Алмаз", "ГВМ 100/6", "ГВМ 100/6-410", "НСГН-203"]
        # self.c1 = ["Алмаз-1", "ГВМ 100/6-1", "ГВМ 100/6-410-1", "НСГН-203-1"]
        # self.c2 = ["ГВМ2", "ГВМ3", "ГВМ4", "ГВМ5"]
        # self.group3 = QtWidgets.QGraphicsItemGroup()
        #
        # self.ellipse3 = MyItem("circle", 0)
        # self.text22 = MyItem("text", 0, self.c[0])
        #
        # self.group3.addToGroup(self.ellipse3)
        # self.group3.addToGroup(self.text22)
        #
        # l = [[15, 15], [55, 25], [30, 55]]
        #
        # for i in range(3):
        #     self.ellipse3 = MyItem("circle", 1)
        #     self.ellipse3.setPos(l[i][0], l[i][1])
        #     self.group3.addToGroup(self.ellipse3)
        #     self.text22 = MyItem("text", 1, self.c[i+1])
        #     self.text22.setPos(l[i][0], l[i][1])
        #     self.group3.addToGroup(self.text22)
        #
        # # if globalScale > 5:
        # for i in range(3):
        #     self.ellipse3 = MyItem("circle", 2)
        #     self.ellipse3.setPos(l[i][0], l[i][1])
        #     self.group3.addToGroup(self.ellipse3)
        #     self.text22 = MyItem("text", 2, self.c1[i + 1])
        #     self.text22.setPos(l[i][0], l[i][1])
        #     self.group3.addToGroup(self.text22)
        #
        # for i in range(3):
        #     self.ellipse3 = MyItem("circle", 3)
        #     self.ellipse3.setPos(l[i][0], l[i][1])
        #     self.group3.addToGroup(self.ellipse3)
        #     self.text22 = MyItem("text", 3, self.c2[i + 1])
        #     self.text22.setPos(l[i][0], l[i][1])
        #     self.group3.addToGroup(self.text22)
        #
        # self.group3.setPos(0, 0)
        # self.group3.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        # #self.group3.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations) #игнорирует наследсвенные преобразования
        # self.scene.addItem(self.group3)



        #self.scene.addWidget(button)



        self.view = MyGraphicsView(self.scene, self)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        #self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setAlignment(QtCore.Qt.AlignCenter)
        self.view.setScene(self.scene)
        self.view.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.view.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.view.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.view.centerOn(0, 0)
        # self.view.setCursor(QtCore.Qt.OpenHandCursor)
        self.view.resize(900, 900)

        self.show()




def main(arguments):
    app = QtWidgets.QApplication(arguments)

    book = openpyxl.open('data.xlsx')
    sheet = book["data2"]

    data_connections = []

    for i in range(2, sheet.max_row + 1):
        for j in range(1, sheet.max_column):
            if sheet[i][j].value == 1:
                data_connections.append([i - 1, j])

    print(data_connections)

    dict_with_elem_conn = {}
    for i in data_connections:
        # если элемент  таким ключом уже есть в списке, то
        if i[1] in dict_with_elem_conn:
            (dict_with_elem_conn.get(i[1])).append(i[0])
        # если элемента еще нет, то создаем новый ключ, а в качесмве значения инициализируем пустой список
        else:
            dict_with_elem_conn[i[1]] = []
            dict_with_elem_conn[i[1]].append(i[0])

    print("dict_with_elem_conn = ", dict_with_elem_conn)

    # создали пересечения для обьявления всех элементов главных кругов и дополнительных кругов
    main_circles = set()  # перечисление внешних кругов
    additional_circles = set()  # перечисление внутренних кругов

    # перебираем все данные из list of conn и добавляем в перечисления для элементов главного круга и дополнительного
    for i in range(len(data_connections)):
        main_circles.add(data_connections[i][1])
        additional_circles.add(data_connections[i][0])

    print(dict_with_elem_conn)


    window = MyMainWindow(dict_with_elem_conn)
    window.setWindowTitle("Circles")
    window.setGeometry(450, 200, 800, 800)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)