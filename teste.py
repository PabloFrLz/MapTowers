from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QApplication([])
    engine = QQmlApplicationEngine()
    engine.load("example3.qml")

    app.exec()
