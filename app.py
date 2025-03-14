from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("todo_app.ui", self)  




app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()