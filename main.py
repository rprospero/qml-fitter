import sys
import numpy as np
from PySide6.QtCore import QObject, Signal, Property, Slot, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView, QQuickPaintedItem
from PySide6.QtGui import QImage, QPainter
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class Model(QObject):
    modelChanged = Signal()
    imageChanged = Signal()

    _slope = 1.0
    _intercept = 0.0
    _xrange = [-5.0, 5.0]
    _xs = []
    _ys = []
    _imageWidth = 1920
    _imageHeight = 1080

    def __init__(self):
        QObject.__init__(self)
        self._xs = np.linspace(self._xrange[0], self._xrange[1], 100)
        self._ys = self._xs *self._slope + self._intercept
        self.modelChanged.connect(self.imageChanged)

    @Property(float, notify=modelChanged)
    def slope(self):
        return self._slope

    @slope.setter
    def slope(self, val):
        self._slope = val
        self.modelChanged.emit()

    @Property(float, notify=modelChanged)
    def intercept(self):
        return self._intercept

    @intercept.setter
    def intercept(self, val):
        self._intercept = val
        self.modelChanged.emit()

    @Property(float, notify=modelChanged)
    def x_min(self):
        return self._xrange[0]

    @x_min.setter
    def x_min(self, val):
        self._xrange[0] = val
        self.modelChanged.emit()

    @Property(float, notify=modelChanged)
    def x_max(self):
        return self._xrange[1]

    @x_max.setter
    def x_max(self, val):
        self._xrange[1] = val
        self.modelChanged.emit()

    @Property(int)
    def imageWidth(self):
        return self._imageWidth

    @imageWidth.setter
    def imageWidth(self, width):
        self._imageWidth = width
        self.imageChanged.emit()

    @Property(int)
    def imageHeight(self):
        return self._imageHeight

    @imageHeight.setter
    def imageHeight(self, height):
        self._imageHeight = height
        self.imageChanged.emit()

    def calc(self):
        self._xs = np.linspace(self._xrange[0], self._xrange[1], 100)
        self._ys = self._xs *self._slope + self._intercept

    @Property(QImage, notify=imageChanged)
    def image(self):
        self.calc()

        width = self._imageWidth/100.0
        if self._imageWidth < 0:
            width = 0

        height = self._imageHeight/100.0
        if self._imageHeight < 0:
            height = 0

        fig = Figure(dpi=100, figsize=(width, height))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.plot(self._xs, self._ys)
        ax.set_title('test plot')
        canvas.draw()
        
        width, height = fig.figbbox.width, fig.figbbox.height
        return QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)

class LiveImage(QQuickPaintedItem):
    modelChanged = Signal()
    _image = None

    def __init__(self):
        QQuickPaintedItem.__init__(self)

    @Property(QImage, notify=modelChanged)
    def image(self):
        return self._image

    @image.setter
    def image(self, im):
        self._image = im
        self.update()

    def paint(self, painter : QPainter):
        if self._image is None:
            return
        painter.drawImage(QPoint(0, 0), self._image)

if __name__ == "__main__":
    app = QApplication()
    engine = QQmlApplicationEngine()
    qmlRegisterType(Model, "Tutorial", 1, 0, "Model")
    qmlRegisterType(LiveImage, "Tutorial", 1, 0, "LiveImage")

    engine.load('view.qml')

    app.exec()