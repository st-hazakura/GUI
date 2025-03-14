from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("todo_app.ui", self)  

        self.button_addtask.clicked.connect(self.add_task)
    
    
            
    def add_task(self):
        line_taskinput = self.line_taskinput.text().strip()
        
        if line_taskinput == '':
            self.input_error("Error","Please write task")
        else: 
            self.list_todo.addItem(line_taskinput)
            self.line_taskinput.clear()
    

    def input_error(self, title, text):
        window_error = QtWidgets.QMessageBox()
        window_error.setWindowTitle(title)
        window_error.setText(text)
        
        #1
        # window_error.setIcon(QtWidgets.QMessageBox.Warning)
        #2
        pixmap = QPixmap("Icons\\error_2.png")  
        skale_pixmap = pixmap.scaled(90,90)
        window_error.setIconPixmap(skale_pixmap)  
        
        window_error.setStandardButtons(QtWidgets.QMessageBox.Ok)
        window_error.exec_()
        

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()