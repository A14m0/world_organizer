#!/usr/bin/env python3
import json
from PyQt5 import QtWidgets, QtCore
import sys
from elements import *

low_complexity = 1
med_complexity = 2
high_complexity = 3


f = open("questions.json", "r")
dat = f.read()
f.close()

questions = json.loads(dat)


# the main window of the application
class MainWin(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, story):
        super().__init__()
        self.story = story
        self.setWindowTitle("Test Window")
        self.setGeometry(100,100,800,550)
        self.UiComponents()
        self.show()
        self.resized.connect(self.update_stuff)
        

    def UiComponents(self):
        # gets variables for defining windows
        x = self.width()
        y = self.height()

        # initialize the File menu
        self.menu_file = QtWidgets.QMenu(self)
        self.menu_file.setTitle("File")
        self.menu_file.addAction("New Story", self.Junk)
        self.menu_file.addAction("Load Story", self.Junk)
        self.menu_file.addSeparator()
        self.menu_file.addAction("Save Story", self.Junk)

        # initialize the Tools menu
        self.menu_tools = QtWidgets.QMenu(self)
        self.menu_tools.setTitle("Tools")
        self.menu_tools.addAction("View Timeline", self.Junk)
        self.menu_tools.addAction("View Relations", self.Junk)
        self.menu_tools.addAction("View Story Notes", self.Junk)
        self.menu_tools.addAction("Edit Story Notes", self.Junk)

        #initialize the toolbar
        self.toolbar = QtWidgets.QMenuBar(self)
        self.toolbar.addMenu(self.menu_file)
        self.toolbar.addMenu(self.menu_tools)

        # Initialize the starting button layout
        self.add_char_button = QtWidgets.QPushButton(self)
        self.add_event_button = QtWidgets.QPushButton(self)
        self.add_world_elem_button = QtWidgets.QPushButton(self)

        self.add_char_button.setGeometry(60, 40, 150, 25)
        self.add_char_button.setText("Add Character")

        self.add_event_button.setGeometry(60, 70, 150, 25)
        self.add_event_button.setText("Add Event")

        self.add_world_elem_button.setGeometry(60, 100, 150, 25)
        self.add_world_elem_button.setText("Add World Element")

        self.add_char_button.clicked.connect(self.Junk)
        self.add_event_button.clicked.connect(self.Junk)
        self.add_world_elem_button.clicked.connect(self.Junk)

        # initialize Information Labels
        self.story_str_label = QtWidgets.QLabel(self)
        self.story_str_label.setText("Story Name: " + self.story.get_title())
        self.story_str_label.setGeometry(60, y-70, 150, 25)

        self.char_num_label = QtWidgets.QLabel(self)
        self.char_num_label.setText("Number of Characters: " + str(len(self.story.get_characters())))
        self.char_num_label.setGeometry(60, y-50, 150, 25)

        self.event_num_label = QtWidgets.QLabel(self)
        self.event_num_label.setText("Number of Events: " + str(len(self.story.get_events())))
        self.event_num_label.setGeometry(60, y-30, 150, 25)

        # initialize tree view of story elements
        self.char_tree = QtWidgets.QTreeWidget(self)
        self.char_tree.setHeaderLabel("Characters")
        self.event_tree = QtWidgets.QTreeWidget(self)
        self.event_tree.setHeaderLabel("Events")
        self.location_tree = QtWidgets.QTreeWidget(self)
        self.location_tree.setHeaderLabel("Locations")
        self.world_prop_tree = QtWidgets.QTreeWidget(self)
        self.world_prop_tree.setHeaderLabel("World Properties")

        self.char_tree.setGeometry(230, 30, 300, 180)
        self.event_tree.setGeometry(550, 30, 300, 180)
        self.location_tree.setGeometry(230, 230, 300, 180)
        self.world_prop_tree.setGeometry(550, 230, 300, 180)


    # updates position of labels
    def update_stuff(self):
        geom = self.geometry()

        x = geom.width()
        y = geom.height()

        # define bounds beyond which we wont try to readjust stuff
        if y < 450:
            y = 450

        if x < 550:
            x = 550

        self.story_str_label.setGeometry(60, y-70, 150, 25)
        self.char_num_label.setGeometry(60, y-50, 150, 25)
        self.event_num_label.setGeometry(60, y-30, 150, 25)

        self.char_tree.setGeometry(230, 30, int((1/2) * (x-300)), int((1/2) * (y-180)) )
        self.event_tree.setGeometry(int((1/2) * (x-300)) + 250, 30, int((1/2) * (x-300)), int((1/2) * (y-180)) )
        self.location_tree.setGeometry(230, int((1/2) * (y-180)) + 50, int((1/2) * (x-300)), int((1/2) * (y-180)))
        self.world_prop_tree.setGeometry(int((1/2) * (x-300)) + 250, int((1/2) * (y-180)) + 50, int((1/2) * (x-300)), int((1/2) * (y-180)))

    # junk file
    def Junk(self):
        print("Button was pressed")
        
    # triggers resize events 
    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWin, self).resizeEvent(event)
  








def full_char():
    character = Character()
    for question in questions["Questions"]:
        element = Attribute()
        element.set_e1(question["QuestionString"])
        answer = input(question["QuestionString"] + " > ")
        element.set_e2(answer)
        character.add_attribute(element)

    print("\n" * 4)
    print("-"*20)
    print(character)
    

def med_char():
    ret_str = ""
    for question in questions["Questions"]:
        if question["Priority"] != 3:
            answer = input(question["QuestionString"] + " > ")
            ret_str += "%s: %s\n" % (question["QuestionString"], answer)
    print("\n" * 4)
    print("-"*20)
    print("Generated character information: ")
    print(ret_str)
    return

def min_char():
    ret_str = ""
    for question in questions["Questions"]:
        if question["Priority"] == 1:
            answer = input(question["QuestionString"] + " > ")
            ret_str += "%s: %s\n" % (question["QuestionString"], answer)
    print("\n" * 4)
    print("-"*20)
    print("Generated character information: ")
    print(ret_str)
    return



def main(ye_olden_flag):
    if not ye_olden_flag:
        App = QtWidgets.QApplication(sys.argv) 

        story = Story()
    
        # create the instance of our Window 
        window = MainWin(story) 

        # start the app 
        sys.exit(App.exec())
    else:


        levl = input("How in depth would you like to go? (1 (low), 2 (moderate), 3 (high)) > ")
        try:
            levl = int(levl)
        except ValueError:
            print("Failed to determine complexity. Please enter a valid complexity level")
            return
        if levl == low_complexity:
            min_char()
        elif levl == med_complexity:
            med_char()
        else:
            full_char()

    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(True)
    else:
        main(False)
