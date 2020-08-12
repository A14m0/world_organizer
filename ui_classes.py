from PyQt5 import QtWidgets, QtCore, QtGui
from elements import *


# dialog for adding a character
class AddChar_Diag(QtWidgets.QDialog):
    resized = QtCore.pyqtSignal()
    def __init__(self, Parent=None):
        super().__init__()
        self.parent = Parent
        self.level = self.parent.level
        self.index = 0
        self.story = self.parent.story
        self.character = None
        self.FirstRun = True
        self.edit_areas = []
        
        self.setGeometry(100,100,960,800)


        self.UiComponents()
        self.show()
        self.update()
        self.resized.connect(self.update)
        #self.move_next()

    def UiComponents(self):
        # set up buttons and picture spots
        self.save = QtWidgets.QPushButton(self)
        self.cancel = QtWidgets.QPushButton(self)
        self.image = QtWidgets.QLabel(self)
        self.image_path = QtGui.QPixmap("example.jpg")
        self.image_button = QtWidgets.QPushButton(self)

        self.save.setText("Save")
        self.cancel.setText("Cancel")
        self.image_button.setText("Load Image")

        # connect buttons
        self.save.clicked.connect(self.save_char)
        self.cancel.clicked.connect(self.close)
        self.image_button.clicked.connect(self.load_img)

        self.image.setPixmap(self.image_path)

        # move buttons
        self.save.setGeometry(int(self.width()/2) + 30, self.height() -30, 100, 35)
        self.cancel.setGeometry(int(3*self.width()/4) + 30, self.height() -30, 100, 35)
        self.image_button.setGeometry(int(2*self.width()/3), int(self.height()/2) + 20, 100, 35)

        # set up scroll area for questions
        self.scroll = QtWidgets.QScrollArea(self)
        self.widget = QtWidgets.QWidget(self)
        self.vbox = QtWidgets.QVBoxLayout(self)

        current_y = 0

        # add questions and spots to answer them
        for question in self.story.questions["Questions"]:
            if question["Priority"] <= self.level:
                quest = QtWidgets.QLabel(self)
                quest.setText(question["QuestionString"])
                quest.setGeometry(10, current_y, int(self.width()/2), 80)
                current_y = current_y + 90

                text_box = QtWidgets.QPlainTextEdit(self)
                text_box.setGeometry(10, current_y, int(self.width()/2) -40, 180)
                self.edit_areas.append(text_box)
                current_y = current_y + 190

                self.vbox.addWidget(quest)
                self.vbox.addWidget(text_box)


        # finish up the scroll layout
        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setGeometry(0, 0, int(self.width()/2), self.height())


    # triggers resize events 
    def resizeEvent(self, event):
        self.resized.emit()
        return super(AddChar_Diag, self).resizeEvent(event)

    def update(self):
        self.scroll.setGeometry(0, 0, int(self.width()/2), self.height())
        for editor in self.edit_areas:
            editor_geom = editor.geometry()
            editor.setGeometry(10, editor_geom.y(), int(self.width()/2) -40, 80)

        self.image.setPixmap(self.image_path.scaled(int(self.width()/2)-60, int(self.height()/2)- 60)) #QtCore.Qt.KeepAspectRatio,
        self.image.setGeometry(int(self.width()/2) + 30 , 30, int(self.width()/2)-60, int(self.height()/2)- 60)
        

        self.save.setGeometry(int(3*self.width()/6) + 30, self.height() -45, 100, 35)
        self.cancel.setGeometry(int(5*self.width()/6) + 30, self.height() -45, 100, 35)
        self.image_button.setGeometry(int(3*self.width()/4)-50, int(self.height()/2) + 20, 100, 35)


    def save_char(self):
        indx = 0
        self.character = None
        for val in self.edit_areas:
            attr = Attribute()

            if indx == 0:
                self.character = Character(val.toPlainText())
            else:
                attr.set_e1(self.story.questions["Questions"][indx]["QuestionString"])
                attr.set_e2(val.toPlainText())
                self.character.add_attribute(attr)

            indx = indx + 1

        self.story.add_character(self.character)
        self.close()

    def load_img(self):
        img_name = open_file()
        if img_name != "":
            self.image_path = QtGui.QPixmap(img_name)
            self.update()


        

class ComplexityLvl_Diag(QtWidgets.QDialog):
    def __init__(self, Parent=None):
        super().__init__()
        self.parent = Parent
        self.story = self.parent.story
        self.setGeometry(600, 400, 420, 180)
        self.level = -1
        self.UiComponents()
        self.show()

    def UiComponents(self):
        # set up buttons
        self.low_comp_button = QtWidgets.QPushButton(self)
        self.med_comp_button = QtWidgets.QPushButton(self)
        self.high_comp_button = QtWidgets.QPushButton(self)

        # set up labels and button texts
        self.low_comp_button.setText("Low Complexity")
        self.med_comp_button.setText("Medium Complexity")
        self.high_comp_button.setText("High Complexity")

        self.lab = QtWidgets.QLabel(self)

        # Position the buttons
        self.lab.setGeometry(int(self.width()/2) - 170, 20, 340, 30)
        self.lab.setText("How Complex of a character would you like to make?")

        self.low_comp_button.setGeometry(10, 80, 130, 25)
        self.med_comp_button.setGeometry(145, 80, 130, 25)
        self.high_comp_button.setGeometry(280, 80, 130, 25)

        # hook up the buttons 
        self.low_comp_button.clicked.connect(self.low)
        self.med_comp_button.clicked.connect(self.med)
        self.high_comp_button.clicked.connect(self.high)

    def low(self):
        self.hide()
        self.level = 1
        win = AddChar_Diag(self)
        win.exec()
        return

    def med(self):
        self.hide()
        self.level = 2
        win = AddChar_Diag(self)
        win.exec()
        return

    def high(self):
        self.hide()
        self.level = 3
        win = AddChar_Diag(self)
        win.exec()
        return

def open_file():
    obj = QtWidgets.QFileDialog()
    filepath = obj.getOpenFileName(None, "Select file", "", "Image Files (*.jpg *.png)")
    
    if not filepath:
        return 0

    name = filepath[0]

    return name  