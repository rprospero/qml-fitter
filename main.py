import sys
import numpy as np
from PySide6.QtCore import QObject, Signal, Property, Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType

class Model(QObject):
    modelChanged = Signal()

    m_slope = 0.0
    m_intercept = 0.0
    m_xrange = (-5.0, 5.0)

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
        print(val)
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

if __name__ == "__main__":
    app = QApplication()
    engine = QQmlApplicationEngine()
    model = Model()
    qmlRegisterType(Model, "Tutorial", 1, 0, "Model")

    ctx = engine.rootContext()
    engine.load('view.qml')

    app.exec()