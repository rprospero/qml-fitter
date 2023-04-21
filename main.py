import sys
import numpy as np
from PySide6.QtCore import QObject, Signal, Property, Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView, QQuickImageProvider
from PySide6.QtGui import QImage
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class Model(QObject):
    modelChanged = Signal()

    m_slope = 0.0
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

    @intercept.setter
    def x_min(self, val):
        self.m_xrange[0] = val
        self.modelChanged.emit()

    @Property(float, notify=modelChanged)
    def x_max(self):
        return self.m_xrange[1]

    @intercept.setter
    def x_max(self, val):
        self.m_xrange[1] = val
        self.modelChanged.emit()

    @Property(float, notify=modelChanged)
    def y_min(self):
        self.m_xs = np.linspace(self.m_xrange[0], self.m_xrange[1], 100)
        self.m_ys = self.m_xs *self.m_slope + self.m_intercept
        return np.min(self.m_ys)

    @Property(float, notify=modelChanged)
    def y_max(self):
        self.m_xs = np.linspace(self.m_xrange[0], self.m_xrange[1], 100)
        self.m_ys = self.m_xs *self.m_slope + self.m_intercept
        return np.max(self.m_ys)

    @Property(str, notify=modelChanged)
    def image(self):
        self.m_xs = np.linspace(self.m_xrange[0], self.m_xrange[1], 100)
        self.m_ys = self.m_xs *self.m_slope + self.m_intercept
        return "image://tutorialProvider/{}".format(np.random.rand())

class Provider(QQuickImageProvider):
    imageChanged = Signal()
    m_model = None

    def __init__(self, model):
        super(Provider, self).__init__(QQuickImageProvider.Image)
        self.m_model = model
        self.imageChanged.emit()

    def requestImage(self, id, size, requestedSize):
        print("id: ", id)
        print("size: ", size)
        print("requestedSize: ", requestedSize)

        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.plot(self.m_model.m_xs, self.m_model.m_ys)
        ax.set_title('test plot')
        canvas.draw()
        
        width, height = fig.figbbox.width, fig.figbbox.height
        return QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)

if __name__ == "__main__":
    app = QApplication()
    engine = QQmlApplicationEngine()
    model = Model()
    qmlRegisterType(Model, "Tutorial", 1, 0, "Model")

    provider = Provider(model)
    engine.addImageProvider("tutorialProvider", provider)

    engine.load('view.qml')

    app.exec()