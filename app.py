from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtGui import QPixmap

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("todo_app.ui", self) 

        with open("style.css", "r") as file:
            self.setStyleSheet(file.read())  
        
        self.setWindowIcon(QtGui.QIcon("Icons\\logo.png")) 
        self.dropdown_priority.setIconSize(QtCore.QSize(40,20))
        
        self.button_addtask.clicked.connect(self.add_task)
        self.button_deletetask.clicked.connect(self.delete_task)
        
        self.list_widgets = [self.list_todo, self.list_doing, self.list_done]  
        for widget in self.list_widgets:
            widget.setIconSize(QtCore.QSize(40,40))
            widget.itemSelectionChanged.connect(self.change_selection)
            # widget.model().rowsInserted.connect(self.update_color_background)
            
            
    # def update_color_background(self, parent, start, end):
    #     sender_widget = self.sender().parent()
    #     name_widget = sender_widget.objectName()
    #     # print(name_widget, start)
        
    #     color_map = {
    #         "list_todo": "#dae674",  
    #         "list_doing": "#75cbdf",  
    #         "list_done": "#66cb9e"  }
        
    #     item = sender_widget.item(start)
    #     QtCore.QTimer.singleShot(0, lambda: item.setBackground(QtGui.QColor(color_map[name_widget])))
            
        
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
        text_taskinput = self.line_taskinput.text().strip()
        idx_item_dropdown = self.dropdown_priority.currentIndex()
        priority_icons_path = ['Icons\\low.png', 'Icons\\medium.png', 'Icons\\high.png']
        
        idx_drop_box_date = self.dropdown_doto.currentIndex()
        
        if text_taskinput == '':
            self.input_error("Error","Please write task")
        
        else: 
            item = QtWidgets.QListWidgetItem(text_taskinput)
            icon = QtGui.QIcon(priority_icons_path[idx_item_dropdown])
            item.setIcon(icon)
            self.list_todo.addItem(item)
                
            if idx_drop_box_date == 1:
                self.select_date(item)
            
            self.line_taskinput.clear()                
                
    
    def select_date(self, item):
        dialog_window = QtWidgets.QDialog(self)
        layout = QtWidgets.QVBoxLayout()
        
        calendar = QtWidgets.QCalendarWidget()
        layout.addWidget(calendar)
        
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        dialog_window.setLayout(layout)
                
        def add_date(calendar, dialog_window, item):
            selected_date = calendar.selectedDate().toString("yyyy-MM-dd")
            item.setText(f"{selected_date}  {item.text()}")
            dialog_window.accept()
        
        buttons.accepted.connect(lambda: add_date(calendar, dialog_window, item))
        buttons.rejected.connect(dialog_window.reject)
        
        dialog_window.exec_()


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
        for widget in self.list_widgets:
            if widget.selectedItems():
                answer = self.confirm_delete("Confirm Delete", "Are you sure?")

                if answer == QtWidgets.QMessageBox.Yes:
                    row = widget.currentRow()
                    widget.takeItem(row)
                    break
                
    
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