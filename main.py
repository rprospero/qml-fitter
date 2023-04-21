import sys
from PySide6.QtCore import QObject, Signal, Property, Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtQml import QQmlApplicationEngine

class Model(QObject):
    currentValueChanged = Signal()

    def __init__(self):
        QObject.__init__(self)
        self.m_currentValue = 0.0
        self.currentValueChanged.connect(self.on_currentValueChanged)

    @Property(float, notify=currentValueChanged)
    def currentValue(self):
        return self.m_currentValue

    @currentValue.setter
    def setCurrentValue(self, val):
        if self.m_currentValue == val:
            return
        self.m_currentValue = val
        self.currentValueChanged.emit()

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