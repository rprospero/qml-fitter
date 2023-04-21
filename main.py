import sys
import numpy as np
from PySide6.QtCore import QObject, Signal, Property, Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtQml import QQmlApplicationEngine

class Model(QObject):
    modelChanged = Signal()

    def __init__(self):
        QObject.__init__(self)
        self.m_slope = 0.0
        self.m_intercept = 0.0

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

    @Slot()
    def on_currentValueChanged(self):
        print(self.m_currentValue)

if __name__ == "__main__":
    app = QApplication()
    engine = QQmlApplicationEngine()
    model = Model()

    ctx = engine.rootContext()
    ctx.setContextProperty("Model", model)
    engine.load('view.qml')

    app.exec()