from PyQt5 import QtCore, QtWidgets, QtGui
import sys, time, math, codecs, json



class MyItem(QtWidgets.QGraphicsItem):

    def __repr__(self):
        return "id = {}, name = {}, type = {}".format(self.id, self.name, self.circle_type)

    def __init__(self, id, circle_type, name, conn_id):
        super().__init__()
        self.id = id
        self.id_peretask = 0
        self.name = name
        self.circle_type = circle_type
        self.addText = 0
        self.flag_select = 0
        self.sam_text = ""
        self.flag_scene = 0
        self.conn_id = conn_id
        self._brush = QtGui.QBrush(QtCore.Qt.green)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        #self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)

        if self.circle_type == "big":
            self.setAcceptDrops(True)
            self.setAcceptHoverEvents(True)
            self._brush = QtGui.QBrush(QtGui.QColor(255, 255, 153))
            #self.rectF = QtCore.QRectF(-50, -50, 100, 100)
            self.rectF = QtCore.QRectF(-70, -70, 130, 130)

        if self.circle_type == "little":
            self._brush = QtGui.QBrush(QtGui.QColor(0, 255, 128))
            self.rectF = QtCore.QRectF(-18, -18, 35, 35)
            #self.rectF = QtCore.QRectF(-18, -18, 50, 35)

        if self.circle_type == "grand":
            self._brush = QtGui.QBrush(QtGui.QColor(255, 204, 153))
            # self.rectF = QtCore.QRectF(-50, -50, 100, 100)
            self.setAcceptDrops(True)
            self.setAcceptHoverEvents(True)
            self.rectF = QtCore.QRectF(-230, -230, 430, 430)


    def boundingRect(self):
        return self.rectF

    # def paint(self, painter, option=None, style=None, widget=None):
    #     print("hello")

    # метод для рисования текста
    def add_text(self, text):
        self.addText = 1
        self.text = text

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemSelectedChange:

            if value:
                #срабатывает когда происходит выделение какого либо круга
                self.flag_select = 1
                #self.scene().selectedIt.emit(self)
            else:
                self.flag_select = 0
        return QtWidgets.QGraphicsItem.itemChange(self, change, value)

        # переход на следующий уровень вложенности
    def mouseDoubleClickEvent(self, event):
        #print("mousePressEvent")
            # self.flag = 1
        time.sleep(0.5)
        self.scene().selectedIt.emit(self)  # создается сигнал

    def paint(self, painter, option=None, style=None, widget=None):

        # эти 2 условия используются для выделения круга
        # при нажатии на круг устванавливается фраг, а при вызове paint происходит перерисовка
        if self.flag_select == 0:
            painter.setPen(QtGui.QPen(QtCore.Qt.black))

        if self.flag_select == 1:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 4))

        if self.circle_type == "grand":
            painter.setBrush(self._brush)
            painter.drawEllipse(-200, -200, 400, 400)
            #добавляем текст
            if self.name:
                painter.setFont((QtGui.QFont("Verdana", 18)))
                if len(str(self.name)) >= 5:
                    painter.setFont((QtGui.QFont("Verdana", 14)))
                if len(str(self.name)) >= 10:
                    painter.setFont((QtGui.QFont("Verdana", 10)))
                # painter.drawText(-(len(str(self.name)))*5, 5, str(self.name))
                #print("big", self.name)
                painter.drawText(-len(str(self.name))*3.5, -175, str(self.name))

        #рисуем большой желтыйкруг
        if self.circle_type == "big":
            painter.setBrush(self._brush)
            painter.drawEllipse(-50, -50, 100, 100)
            #добавляем текст
            if self.name:
                painter.setFont((QtGui.QFont("Verdana", 14)))
                if len(str(self.name)) >= 5:
                    painter.setFont((QtGui.QFont("Verdana", 12)))
                if len(str(self.name)) >= 10:
                    painter.setFont((QtGui.QFont("Verdana", 8)))
                # painter.drawText(-(len(str(self.name)))*5, 5, str(self.name))
                #print("big", self.name)
                painter.drawText(-len(str(self.name))*3.5, -55, str(self.name))



        # рисуем маленький зеленый круг
        if self.circle_type == "little":
            painter.setBrush(self._brush)
            painter.drawEllipse(-18, -18, 35, 35)

            #добавляем текст
            if self.name:

                painter.setFont((QtGui.QFont("Verdana", 12)))
                if len(self.name) >= 5:
                    painter.setFont((QtGui.QFont("Verdana", 10)))

                    self.setToolTip(str(self.name))
                    self.sam_text = self.name[:4] + ".."
                else:
                    self.sam_text = self.name
                painter.drawText(-15, 5, str(self.sam_text))

    #метод реализации drag and drop
    def mouseMoveEvent(self, e):
        mime = QtCore.QMimeData() #создается обьект, в котором переносится информация при d"n"d
        mime.setText(str(self.id)) #id обьекта сохраняется в mime обьект
        #mime.setUrls([QtCore.QUrl("http://google.ru/")])
        #mime.setData('application/x-qt-windows-mime;value="name"', bytearray(str(self.name), encoding="utf-8"))
        drag = QtGui.QDrag(e.widget())
        drag.setMimeData(mime)

        #формируем картинку при перетаскивании
        pix = QtGui.QPixmap(250, 250)
        pix.fill(QtCore.Qt.white)
        painter = QtGui.QPainter(pix)
        #в зависимости от того, какой круг был выбран. происходит его рисование
        if self.circle_type == "little":
            painter.translate(20, 20) # сдвиг отностительно нуля было 20, 20
        if self.circle_type == "big":
            painter.translate(100, 100) #сдвига6емся относительно нуля
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.flag2 = 1
        self.paint(painter, 0, 0) #
        painter.end()
        pix.setMask(pix.createHeuristicMask()) #сглаживание квадрата куда вписан круг и текст
        drag.setPixmap(pix)
        #смещение точки относительно "центра хватания"
        if self.circle_type == "little":
            drag.setHotSpot(QtCore.QPoint(17, 17)) # было 17, 17
        if self.circle_type == "big":
            drag.setHotSpot(QtCore.QPoint(100, 100))  # было 17, 17
        dropAction = drag.exec(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction | QtCore.Qt.LinkAction, QtCore.Qt.LinkAction) #добавляем флагов для типа перемещения

        #self.setCursor(QtCore.Qt.ClosedHandCursor)

    #УБРАЛ ЧТОБЫ НЕ ПОЯВАЛЯЛАСЬ ОШИБКА
        #QtWidgets.QGraphicsItem.mouseMoveEvent(self, e)


    #метод который реализует сброс обьектов в круге
    def dropEvent(self, event: 'QGraphicsSceneDragDropEvent') -> None:
        print(event.mimeData().formats())
        print("dropEvent")
        self.id_peretask = event.mimeData().text()
        self.scene().newIT.emit(self)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            #self.hide()
            print(self.conn_id)
            self.scene().delobj.emit(self)


    def mouseDoubleClickEvent(self, event):
        print("mousePressEvent")
        #self.flag = 1
        time.sleep(0.5)
        self.scene().selectedIt.emit(self) #создается сигнал

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if event.button() == QtCore.Qt.RightButton:
            print("нажата права кнопка")
        else:
            super(MyItem, self).mousePressEvent(event)



