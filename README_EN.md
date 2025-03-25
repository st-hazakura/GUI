# $$1\ Download\ QTDesigner $$

[Link to website](https://build-system.fman.io/qt-designer-download)

Open QTDesigner:

![image](https://github.com/user-attachments/assets/9c716acb-38c2-4037-90e0-28be6ac6b30c)

---

# $$ 2\ Overview of \ QTDesigner $$

In QTDesigner, we create the skeleton of our application.

Basic elements, we are going to use:

* Layout - for organizing of widgets:

  * Horizontal - widgets are placed in a row
  * GridLayout - widgets are placed in a grid
  * Next options, such as QFormLayout - useful for forms, e.g. name + mobile number...
* Line edit - field for text
* Label
* Combo box = dropdown
* QPushButton - button with text; QToolButton - button with a picture (icon)
* Line - line for separation of widgets (just visual element)
* ListWidget - list for QListWidgetItem items (specific tasks)

<img src="image\README\1.png" width="1000">

**!!!Save your .ui file into your working directory**

---

# $$ 3 \ VSCode, \ settings \ of \ environment. $$

`Terminal`:

```md
pip install pyqt5
```

Open the terminal using the shortcut $Ctrl+J$
-------------------------------------

### Two options for importing .ui into Python:

### 1. **Conversion** - it converts $.ui$ file into $.py$, which we can run.

The generated code describes the interface created in QTDesigner (placing of objects, their names and properties...)

**Pros**: Final app run faster (than the second option), because interpreter does not have to process the XML file each time.

**Cons**: Each time we change interface in QTDesigner, we have to convert it and rewrite our code.

`Terminal`

```md
python -m PyQt5.uic.pyuic -x qt_designer_file.ui -o your_file.py
```

### 2. Dynamic uploading of .ui - each time we run app, the actual $.ui$ file is uploaded. Library QT creates objects (buttons, labels ...)

**Pros**:

* We can change the interface in QTDesigner.
* Clear code.

**Cons**:

* We cannot add new widgets in our code.
* Widget's names cannot be changed in code, only in QTDesigner.

These cons are not problem for our app.

`app.py`

```py
from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("todo_app.ui", self)  


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
```

---

Let's import modules from library $PyQt$:

* $QtWidgets$ – it coinatins all widgets and basic components of UI
* $uic$ – module for uploading $.ui$ files
  Now we define class $MainWindow$, which inherits $QMainWindow$, so now it has a function of main window in Qt.

Let's define constructor:

* `super().init()` - It calls and initializes constructor of parent class $QMainWindow$, it allows to use its properties (e.g. styles of main window, attaching widget to main window ...)
* `uic.loadUi("todo_app.ui", self)` - method uploads $.ui$ file and automaticaly creates all widgets, which are now attributes of $MainWindow$ and connects to $self$.
* `QtWidgets.QApplication([])` - Creates main app, which manages events and run of the whole program.
* `window = MainWindow()` - Creates an instance of MainWindow.
* `app.exec_()` - It runs app in infinity loop, manages events(e.g. button click) and reacts on them. When we close the main window, exec_() ends.

---

# $$ 4\ Back\ into\ QTDesigneru $$

Widgets are now attributes of $MainWindow$ and we can access to them. How?

In QtDesigner we see, that each widget has 2 names:

1. Left - name of the instance (widget), which we can change .
2. Right - class of the widget.

We reference the widget using the name we provided and apply the method of the class to which the widget belongs.

So let's set appropriate names.

<img src="image\README\2.png" width="1000">

---

We can also add icons on the buttons from folder $Icons$.

Choose button, in $Property Editor$ → $QAbstractButton$ → $icon$.

<img src="image\README\4.png" width="500">

If you cannot find $PropertyEditor$ :

<img src="image\README\5.png" width="400">

The buttons are too little, we can change their size $Property Editor$ → $QAbstractButton$ → $iconSize$.

We can set this also in the code, we will show that in examples later, where we cannot use QTDesigner.

---

The wrapper around the icon can be removed in two ways:

1. In QTDesigneru v $PropertyEditor$ → $QToolButton$ → $autoRaise$.
2. In the code:

`app.py`

```py
        self.button_addtask.setAutoRaise(True)  
```

We can align labels of the colmuns: "To do", "Doing", "Done", in QTDesigner ($PropertyEditor$ → $QLabel$ → $alignment$) or in code:

```py
        self.label_done.setAlignment(QtCore.Qt.AlignCenter)
```

There are lots of properties we can set in QTDesigner or in the code. We will try to set most of it in QTDesigner and program the rest.

---

# $$ 5\ Start of\ coding $$

**Terminology:**

* Signal – a command called by the user
* Slot – a function that is executed afted receiving a signal

**Let's divide the code into two parts:**

1. Referencing the widgets and change their settings:
   * Visual changes (text alignment ...) (this can be usually done in QTDesigner)
   * Connecting signal of the widget to slot
2. Realization of functionality:
   * We define methods/slots of the $MainWindow$ class.

`app.py`

```py
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("todo_app.ui", self)  

        # 1
  
    # 2
```

---

# Button "button_addtask"

### **1. part Define signal**

1. Find assigned name in QTDesigner.
2. Reference that through self.
3. Define signal – `$clicked$`. We can find it in the class, which the widget belong to.
4. Connect signal to slot `$add_task$` using `$connect$`. So method/slot `$add_task$` is executed after receiving signal `$clicked$` (user clicked on a button)

`!!!` When you use a method as an argument (e.g. in connect()), remove brackets. Otherwise the program won't run.

We can connect signal to several slots - all of them will be executed after the signal is received.

```py
        #1
        self.button_addtask.clicked.connect(self.add_task)
```

### **2 part Realization of the method / slot.**

- In brackets of the method we write $self$, so it can access main window's atributes(widgets).

1. Reference the widget, which contain text of a task (class $QLineEdit$). Call a function of this class, which gets the text from the widget.
2. Use Python's function to remove spaces at the begining of the text.
3. Restrict addition of blank input - new function.
4. Add task into task list $QListWidget$:
   - Create an item of class $QListWidgetItem$ and add it into the list $addItem(item)$.
5. Clear the input line (method of the class $QLineEdit$)

```py
    #2  
    def add_task(self):
        text_taskinput = self.line_taskinput.text().strip()
  
        if text_taskinput == '':
            self.input_error("Error","Please write task")
        else: 
            self.list_todo.addItem(text_taskinput)
            self.line_taskinput.clear()
```

---

# $$ 6\ Dynamic\ window\ –\ method\ input\_error $$

`!` It is not possible to create dynamic elements in QTDesigner, so we are going to add it in code, using $QMessageBox$ from $QtWidgets$.

There are other dynamic elements, but we are not going to use them all in our program: *QFileDialog, QColorDialog, QFontDialog, QInputDialog*.

1) Make an instance of class $QMessageBox$.
2) We can set icon in two ways:

   1) Existing icons from $QMessageBox$.
   2) Our own icons using $QPixmap$.
3) The same goes to buttons. There are already existing buttons such as: $OK, Cancel, Yes, No$. We can set these through the method $setStandardButtons()$.

`*` During creating the instance of class $QMessageBox$ we add $self$ into the brackets. In that way, we say, that his parent class is $MainWindow$. $QMessageBox$ is now connected to $MainWindow$.

Dynamic window is connected to the main one, so it will display at the center of it.

```py
from PyQt5.QtGui import QPixmap

    #2
    def input_error(self, title, text):
        window_error = QtWidgets.QMessageBox(self)
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
```

$exec\_()$ – executes the dynamic window above the main one. Until we close it or push a button, we can't interact with the main window.

It's important to use $exec\_()$ instead of $exec()$, because $exec()$ is a Python's function. For QT we use $exec\_()$.
------------------------------------------------------------------------------------

# $$ 7\ Drag\ and\ Drop $$

There are to ways, how add drag and drop functionality between $QListWidgety$:

1. Settings in QTDesigner of each widget: $Property Editor$ → $QAbstractItemView$ → $dragDropMode$ → $DragDrop$.
2. In code.

In our app we use the first option. The second one is useful for specific requirements.

Now, the items will be copied, so we need to set them to move:
$Property Editor$ → $QAbstractItemView$ → $defaultDropAction$ → $MoveAction$.

There exist multiple parameters, which we can set, but this is good for now.

---

# $$ 8\ Visual\ part $$

We can use method $setStyleSheet()$ of class $QMainWindow$ to directly set visuals of widgets. But it's better to save them into external file and then upload them.

Let's create file `style.css` and upload it.

It is possible to write it in basic .txt file, but .css is prefered due to compatibility with PyQt.

```py
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("todo_app.ui", self)  

        with open("style.css", "r") as file:
            self.setStyleSheet(file.read())  
```

---

We access widgets in `style.css` through:

* Widget's name + #
* Class name

Each task list will has its own color - we access it through its name .

Visuals of the main window - access it through the name of its class.

`style.css`

```css
QMainWindow{
    background-color: #dee9ff;
}

#list_todo, #label_todo{
    background-color: #f7ffb0;
    border: 2px solid  #dae674;
    border-radius: 5px;
}

#list_doing, #label_doing{
    background-color: #c3f4ff;
    border: 2px solid #75cbdf;
    border-radius: 5px;
}

#list_done, #label_done{
    background-color: #9cffd2;
    border: 2px solid #66cb9e;
    border-radius: 5px;
}
```

---

Setting of font and size of text is easier in `style.css` too.

```css
QLabel, QComboBox, QLineEdit{
    font-family: Verdana, sans-serif;
    font-size: 15px;
}

QLineEdit {
    border: 2px solid #88C0D0;
    padding: 5px;
    border-radius: 5px;
}
```

---

We can see that between labels and columns with tasks are spaces.

So let's go into QTDesigner: Choose $QGridLayout$, go to $Property Editor$ and set parameter $layoutVerticalSpacing$ at 0.

---

# $$ 9\ Coding\ 2 $$


**We notice an error**, that occurs. When selecting an item in each of the widgets with our tasks (list_todo, list_doing, list_done), the items change to a different color.

When we select an item, its $isSelected$ property is set to $True$. Each of the three widgets can have one $selected$ item.

However, we want only one item to be selected at a time—the last one the user clicked on.

`*` This is not only for visual reasons; you will see why later.

To avoid defining a separate signal for each widget, we will create a list containing our task lists. We will add this list to the constructor so that we can access it easily.

```py
        #1
        self.list_widgets = [self.list_todo, self.list_doing, self.list_done] 
```

Next, we will iterate through the list and define a signal responsible for the action—$itemSelectionChanged$. We will then connect it to a slot/method—$change\_selection$—which will be triggered when the action is performed.

```py
        #1
        for widget in self.list_widgets:
            widget.itemSelectionChanged.connect(self.change_selection)
```

---

# Definition of slot:

In our $QListWidget$ widget, there is a $Focus$ property that determines whether the last user click was performed on this widget. The click does not have to be on an item—it is enough to click on an empty space.

Therefore, when the user moves an item, we will record which widget is currently active.

For all other widgets, we will set the $isSelected$ property to $False$.

```py
    #2
    def change_selection(self):
        fokus_widget = None
        for widget in self.list_widgets:
            if widget.hasFocus():
                fokus_widget = widget
                break
    
        for widget in self.list_widgets:
            if widget != fokus_widget:
                widget.clearSelection()   
```

---

# Delete Task Button

In the same way as before, we will define a slot and signal for the button used to delete a task.

```py
        #1
        self.button_deletetask.clicked.connect(self.delete_task)
```

Let's take a look what the function $currentRow()$ does.

```py
    #2
    def delete_task(self):
        for widget in self.list_widgets:
            row = widget.currentRow()
            print(row)
        print("\n")
```

We see that it returns the row index. If we run this function at the beginning (before adding any tasks), it returns -1. Why?

The answer is in QT Designer:
$Property Editor$ → $QListWidget$ → $currentRow$.

---

To remove an item, we can use a function that takes the row index as an argument.

```py
            widget.takeItem(row)
```

**Problem with $currentRow$**:

The $currentRow$ property stores the last selected item in the widget. Once we select an item, its index is saved, and we no longer get $-1$.

Therefore, we cannot use this approach in our application. However, if we had only one task list, this approach would be suitable.

We will extend the function with a new condition using the $selectedItems()$ function, which returns:

* An empty list [] if no item is $selected$.
* An object if a selected item exists.

```py
    #2
    def delete_task(self):
        for widget in self.list_widgets:
            if widget.selectedItems():
                row = widget.currentRow()
                widget.takeItem(row)
                break
```

Now you understand why we did one of the previous steps.

---

# Dynamic window for the delete button

Just like in the case of the $button\_addtask$, we will create a dynamic window.

We will also connect it to the main window using $self$ and use either a custom or a preset icon.

The first change – now we will use two preset buttons for confirming and rejecting the action.

The second change - `exec_()` not only opens the window but also returns a 'response code'—in other words, the pressed button. Therefore, we will return this response code.

```py
    #2
    def confirm_delete(self, title, text):
        window_confirm = QtWidgets.QMessageBox(self)
        window_confirm.setWindowTitle(title)
        window_confirm.setText(text)
  
        pixmap = QPixmap("Icons\\thinking_cat.png")  
        scale_pixmap = pixmap.scaled(90,90)
        window_confirm.setIconPixmap(scale_pixmap)
        window_confirm.setStandardButtons( QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        answer = window_confirm.exec_()
        return answer
```

We add this function to the slot and check the response code:

```py
    #2
    def delete_task(self):
        for widget in self.list_widgets:
            if widget.selectedItems():
                answer = self.confirm_delete("Confirm Delete", "Are you sure?")

                if answer == QtWidgets.QMessageBox.Yes:
                    row = widget.currentRow()
                    widget.takeItem(row)
                    break
```

---

# Main window icon

We can also set the main window icon in the constructor, simply using the appropriate method.

```py
from PyQt5 import QtGui


        #1
        self.setWindowIcon(QtGui.QIcon("Icons\\logo.png")) 
```

`*` Because the parent class for dynamic windows is $MainWindow$, the icons for these windows will be set automatically.

---

# $$ 10\ ComboBox $$

We would also like to assign an icon based on the task's importance. We have already predefined the items in QT Designer. We can set their icons either in QT Designer:

<img src="image\README\7.png" width="500">


or in the constructor using $setItemIcon(idx\_item, icon)$:

```py
        #1
        dropdown_images_path = ['Icons\\low.png','Icons\\medium.png','Icons\\high.png']   
        for i in range(self.dropdown_priority.count()):
            self.dropdown_priority.setItemIcon(i, QtGui.QIcon(dropdown_images_path[i]))  
```

---

However, we cannot set the size of the item icons in the ComboBox directly in QT Designer, so we will set it in the code.

```py
from PyQt5 import QtCore
  

        #1
        self.dropdown_priority.setIconSize(QtCore.QSize(30,10))
```

We want the icons to be displayed in the task list as well, so we will modify our $add\_task$ function.

1. We get the current index of the item in the dropdown using $currentIndex()$ and define the paths to the icons.
2. We manually create an item from the $QListWidgetItem$ class.
3. We create an icon and assign it to the item.

```py
    def add_task(self):
        text_taskinput = self.line_taskinput.text().strip()
        idx_item_dropdown = self.dropdown_priority.currentIndex()
        priority_icons_path = ['Icons\\low.png', 'Icons\\medium.png', 'Icons\\high.png']
  
        if text_taskinput == '':
            self.input_error("Error","Please write task")
        else: 
            item = QtWidgets.QListWidgetItem(text_taskinput)
            icon = QtGui.QIcon(priority_icons_path[idx_item_dropdown])
            item.setIcon(icon)
            self.list_todo.addItem(item)
  
            self.line_taskinput.clear()
```

We also don't like that the icons are small – we will increase their size in the task list.

```py
        #1
        for widget in self.list_widgets:
            widget.setIconSize(QtCore.QSize(40,40))
```

---

# $$ 11\ Visual\ part\ 2 $$


We would like to style the items in the $QListWidget$. QTDesigner doesn't allow us to do this, so we can use the first method – setting styles with CSS.

We could access them by class name, but each widget will have its own color. Therefore, we access them by the widget's name.

We will set the borders, border radius, and background color.

`style.css`

```css
#list_todo::item{
    border: 2px solid #dbe866;
    border-radius: 5px;
    background-color: #ecf690;
}

#list_doing::item{
    border: 2px solid #63c4da;
    border-radius: 5px;
    background-color: #ace3f0;
}

#list_done::item{
    border: 2px solid #59d79f;
    border-radius: 5px;
    background-color: #81edbd;
}
```

We can see that the default properties of the text field, such as font color or the color when an item is selected, are no longer predefined.

Therefore, we will redefine them and also set the color for the selected item.

Additionally, we will add padding.

```css
QListWidget::item{
    color: #000000;
    padding: 2px;
}

#list_todo::item:selected{
    background-color: #dbe866;
}

#list_doing::item:selected{
    background-color: #63c4da;
}

#list_done::item:selected{
    background-color: #59d79f;
}
```

---

# The second option (optional)

We can also set this in the code.
However, in the code, we cannot set borders, only the background color.

So, we will comment out what we just added in `style.css` and set up a signal that will trigger a slot when a new row appears in the widget.

```py
        #1
        for widget in self.list_widgets:
            widget.model().rowsInserted.connect(self.update_color_background)
```

## **Definition of signal:**

1. It accepts three arguments from the model:
   - `start` – the index of the position of the first added row,
   - `end` – the index of the last added row.
   - `parent` - eturns a $QModelIndex$ object, which we don’t need.

If only one row is added, then $start = end$.

2. `sender()` - the sender of the signal, from the $QAbstractItemModel$ class.

We get its parent, which is the widget into which the item was added:  `self.sender().parent()` returns the $QListWidget$ object.

3. We get the name of the widget into which the item was added and define colors based on its name.
4. We get the item itself from the widget by its index.
5. Due to some issues (which I couldn’t identify – probably because the item isn’t passed to the list in time), we can set the background only using an anonymous function.

```py
    #2
    def update_color_background(self, parent, start, end):
        sender_widget = self.sender().parent()
        name_widget = sender_widget.objectName()
        print(name_widget, start)
  
        color_map = {
            "list_todo": "#dae674",  
            "list_doing": "#75cbdf",  
            "list_done": "#66cb9e"  }
  
        item = sender_widget.item(start)
        QtCore.QTimer.singleShot(0, lambda: item.setBackground(QtGui.QColor(color_map[name_widget])))
```

`*` We can see, that the better method is through styles, as it provides more options for customization and easier access."

---

# $$ 12\ ComboBox\ 2\ -\ date $$

`QMessageBox` is intended only for icons, text, and buttons – it does not support widgets like a calendar, for example.

Therefore, we will use `QDialog`.

1. We create a window and a vertical layout.
2. We create a calendar widget and add it to the layout.
3. For $QDialog$, we have different predefined buttons that are located in $QDialogButtonBox$ – we select them and also add them to the layout.
4. We set the layout for $QDialog$ that we added the widgets to and open the window.

```py

    #2
    def select_date(self):
        dialog_window = QtWidgets.QDialog(self)
        layout = QtWidgets.QVBoxLayout()
  
        calendar = QtWidgets.QCalendarWidget()
        layout.addWidget(calendar)
  
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        layout.addWidget(buttons)
  
        dialog_window.setLayout(layout)
  
        dialog_window.exec_()
```

---

## **Modification of the $add\_task$ function**

UWe will modify the $add\_task$ function so that it reacts to the selected item index in the ComboBox.

We will add the item normally.

If the first item was selected in the ComboBox, we will pass the item to the dynamic window function and potentially modify it.

The $item$ is obtained from the input field $QLineEdit$, and since it changes with every task added, it is not suitable to store it as an attribute – instead, we pass it as an argument.

Also, objects are passed by reference. So when we add the $item$ to the list, we still have a reference to it, and changes made in the function $select\_date(item)$ will be reflected in the $list\_todo$ list.

```py
    #2
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
```

---

## **Slots for Buttons**

The predefined buttons $OK, Cancel$ have predefined signals:

* accepted
* rejected

We only need to write slots for them.

**Slot as a Local Function:**

* We define the slot inside $select\_date$ because $QDialog$ is not part of the main window (it is not defined in the constructor of $MainWindow$), and thus does not have direct access to the $QDialog$ widgets.
* Instead of storing objects from $QDialog$ in attributes, it is better to pass the required objects as arguments.

**Standard QDialog Methods**

* accept() – Closes the window and returns $QDialog.Accepted$ (we can use this for some condition, as in $delete_task$, but we don’t need it here)
* reject() – Closes the window and returns $QDialog.Rejected$, it just closes the window.

```py
    #2
    def select_date(self, item):
        # ...
        dialog_window.setLayout(layout)
        
        def add_date(calendar, dialog_window, item):
            selected_date = calendar.selectedDate().toString("yyyy-MM-dd")
            item.setText(f"{selected_date}  {item.text()}")
            dialog_window.accept()
```

**Signals**

For the signal when the $OK$ button is pressed, we assign the slot using a `lambda` function to prevent the function from being executed immediately. The slot will only be triggered when the action occurs.

We use this approach because we need to pass arguments to the slot.

```py
    #2
    def select_date(self, item):
        # ...
        def add_date(calendar, dialog_window, item):
            selected_date = calendar.selectedDate().toString("yyyy-MM-dd")
            item.setText(f"{selected_date}  {item.text()}")
            dialog_window.accept()
  
        buttons.accepted.connect(lambda: add_date(calendar, dialog_window, item))
        buttons.rejected.connect(dialog_window.reject)
  
        dialog_window.exec_()
```
