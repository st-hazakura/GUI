from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("todo_app.ui", self) 
        self.list_widgets = [self.list_todo, self.list_doing, self.list_done] 

        with open("style.css", "r") as file:
            self.setStyleSheet(file.read())  

        self.button_addtask.clicked.connect(self.add_task)
        self.button_deletetask.clicked.connect(self.delete_task)
        
        for widget in self.list_widgets:
            widget.itemSelectionChanged.connect(self.change_selection)
      
    def change_selection(self):
        fokus_widget = None
        for widget in self.list_widgets:
            if widget.hasFocus():
                fokus_widget = widget
                break
        for widget in self.list_widgets:
            if widget != fokus_widget:
                widget.clearSelection()   
    
            
    def add_task(self):
        line_taskinput = self.line_taskinput.text().strip()
        
        if line_taskinput == '':
            self.input_error("Error","Please write task")
        else: 
            self.list_todo.addItem(line_taskinput)
            self.line_taskinput.clear()
    

    def input_error(self, title, text):
        window_error = QtWidgets.QMessageBox(self)
        window_error.setWindowTitle(title)
        window_error.setText(text)
        
        # window_error.setIcon(QtWidgets.QMessageBox.Warning)
        pixmap = QPixmap("Icons\\error_2.png")  
        skale_pixmap = pixmap.scaled(90,90)
        window_error.setIconPixmap(skale_pixmap)  
        
        window_error.setStandardButtons(QtWidgets.QMessageBox.Ok)
        window_error.exec_()


    def delete_task(self):
        isselect_item = False
        for widget in self.list_widgets:
            if widget.selectedItems():
                answer = self.confirm_delete("Confirm Delete", "Are you sure?")

                if answer == QtWidgets.QMessageBox.Yes:
                    row = widget.currentRow()
                    widget.takeItem(row)
                    isselect_item = True
                    break
        
        if not isselect_item:
            self.input_error("Error", "Please select task")
                
    
    def confirm_delete(self, title, text):
        window_confirm = QtWidgets.QMessageBox(self)
        window_confirm.setWindowTitle(title)
        window_confirm.setText(text)
        
        #window_confirm.setIcon(QtWidgets.QMessageBox.Question)
        pixmap = QPixmap("Icons\\thinking_cat.png")        
        scale_pixmap = pixmap.scaled(90,90)
        window_confirm.setIconPixmap(scale_pixmap)
        window_confirm.setStandardButtons( QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        answer = window_confirm.exec_()
        return answer    
    

        

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()