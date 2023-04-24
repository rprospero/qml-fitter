import sys
import numpy as np
from PySide6.QtCore import QObject, Signal, Property, Slot, QRect
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView, QQuickPaintedItem
from PySide6.QtGui import QImage, QPainter
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class Model(QObject):
    modelChanged = Signal()

    m_slope = 1.0
    m_intercept = 0.0
    m_xrange = [-5.0, 5.0]
    m_xs = []
    m_ys = []

    def __init__(self):
        QObject.__init__(self)
        self.m_xs = np.linspace(self.m_xrange[0], self.m_xrange[1], 100)
        self.m_ys = self.m_xs *self.m_slope + self.m_intercept

    @Property(float, notify=modelChanged)
    def slope(self):
        return self.m_slope

    @slope.setter
    def slope(self, val):
        self.m_slope = val
        self.modelChanged.emit()

    @Property(float, notify=modelChanged)
    def intercept(self):
        return self.m_intercept

    @intercept.setter
    def intercept(self, val):
        self.m_intercept = val
        self.modelChanged.emit()

    @Property(float, notify=modelChanged)
    def x_min(self):
        return self.m_xrange[0]

    @x_min.setter
    def x_min(self, val):
        self.m_xrange[0] = val
        self.modelChanged.emit()

    @Property(float, notify=modelChanged)
    def x_max(self):
        return self.m_xrange[1]

    @x_max.setter
    def x_max(self, val):
        self.m_xrange[1] = val
        self.modelChanged.emit()

    def calc(self):
        self.m_xs = np.linspace(self.m_xrange[0], self.m_xrange[1], 100)
        self.m_ys = self.m_xs *self.m_slope + self.m_intercept

    @Property(float, notify=modelChanged)
    def y_min(self):
        self.calc()
        return np.min(self.m_ys)

    @Property(float, notify=modelChanged)
    def y_max(self):
        self.calc()
        return np.max(self.m_ys)

class GraphImage(QQuickPaintedItem):
    modelChanged = Signal()
    m_model = None

    def __init__(self):
        QQuickPaintedItem.__init__(self)

    @Property(Model, notify=modelChanged)
    def model(self):
        return self.m_model

    @model.setter
    def model(self, m):
        self.m_model = m
        self.modelChanged.emit()

    def paint(self, painter : QPainter):
        # size = bounding_rect()
        # print("size: ", size)
        self.model.calc()

        fig = Figure(figsize=(self.width()/100.0, self.height()/100.0), dpi=100)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.plot(self.m_model.m_xs, self.m_model.m_ys)
        ax.set_title('test plot')
        canvas.draw()
        
        width, height = fig.figbbox.width, fig.figbbox.height
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
        painter.drawImage(QRect(0, 0, width, height), image)

if __name__ == "__main__":
    app = QApplication()
    engine = QQmlApplicationEngine()
    qmlRegisterType(Model, "Tutorial", 1, 0, "Model")
    qmlRegisterType(GraphImage, "Tutorial", 1, 0, "GraphImage")

    engine.load('view.qml')

    app.exec()