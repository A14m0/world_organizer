from PyQt5 import QtWidgets, QtCore, QtGui
from elements import *


# dialog for adding a character
class AddChar_Diag(QtWidgets.QDialog):
    resized = QtCore.pyqtSignal()
    def __init__(self, Parent=None, character=None):
        super().__init__()
        self.parent = Parent
        
        # set parent value if character doesnt exist yet
        if character is None:
            self.level = self.parent.level
            self.char_exists = False
        else:
            self.level = 1
            self.char_exists = True
        
        self.index = 0
        self.story = self.parent.story
        self.character = character
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
        self.image_path = QtGui.QPixmap("images/character-default.jpg")
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

        # check if the character exists
        if self.char_exists:
            #load the answered questions
            for attr in self.character.attributes:
                quest = QtWidgets.QLabel(self)
                quest.setText(attr.ele1)
                quest.setGeometry(10, current_y, int(self.width()/2), 80)
                current_y = current_y + 90

                text_box = QtWidgets.QPlainTextEdit(self)
                text_box.setGeometry(10, current_y, int(self.width()/2) -40, 180)
                text_box.document().setPlainText(attr.ele2)
                self.edit_areas.append(text_box)
                current_y = current_y + 190

                self.vbox.addWidget(quest)
                self.vbox.addWidget(text_box)
        else:
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

        for val in self.edit_areas:
            attr = Attribute()

            if indx == 0:
                self.character = Character(val.toPlainText())
            
            attr.set_e1(self.story.questions["Questions"][indx]["QuestionString"])
            attr.set_e2(val.toPlainText())
            self.character.add_attribute(attr)

            indx = indx + 1


        if self.char_exists:
            self.story.update_character(self.character)
        else:
            self.story.add_character(self.character)
        
        self.close()

    def load_img(self):
        img_name = open_file("Image Files (*.jpg *.png)")
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

class AddEvent_Diag(QtWidgets.QDialog):
    resized = QtCore.pyqtSignal()
    def __init__(self, Parent=None, event=None):
        super().__init__()
        self.parent = Parent
        self.story = self.parent.story
        self.event = event

        if event is None:
            self.event_exists = False
        else:
            self.event_exists = True

        self.questions = ["Short Description (few words)",\
                         "Date the event occurred", "Time the event occurred",\
                         "Location the event happened at", "Description of the event"]
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
        self.image_path = QtGui.QPixmap("images/event-default.jpg")
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
        for question in self.questions:
            quest = QtWidgets.QLabel(self)
            quest.setText(question)
            quest.setGeometry(10, current_y, int(self.width()/2), 80)
            current_y = current_y + 90

            text_box = QtWidgets.QPlainTextEdit(self)
            text_box.setGeometry(10, current_y, int(self.width()/2) -40, 180)
            self.edit_areas.append(text_box)
            current_y = current_y + 190

            self.vbox.addWidget(quest)
            self.vbox.addWidget(text_box)

        # check if the event already exists
        if self.event_exists:
            # load previous answers if it does exist
            self.edit_areas[0].document().setPlainText(self.event.short)
            self.edit_areas[1].document().setPlainText(self.event.Date)
            self.edit_areas[2].document().setPlainText(self.event.Time)
            self.edit_areas[3].document().setPlainText(self.event.Location)
            self.edit_areas[4].document().setPlainText(self.event.Description)

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
        return super(AddEvent_Diag, self).resizeEvent(event)

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
        
        self.evt = Event(self.edit_areas[0].toPlainText(), 
                    self.edit_areas[1].toPlainText(), 
                    self.edit_areas[2].toPlainText(),
                    self.edit_areas[3].toPlainText(), 
                    self.edit_areas[4].toPlainText())
        if self.event_exists:
            self.story.update_event(self.evt)
        else:
            self.story.add_event(self.evt)
        self.close()

    def load_img(self):
        img_name = open_file("Image Files (*.jpg *.png)")
        if img_name != "":
            self.image_path = QtGui.QPixmap(img_name)
            self.update()




class AddLocation_Diag(QtWidgets.QDialog):
    resized = QtCore.pyqtSignal()
    def __init__(self, Parent=None, location=None):
        super().__init__()
        self.parent = Parent
        self.story = self.parent.story
        self.location = location

        if self.location is None:
            self.location_exists = False
        else:
            self.location_exists = True

        self.questions = ["Location Name",\
                         "Location Description",\
                         "Other notes"]
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
        self.image_path = QtGui.QPixmap("images/location-default.jpg")
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
        for question in self.questions:
            quest = QtWidgets.QLabel(self)
            quest.setText(question)
            quest.setGeometry(10, current_y, int(self.width()/2), 80)
            current_y = current_y + 90

            text_box = QtWidgets.QPlainTextEdit(self)
            text_box.setGeometry(10, current_y, int(self.width()/2) -40, 180)
            self.edit_areas.append(text_box)
            current_y = current_y + 190

            self.vbox.addWidget(quest)
            self.vbox.addWidget(text_box)

        # check if the location exists already
        if self.location_exists:
            self.edit_areas[0].document().setPlainText(self.location.name)
            self.edit_areas[1].document().setPlainText(self.location.description)
            self.edit_areas[2].document().setPlainText(self.location.notes)
            
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
        return super(AddLocation_Diag, self).resizeEvent(event)

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
        
        self.location = Location(self.edit_areas[0].toPlainText(), 
                        self.edit_areas[1].toPlainText(), 
                        self.edit_areas[2].toPlainText())
        if self.location_exists:
            self.story.update_location(self.location)
        else:
            self.story.add_location(self.location)
        self.close()

    def load_img(self):
        img_name = open_file("Image Files (*.jpg *.png)")
        if img_name != "":
            self.image_path = QtGui.QPixmap(img_name)
            self.update()


# dialogue to add a new World Property
class AddWorldProp_Diag(QtWidgets.QDialog):
    resized = QtCore.pyqtSignal()
    def __init__(self, Parent=None, prop=None):
        super().__init__()
        self.parent = Parent
        self.story = self.parent.story
        self.prop = prop

        if self.prop is None:
            self.world_prop_exists = False
        else: 
            self.world_prop_exists = True

        self.questions = ["World Property Name",\
                         "Notes about the property"]
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
        self.image_path = QtGui.QPixmap("images/world-default.jpg")
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
        for question in self.questions:
            quest = QtWidgets.QLabel(self)
            quest.setText(question)
            quest.setGeometry(10, current_y, int(self.width()/2), 80)
            current_y = current_y + 90

            text_box = QtWidgets.QPlainTextEdit(self)
            text_box.setGeometry(10, current_y, int(self.width()/2) -40, 180)
            self.edit_areas.append(text_box)
            current_y = current_y + 190

            self.vbox.addWidget(quest)
            self.vbox.addWidget(text_box)

        # check if the property exists already
        if self.world_prop_exists:
            self.edit_areas[0].document().setPlainText(self.prop.name)
            self.edit_areas[1].document().setPlainText(self.prop.notes)
            


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
        return super(AddWorldProp_Diag, self).resizeEvent(event)

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
        
        self.prop = World_Prop(self.edit_areas[0].toPlainText(), 
                        self.edit_areas[1].toPlainText())
        
        if self.world_prop_exists:
            self.story.update_world_attr(self.prop)
        else:
            self.story.add_world_attr(self.prop)
        self.close()

    def load_img(self):
        img_name = open_file("Image Files (*.jpg *.png)")
        if img_name != "":
            self.image_path = QtGui.QPixmap(img_name)
            self.update()



def open_file(filtr):
    obj = QtWidgets.QFileDialog()
    filepath = obj.getOpenFileName(None, "Select file", "", filtr)
    
    if not filepath:
        return 0

    name = filepath[0]

    return name  