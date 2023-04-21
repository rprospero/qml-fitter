import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QApplication()
    engine = QQmlApplicationEngine("view.qml")
    app.exec()