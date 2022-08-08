from PyQt5 import QtCore, QtWidgets, QtGui
import sys, openpyxl, time, math, codecs, json
from PyQt5 import *
mScale = 0.5
globalScale = 0


# https://qtcentre.org/threads/67783-PyQt-zooming-with-QGraphicsSceneWheelEvent
# https://www.cyberforum.ru/qt/thread2229093.html
# https://stackoverflow.com/questions/40680065/qgraphicsscene-view-scale-understanding
# https://github.com/trufont/defconQt/blob/master/Lib/defconQt/controls/glyphLineView.py

#тут было реализован маштабирование представления
class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args):
        super().__init__(*args)


# ЕСЛИ В качесвтве аргумента указать "text", а затем уровень вложенности, а затем сам текст,
# ТО будет добавлена надпись определеноого уровня вложенности
class MyItem(QtWidgets.QGraphicsItem):
    global globalScale
    pen_width = 1.2

# конструктор класса MyItem
    def __init__(self, type_of_obj, level_nested, f, dict_obj_name):
        super().__init__()


        self.type_of_obj = type_of_obj  # тип обьекта
        self.level_nested = level_nested  # уровень вложенности (Желтый ил зеленый круг)
        self.id = f #id самого обьекта
        self.id2 = 0 #id обьекта родителя
        self.name = 0 #текстовое имя объекта
        print("init, id = {}".format(self.id))
        self.dict_obj_name = dict_obj_name #словарь обьект - id
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        if self.level_nested == 0:
            self.setAcceptDrops(True)
            self.setAcceptHoverEvents(True)

        # if self.level_nested == 1:
        #     self.setAcceptDrops(True)
        #     self.setAcceptHoverEvents(True)

        self.flag = 0
        self.flag2 = 0
        # задаем параметры рисования
        if self.level_nested == 0:
            self._brush = QtGui.QBrush(QtCore.Qt.yellow)
            self.rectF = QtCore.QRectF(-50, -50, 100, 100)
        if self.level_nested == 1:
            self._brush = QtGui.QBrush(QtCore.Qt.green)
            self.rectF = QtCore.QRectF(-18, -18, 35, 35)
    #задаем прямоугольник, в который будет вписвн круг
    def boundingRect(self):
        return self.rectF
    #используется для выделения круга
    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemSelectedChange:

            if value:
                #срабатывает когда происходит выделение какого либо круга
                self.flag = 1
                #self.scene().selectedIt.emit(self)
            else:
                self.flag = 0
        return QtWidgets.QGraphicsItem.itemChange(self, change, value)



    #переход на следующий уровень вложенности
    def mouseDoubleClickEvent(self, event):
        print("mousePressEvent")
        #self.flag = 1
        time.sleep(0.5)
        self.scene().selectedIt.emit(self) #создается сигнал

    #метод реализации drag and drop
    # def mouseMoveEvent(self, e):
    #     mime = QtCore.QMimeData() #создается обьект, в котором переносится информация при d"n"d
    #     mime.setText(str(self.id)) #id обьекта сохраняется в mime обьект
    #     #mime.setUrls([QtCore.QUrl("http://google.ru/")])
    #     #mime.setData('application/x-qt-windows-mime;value="name"', bytearray(str(self.name), encoding="utf-8"))
    #     drag = QtGui.QDrag(e.widget())
    #     drag.setMimeData(mime)
    #
    #     #формируем картинку при перетаскивании
    #     pix = QtGui.QPixmap(250, 250)
    #     pix.fill(QtCore.Qt.white)
    #     painter = QtGui.QPainter(pix)
    #     #в зависимости от того, какой круг был выбран. происходит его рисование
    #     if self.level_nested == 1:
    #         painter.translate(20, 20) # сдвиг отностительно нуля было 20, 20
    #     if self.level_nested == 0:
    #         painter.translate(100, 100) #сдвига6емся относительно нуля
    #     painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    #     self.flag2 = 1
    #     self.paint(painter, 0, 0) #
    #     painter.end()
    #     pix.setMask(pix.createHeuristicMask()) #сглаживание квадрата куда вписан круг и текст
    #     drag.setPixmap(pix)
    #     #смещение точки относительно "центра хватания"
    #     if self.level_nested == 1:
    #         drag.setHotSpot(QtCore.QPoint(17, 17)) # было 17, 17
    #     if self.level_nested == 0:
    #         drag.setHotSpot(QtCore.QPoint(100, 100))  # было 17, 17
    #     dropAction = drag.exec(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction | QtCore.Qt.LinkAction, QtCore.Qt.LinkAction) #добавляем флагов для типа перемещения
    #
    #     #self.setCursor(QtCore.Qt.ClosedHandCursor)
    #
    #     QtWidgets.QGraphicsItem.mouseMoveEvent(self, e)


    #метод который реализует сброс обьектов в круге
    def dropEvent(self, event: 'QGraphicsSceneDragDropEvent') -> None:
        print(event.mimeData().formats())
        print("dropEvent")
        self.id2 = event.mimeData().text()
        self.scene().newIT.emit(self)

    #метод для обработки нажатия на кнопку del
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            #self.hide()
            print(self.id)
            print(self.id2)
    # В методе paint происходит непостредсвенное рисование обектов
    # Причем в зависимости от значения глобальной переменной (флага) будет видны только оперделенные круги
    #метод отрисовки объекта класса MyItem
    def paint(self, painter, option=None, style=None, widget=None):
        painter.setBrush(self._brush)

        # эти 2 условия используются для выделения круга
        # при нажатии на круг устванавливается фраг, а при вызове paint происходит перерисовка
        if self.flag == 0:
            painter.setPen(QtGui.QPen(QtCore.Qt.black))

        if self.flag == 1:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 4))


            #return
        #рисуем большой желтый круг
        if self.level_nested == 0:
            painter.drawEllipse(-50, -50, 100, 100)
            if self.flag2 == 1:
                painter.setFont((QtGui.QFont("Verdana", 12)))
                if len(str(self.dict_obj_name[self.id])) >= 5:
                    painter.setFont((QtGui.QFont("Verdana", 14)))
                if len(str(self.id)) >= 10:
                    painter.setFont((QtGui.QFont("Verdana", 14)))
                #painter.drawText(-(len(str(self.name)))*5, 5, str(self.name))
                painter.drawText( -(len(str(self.dict_obj_name[self.id])))*5, 0, str(self.dict_obj_name[self.id]))
                self.flag2 = 0
        #рисуем маленький зеленый круг
        if self.level_nested == 1:
            painter.drawEllipse(-18, -18, 35, 35)
            # это условие применяется для рисования обьекта при d n d
            if self.flag2 == 1:
                painter.setFont((QtGui.QFont("Verdana", 12)))
                if len(str(self.dict_obj_name[self.id])) >= 5:
                    painter.setFont((QtGui.QFont("Verdana", 10)))
                if len(str(self.id)) >= 10:
                    painter.setFont((QtGui.QFont("Verdana", 8)))
                #painter.drawText(-(len(str(self.name)))*5, 5, str(self.name))
                painter.drawText( -15, 5, str(self.dict_obj_name[self.id]))
                self.flag2 = 0



#нужно для вывода снизу в статус баре
#также переопределили сигналы сцены для того, чтобы перебросить обьекты из itema в mainwindow
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
    def __init__(self, dicti, dicti2):
        super().__init__()
        self.dict_with_elem_conn = dicti
        self.dict_obj_name = dicti2
        self.message = " "
        #QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        #self.scene = QtWidgets.QGraphicsScene()
        self.scene = Scene()
        self.initUI()
        self.scene.setSceneRect(-300, -300, 600, 600)
        self.view = QtWidgets.QGraphicsView()
        self.setCentralWidget(self.view)

        #пробрасывем сигналы
        self.scene.selectedIt.connect(self.handleSelectIt)
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


    # метод который вызывается при d'n'd
    def newItem(self, item):
        print("item1 =", item.id) #ЭТО ИМЯ ОБЬЕКТА НА КОТОРОЕ ПЕРЕМЕШАЕТСЯ ОБЬЕКТ
        print("item2 =", item.id2)  # ЭТО ИМЯ ОБЬЕКТА НА КОТОРОЕ ПЕРЕМЕШАЕТСЯ ОБЬЕКТ
        #проверка, является ли перетасвиваемый обьект файлом (из проводника папка или файл)
        if item.id2.startswith("file"):
            print("файл!")
            print(item.id2.split("/"))
            #item.id2 = item.id2.split("/")[-1]
            item.name = item.id2.split("/")[-1] #убираем полный абсолютный путь, оставляем только название файла
            item.id2 = len(self.dict_obj_name) #присваиваем новому обьекту id
            self.dict_obj_name[item.id2] = item.name #добавляем name -id в соответсвующую стурктуру
            #print("новый словарь", self.dict_obj_name)
        if int(item.id) != int(item.id2): #проверяем, не являются ли обьекты одинаковыми
            if int(item.id2) not in self.dict_with_elem_conn.get(item.id): #защита от двойного добавления обьектов
                self.dict_with_elem_conn.get(item.id).append(int(item.id2)) #добавляем обьект в словарь
                #print("здесь мы помняли словарь", self.dict_with_elem_conn)
                self.initUI() #вызываем перерисовку ui

        #print("newItem")
        self.newJsonObject() #вызываем процедуру создания нового json файла исходя из словаря

    #метод, с помощью которого будет осущесвляться создание нового файла с обьектами в json
    def newJsonObject(self):
        print("new Json object")

        with open("object_base2.json", 'w', encoding="utf8") as file_objects:
            # считали данные из открвтого файла
            data = []
            #формируем словарь для json
            for key in self.dict_obj_name:
                data2 = {}
                data2["obj_id"] = int(key)
                data2["obj_name"] = self.dict_obj_name[key]
                data2["obj_image"] = {"type": "circle", "params": {"x": 0, "y": 0, "radius":100} }
                data2["obj_description"] = "Группа изделия разрабатываемых для ПАО НПО Алмаз"

                data.append(data2)

            # сохраняем данные в json
            data_objects = json.dump(data, file_objects, ensure_ascii=False, indent=4)
        data = []

        #формируем новый json файл со связями
        with open("connections_base2.json", 'w', encoding="utf8") as file_conn:
            data = []
            i = 0
            for key in self.dict_with_elem_conn:
                data2 = {}
                for val in self.dict_with_elem_conn[key]:
                    data2 = {}
                    conn = []
                    conn.append(val)
                    conn.append(key)
                    data2["connection_id"] = int(i)
                    data2["connection_type"] = "additive"
                    data2["connection_ids"] = conn
                    data2["connection_description"] = "Изделие ГВМ100/6-410 проходит по тематике ПАО НПО Алмаз"
                    data.append(data2)
                    i = i + 1
            data_objects = json.dump(data, file_conn, ensure_ascii=False, indent=4)

    #метод отрисовки интерфейса
    def initUI(self, flag = -1):

        #все объекты, рисуем все круги
        if flag == -1:

            #используется для метоположения обьектов
            self.locationX = -150
            self.locationY = -100

            #в качестве ключей выступают желтые "родительские" круги
            for key in self.dict_with_elem_conn.keys():
                #print("key =", key)
                #создаем желтвй круг
                #аргументы circle - тип объекта
                #0 - уровень (0 - желтый, 1 - зеленый)
                #key - id куга
                #dict_obj_name - словарь id - имя для отрисовка d'n'd
                self.ellipseMAIN = MyItem("circle", 0, key, self.dict_obj_name)
                self.ellipseMAIN.setPos(self.locationX, self.locationY)
                #формируем тескт надписи
                self.text = QtWidgets.QGraphicsSimpleTextItem()
                #сам текст надписи берется из словаря путем подстанвки в него id
                self.text.setText(str(self.dict_obj_name[key]))
                #считаем длину строки для позиционирования объекта
                len_key = len(str(self.dict_obj_name[key]))
                self.text.setFont(QtGui.QFont("Verdana", 14))
                self.text.setPos(-(len_key)*5, -75)
                self.text.setParentItem(self.ellipseMAIN)
                # изменяем позицианирование объекта
                if self.locationX < 250:
                    self.locationX = self.locationX + 150

                if self.locationX > 250:
                    self.locationX = -150
                    self.locationY = self.locationY + 150
                # for value in self.dict_with_elem_conn[key]:
                #     print("value = ", value)
                #расчитываем количество дочерних кругов
                count = len(self.dict_with_elem_conn[key])
                R = 30 # фиксируем радиус
                l = [] #список для координат
                if count == 1:
                    l = [[0, 0], []]
                if count > 1:
                    angle = math.radians((360 / count))
                    #заполняем список координат используя алгоритм
                    for i in range(count):
                        x = R * math.cos(i * angle)

                        y = R * math.sin(i * angle)

                        l.append([x, y])
                #print("l =", l)
                #создаем дочкерние объекты
                for i in range(len(self.dict_with_elem_conn[key])):
                    self.ellipse = MyItem("circle", 1, self.dict_with_elem_conn[key][i], self.dict_obj_name) #здесь используем object_id
                    self.ellipse.setPos(l[i][0], l[i][1])
                    self.ellipse.setParentItem(self.ellipseMAIN)
                    self.text = QtWidgets.QGraphicsSimpleTextItem()
                    sam_text = str(self.dict_obj_name[self.dict_with_elem_conn[key][i]])
                    len_sam_text = len(sam_text)
                    #print(len(sam_text))
                    self.text.setText(sam_text)
                    #print(len_sam_text)
                    self.text.setFont(QtGui.QFont("Verdana", 10))
                    #если длина надписи больше 5, то формируем короткую версию, а длинная через setTip
                    if len_sam_text > 5:
                        self.text.setToolTip(str(sam_text))
                        self.text.setFont(QtGui.QFont("Verdana", 8))
                        sam_text = sam_text[:4] + ".."
                        self.text.setText(sam_text)

                    self.text.setPos( -17, -10)
                    self.text.setParentItem(self.ellipse)

                self.scene.addItem(self.ellipseMAIN)
            #print(self.ellipseMAIN.childrenBoundingRect())

        # Эта ветка использвется при нажатии на какой либбо круг
        #через флаг передается id обьекта который был нажат
        if flag != -1:
            key = flag
            #values = self.dict_with_elem_conn[key]
            self.ellipseMAIN = MyItem("circle", 0, key, self.dict_obj_name)
            self.ellipseMAIN.setPos(0, 0)
            self.text = QtWidgets.QGraphicsSimpleTextItem()
            self.text.setText(str(self.dict_obj_name[key]))
            len_key = len(str(self.dict_obj_name[key]))
            self.text.setFont(QtGui.QFont("Verdana", 14))
            self.text.setPos(-(len_key) * 5, -75)

            self.text.setParentItem(self.ellipseMAIN)
            length = self.dict_with_elem_conn.get(key)

            count = len(length)
            R = 30
            l = []
            if count == 1:
                l = [[0, 0], []]
            #if length == 2:
            if count > 1:
                angle = math.radians((360 / count))
                # angle = 360 * math.pi / count
                # angle2 = angle * math.pi / 180
                for i in range(count):
                    x = R * math.cos(i * angle)
                    y = R * math.sin(i * angle)
                    l.append([x, y])

                #l = [[-15, -15], [20, 25]]
            # if length == 3:
            #     l = [[-15, -15], [25, 0], [-5, 25]]
            for i in range(len(self.dict_with_elem_conn[key])):
                self.ellipse = MyItem("circle", 1, self.dict_with_elem_conn[key][i], self.dict_obj_name)
                self.ellipse.setPos(l[i][0], l[i][1])
                self.ellipse.setParentItem(self.ellipseMAIN)
                self.text = QtWidgets.QGraphicsSimpleTextItem()
                #self.text.setText(str(self.dict_with_elem_conn[key][i]))
                #self.text.setFont(QtGui.QFont("Verdana", 12))
                sam_text = str(self.dict_obj_name[self.dict_with_elem_conn[key][i]])
                print("sam-text =", sam_text)
                self.text.setText(sam_text)
                len_sam_text = len(sam_text)
                self.text.setFont(QtGui.QFont("Verdana", 10))
                if len_sam_text > 5:
                    self.text.setToolTip(str(sam_text))
                    self.text.setFont(QtGui.QFont("Verdana", 8))
                    sam_text = sam_text[:4] + ".."
                    self.text.setText(sam_text)

                self.text.setPos(-17, -10)
                self.text.setParentItem(self.ellipse)
                self.scene.addItem(self.ellipseMAIN)

                #print("value = ", self.dict_with_elem_conn[key])


    #здесь обрабатывается нажатие на круг
    def handleSelectIt(self, item):
        print("здесь мы проверили словарь", self.dict_with_elem_conn)
        print("item.id =", item.id)

        if self.dict_with_elem_conn.get(item.id):
            #чистим сцену
            self.scene.clear()
            print("сработало")
            print("item.name = ", item.id)
            #форимируем строку в статус баре, что было нажато
            if self.message == " ":
                self.message = str(item.id)
            else:
                self.message = self.message + "->" + str(item.id)
            self.statusBar().showMessage(self.message) #отображаем инфу в статус баре
            self.initUI(item.id) #вызываем метод перерисовки
            #return 0

#функция main в которой происходит обработка данных из json в объекты python
def main(arguments):
    app = QtWidgets.QApplication(arguments)



    # открвли файл для работы с данными
    with open("object_base.json", encoding="utf8") as file_objects:
        # считали данные из открвтого файла
        data_objects = json.load(file_objects)

    # открвли второй файл для работы с данными
    with open("connections_base.json", encoding="utf8") as file_connections:
        # считали данные из открвтого файла
        data_conn = json.load(file_connections)

    # print(data_objects[2]["obj_image"]["type"])

    # парсим данные из connections_base.json
    # выделили данные, которые отностятся к connections_ids
    # (по ключу "connections_ids")
    list_of_conn = []
    for i in data_conn:
        list_of_conn.append(i["connection_ids"])

    print(list_of_conn)

    object_id = []
    object_name = []

    # парсим данные из object_base.json
    # создается списки с обьектами id объектов и имена объектов
    for j in data_objects:
        object_id.append(j["obj_id"])
        object_name.append(j["obj_name"])
    # создали списки с id обьекта (а) и с именем обьекта (b)
    # соеденили списки id обьектов и имена обьектов в один словарь
    dict_obj_name = dict(zip(object_id, object_name))  # сть словарь: id и название

    print(dict_obj_name)

    # создали пересечения для обьявления всех элементов главных кругов и дополнительных кругов
    main_circles = set()  # перечисление внешних кругов
    additional_circles = set()  # перечисление внутренних кругов

    # перебираем все данные из list of conn и добавляем в перечисления для элементов главного круга и дополнительного
    for i in range(len(list_of_conn)):
        main_circles.add(list_of_conn[i][1])
        additional_circles.add(list_of_conn[i][0])
        # list_of_conn2[i][0] = dict_obj_name.get(list_of_conn[i][0])
        # list_of_conn2[i][1] = dict_obj_name.get(list_of_conn[i][1])

    a = []
    b = []

    # перечисляем все элементы, которые могут быть
    for i in additional_circles:
        a.append(dict_obj_name.get(i))
    for j in main_circles:
        b.append(dict_obj_name.get(j))
    print("a =", a)
    print("b = ", b)

    dict_with_elem_conn = {}
    m = 0
    print(list_of_conn)
    # ФОРМИРУЕМ СЛОВАРЬ, ГДЕ В КАЧЕСВЕ КЛЮЧА используется главный элемент, а в качесве значения список вклобчаемых элементов
    for i in list_of_conn:
        if i[1] in dict_with_elem_conn:
            (dict_with_elem_conn.get(i[1])).append(i[0])
        else:
            dict_with_elem_conn[i[1]] = []
            dict_with_elem_conn[i[1]].append(i[0])
    print("dict_with_elem_conn = ", dict_with_elem_conn)

    window = MyMainWindow(dict_with_elem_conn, dict_obj_name)
    window.setWindowTitle("Circles")
    window.setGeometry(450, 200, 600, 600)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)