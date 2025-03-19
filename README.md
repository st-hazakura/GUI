# $$1\ Stazeni\ QTDesigner$$

[Stáhnout na webu](https://build-system.fman.io/qt-designer-download)

Otevřte QTDesigner:

![image](https://github.com/user-attachments/assets/9c716acb-38c2-4037-90e0-28be6ac6b30c)

---

# $$2\ Rozebrání\ QTDesigner$$

V Designeru děláme kostru aplikace.

Základní elementy, se kterými budeme pracovat:

* Layout: sem umístíme widgety:

  * Horizontální - widgety jsou umístěné do řádku, při posouvání jednoho se posunou i další.
  * GrindLayout - widgety jsou umístěné do řádku a sloupců.
  * A další layouty, jako QFormLayout - dobrý pro formuláře, jako je jméno a telefonní číslo atd.
* Line edit - pole používané pro zadávání textu
* Label
* Combo box - můžeme říci dropdown
* QPushButton - obecná tlačítka, pouze text a/nebo QToolButton - vlastní ikonka.
* Line - oddělovací čára, jenom pro vizuální oddělování
* ListWidget - každý úkol uvnitř je jiný element QListWidgetItem

<img src="image\README\1.png" width="1000">

**!!! Uložte si to do složky, kde budeme pracovat.**

---

# $$3\ VSCode,\ příprava\ prostředí.$$

`Terminál`:

```md
pip install pyqt5
```

Chcete-li otevřít terminál, stiskněte klávesovou zkratku $Ctrl+J$

---

### Import do Pythonu dvěma způsoby:

### 1. **Konverze** - převádí soubor $.ui$ do $.py$, který můžeme spustit.

`Terminál`

```md
python -m PyQt5.uic.pyuic -x qt_designer_file.ui -o your_file.py
```

### 2. Dynamické načítání .ui - při spuštění programu se bere aktuální $.ui$ soubor. QT samo vytváří objekty (tlačítka, labely atd.).

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

Moduly:

* $QtWidgets$ – obsahuje všechny widgety a základní komponenty uživatelského rozhraní.
* $uic$ – modul pro načítání $.ui$ souborů vytvořených v Qt Designeru.

Konstruktor:

* `uic.loadUi("todo_app.ui", self)` - metoda načte $.ui$ soubor a automaticky vytvoří všechny widgety podle návrhu. 
* `QtWidgets.QApplication([])` - Vytvoří hlavní aplikaci, která spravuje události a běh celého programu.
* `window = MainWindow()` - Instanci hlavního okna
* `app.exec_()` - spouští aplikace v nekonečném cyklu.

---

# $$4\ Návrat\ do\ QTDesigneru$$

1. Vlevo - jméno objektu, které si můžeme nastavit.
2. Vpravo - třída widgetu

<img src="image\README\2.png" width="500">

---

Přiřadíme ikonky našim tlačítkům ze složky $Icons$. Vybereme tlačítko, v $Property Editor$ → $QAbstractButton$ → $icon$.

<img src="image\README\4.png" width="500">

Pokud nemůžete najít $PropertyEditor$ :

<img src="image\README\5.png" width="400">

Změnit velikost tlačítek $Property Editor$ → $QAbstractButton$ → $iconSize$.

---

Zbavit se obálky kolem ikonky dvěma způsoby:

1. V QTDesigneru v $PropertyEditor$ → $QToolButton$ → $autoRaise$.
2. Nastavit v programu:

`app.py`

```py
        self.button_addtask.setAutoRaise(True)  
```

Zarovnat sloupce buď v QTDesigneru ($PropertyEditor$ → $QLabel$ → $alignment$) 
<img src="image\README\6.png" width="600">

nebo v kódu:

```py
        self.label_done.setAlignment(QtCore.Qt.AlignCenter)
```

---

# $$5\ Začátek\ kódování$$

**Terminologie:**

* Signál – je akce, která se vykonala.
* Slot – funkce, která se spustí poté, co obdrží signál.

**Rozdělíme kód na dvě části, kam budeme psát:**

1. Odkazování na widgety a změna jejich nastavení
2. Realizace funkcionality aplikace / sloty:


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

# Tlačítko "button_addtask"

### **1 čast Nastavení akce**
Odkážeme se na widget pomocí - `self`

Signal – `$clicked$`.

Slot - `$add_task$` připojíme pomocí `$connect$`. 

`!!!` Předáváme metodu/signál bez závorek.


```py
        #1
        self.button_addtask.clicked.connect(self.add_task)
```

### **2 čast Realizace metody / slotu.**



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

# $$6\ Dynamické\ okno\ –\ metoda\ input\_error$$

Dynamické elementy: *QMessageBox, QDialog, QFileDialog, QColorDialog, QFontDialog, QInputDialog*.

* Dva způsoby nastavení ikony:
   1) Přednastavené ikony z $QMessageBox$.
   2) Vlastní ikony pomocí $QPixmap$.
* Přednastavené tlačítka nastavujeme pomocí metody $setStandardButtons()$

* Dynamické okno se připojí k hlavnímu oknu pomocí `self` - $QtWidgets.QMessageBox(self)$

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

Používáme $exec\_()$ v PyQT5.

---

# $$7\ Drag\ and\ Drop$$

Dag and drop mezi $QListWidgety$:

$Property Editor$ → $QAbstractItemView$ → $dragDropMode$ → $DragDrop$.

$Property Editor$ → $QAbstractItemView$ → $defaultDropAction$ → $MoveAction$.

---

# $$8\ Vizuální\ část$$

$QMainWindow$ - `setStyleSheet()` nastavení vizuální částí widgetů. 

Vytvoříme soubor `style.css` a načteme ho.

```py
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("todo_app.ui", self)  

        with open("style.css", "r") as file:
            self.setStyleSheet(file.read())  
```

---

V souboru `style.css` k widgetům přistupujeme pomocí:

* Názvu widgetu přes #.
* Názvu třídy.

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

Nastavovení stylu textu, rozměry apod.

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


V QT Designeru: Vybereme $QGridLayout$ -> $Property Editor$ parametr $layoutVerticalSpacing$ -> 0.

---

# $$9\ Kódování\ 2$$

**Chyba** - Každý ze tří widgetů může má $selected$ item.

Vytvoříme seznam widgetů $QListWidget$.

```py
        #1
        self.list_widgets = [self.list_todo, self.list_doing, self.list_done] 
```

Signál – $itemSelectionChanged$, a slot – $change\_selection$.

```py
        #1
        for widget in self.list_widgets:
            widget.itemSelectionChanged.connect(self.change_selection)
```

---

# Definice slotu:

$QListWidget$ $Fokus$, zda uživatel v tomto widgetu. 

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

# Tlačítko pro odstranění úkolu

```py
        #1
        self.button_deletetask.clicked.connect(self.delete_task)
```

`currentRow()` - vrací index řádku. 

```py
    #2
    def delete_task(self):
        for widget in self.list_widgets:
            row = widget.currentRow()
            print(row)
        print("\n")
```


`takeItem(idx)` odstranění položky/itemu.

```py
            widget.takeItem(row)
```

`selectedItems()` vrací [objekt], v objektu jsou itemy s $isSelected = True$  :

```py
    #2
    def delete_task(self):
        for widget in self.list_widgets:
            if widget.selectedItems():
                row = widget.currentRow()
                widget.takeItem(row)
                break
```


# Dynamické okno pro tlačítko odstranění

`exec_()` nejenže spustí okno, ale také vrací "kód odpovědi"

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

# Ikona hlavního okna

```py
from PyQt5 import QtGui


        #1
        self.setWindowIcon(QtGui.QIcon("Icons\\logo.png")) 
```
---

# $$10\ ComboBox$$

V QT Designeru:

<img src="image\README\7.png" width="500">

nebo $setItemIcon(idx\_item, icon)$:

```py
        #1
        dropdown_images_path = ['Icons\\low.png','Icons\\medium.png','Icons\\high.png']   
        for i in range(self.dropdown_priority.count()):
            self.dropdown_priority.setItemIcon(i, QtGui.QIcon(dropdown_images_path[i]))  
```

---

Velikost ikon itemu ComboBoxu

```py
from PyQt5 import QtCore
  

        #1
        self.dropdown_priority.setIconSize(QtCore.QSize(30,10))
```

Ikony v seznamu úkolů - upravíme  $add\_task$.

* $currentIndex()$ -  index itemu v dropdownu.
* Vytvaříme item ze třídy $QListWidgetItem$.

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

Zvětšíme rozměr ikon v seznamu úkolů.

```py
        #1
        for widget in self.list_widgets:
            widget.setIconSize(QtCore.QSize(40,40))
```

---

# $$11\ Vizuální\ část\ 2$$

Stylizovanní itemů v $QListWidget$.

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

Chyba v přednastavených vlastnosti. Definujeme znovu.

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

# Druhá možnost (volitelně)

Můžeme to nastavit i v kódu.
V kódu nemůžeme nastavit hranice/border, pouze barvu pozadí.

```py
        #1
        for widget in self.list_widgets:
            widget.model().rowsInserted.connect(self.update_color_background)
```

## **Definice signálu:**

1. Přijímá tři argumenty z modelu:
   - `start` – index pozice prvního přidaného řádku,
   - `end` – index posledního přidaného řádku.
   - `parent` - vrací objekt $QModelIndex$.

2. `self.sender().parent()` - vrací objekt $QListWidget$.
3. `sender_widget.item(idx)` - Dostane item z widgetu podle indexu.
4. Odložené provedení přes `singleShot (0,...)` a nastavit pozadí pouze pomocí anonymní funkce.

```py
    #2
    def update_color_background(self, parent, start, end):
        sender_widget = self.sender().parent()
        name_widget = sender_widget.objectName()
  
        color_map = {
            "list_todo": "#dae674",  
            "list_doing": "#75cbdf",  
            "list_done": "#66cb9e"  }
  
        item = sender_widget.item(start)
        QtCore.QTimer.singleShot(0, lambda: item.setBackground(QtGui.QColor(color_map[name_widget])))
```

---

# $$12\ ComboBox\ 2\ -\ datum$$

`QMessageBox` nepodporuje widgety jako je kalendář. Proto použijeme `QDialog`.

* Vytvoříme elementy a přidáme je na layout

* $QDialog$ má předdefinované tlačítka, v $QDialogButtonBox$.

* *Nastavíme pro $QDialog$ layout

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

## **Přidání $QDialog$ do funkce $add\_task$**

Předáváme $Item$  jako argument, pro jeho dálší změnu.

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

## **Sloty pro tlačítka**

Předdefinovaná tlačítka $OK, Cancel$ mají předdefinované signály:

* accepted
* rejected


Definujeme slot uvnitř $select\_date$ **jako lokální funkce** s argumety

**Standardní metody QDialog**

* accept() – Zavře okno a vrací kod odpovědí $QDialog.Accepted$ 
* reject() – Zavře okno a vrací $QDialog.Rejected$.

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

**Signály**

Pro signál tlačítka $OK$ přiřazujeme slot pomocí `lambda` funkce, aby se funkce nespustila okamžitě. Slot se spustí až při akci.

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
