#!/usr/bin/env python3
import json
from PyQt5 import QtWidgets, QtCore
import sys

import ui_classes
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
        self.add_location_button = QtWidgets.QPushButton(self)
        self.add_world_elem_button = QtWidgets.QPushButton(self)


        self.add_char_button.setGeometry(60, 40, 150, 25)
        self.add_char_button.setText("Add Character")

        self.add_event_button.setGeometry(60, 70, 150, 25)
        self.add_event_button.setText("Add Event")

        self.add_location_button.setGeometry(60, 100, 150, 25)
        self.add_location_button.setText("Add Location")
        
        self.add_world_elem_button.setGeometry(60, 130, 150, 25)
        self.add_world_elem_button.setText("Add World Attribute")

        self.add_char_button.clicked.connect(self.add_character)
        self.add_event_button.clicked.connect(self.add_event)
        self.add_location_button.clicked.connect(self.add_location)
        self.add_world_elem_button.clicked.connect(self.add_world_attr)

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

        # set tree geometry
        self.char_tree.setGeometry(230, 30, 300, 180)
        self.event_tree.setGeometry(550, 30, 300, 180)
        self.location_tree.setGeometry(230, 230, 300, 180)
        self.world_prop_tree.setGeometry(550, 230, 300, 180)

        # set up signal handlers (data, column)
        self.char_tree.itemDoubleClicked.connect(self.Junk)
        self.event_tree.itemDoubleClicked.connect(self.Junk)
        self.location_tree.itemDoubleClicked.connect(self.Junk)
        self.world_prop_tree.itemDoubleClicked.connect(self.Junk)

        self.update_stuff()

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

        # resize text labels
        self.story_str_label.setGeometry(60, y-70, 150, 25)
        self.char_num_label.setGeometry(60, y-50, 150, 25)
        self.event_num_label.setGeometry(60, y-30, 150, 25)

        # resize views
        self.char_tree.setGeometry(230, 30, int((1/2) * (x-300)), int((1/2) * (y-180)) )
        self.event_tree.setGeometry(int((1/2) * (x-300)) + 250, 30, int((1/2) * (x-300)), int((1/2) * (y-180)) )
        self.location_tree.setGeometry(230, int((1/2) * (y-180)) + 50, int((1/2) * (x-300)), int((1/2) * (y-180)))
        self.world_prop_tree.setGeometry(int((1/2) * (x-300)) + 250, int((1/2) * (y-180)) + 50, int((1/2) * (x-300)), int((1/2) * (y-180)))

    # reload all of the tree views
    def reload_trees(self):
        # clear the tree views
        self.char_tree.clear()
        self.event_tree.clear()
        self.location_tree.clear()
        self.world_prop_tree.clear()

        # re-add all of the entries
        for character in self.story.get_characters():
            entry = QtWidgets.QTreeWidgetItem(self.char_tree)
            entry.setText(0, character.get_text())
            entry.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(character))
            self.char_tree.addTopLevelItem(entry)

        for event in self.story.get_events():
            entry = QtWidgets.QTreeWidgetItem(self.event_tree)
            entry.setText(0, event.get_text())
            entry.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(event))
            self.char_tree.addTopLevelItem(entry)

        for location in self.story.get_locations():
            entry = QtWidgets.QTreeWidgetItem(self.location_tree)
            entry.setText(0, location.get_text())
            entry.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(location))
            self.char_tree.addTopLevelItem(entry)

        for attr in self.story.get_world_attr():
            entry = QtWidgets.QTreeWidgetItem(self.world_prop_tree)
            entry.setText(0, attr.get_text())
            entry.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(attr))
            self.char_tree.addTopLevelItem(entry)
        
        # update labels
        self.story_str_label.setText("Story Name: " + self.story.get_title())
        self.char_num_label.setText("Number of Characters: " + str(len(self.story.get_characters())))
        self.event_num_label.setText("Number of Events: " + str(len(self.story.get_events())))
        

    # junk file
    def Junk(self):
        print("Button was pressed")
        
    # triggers resize events 
    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWin, self).resizeEvent(event)
  
    def add_character(self):
        win = ui_classes.ComplexityLvl_Diag(self)
        win.exec()
        self.reload_trees()
        return

    def add_event(self):
        win = ui_classes.AddEvent_Diag(self)
        win.exec()
        self.reload_trees()
        return

    def add_location(self):
        win = ui_classes.AddLocation_Diag(self)
        win.exec()
        self.reload_trees()
        return

    def add_world_attr(self):
        win = ui_classes.AddWorldProp_Diag(self)
        win.exec()
        self.reload_trees()
        return








def full_char(name):


    character = Character(name)
    for question in questions["Questions"]:
        element = Attribute()
        element.set_e1(question["QuestionString"])
        answer = input(question["QuestionString"] + " > ")
        element.set_e2(answer)
        character.add_attribute(element)

    print("\n" * 4)
    print("-"*20)
    print(character)
    

def med_char(name):
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

def min_char(name):
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

        story = Story(questions)
    
        # create the instance of our Window 
        window = MainWin(story) 

        # start the app 
        sys.exit(App.exec())
    else:

        name = "Test Name"
        levl = input("How in depth would you like to go? (1 (low), 2 (moderate), 3 (high)) > ")
        try:
            levl = int(levl)
        except ValueError:
            print("Failed to determine complexity. Please enter a valid complexity level")
            return
        if levl == low_complexity:
            min_char(name = "Test Name")
        elif levl == med_complexity:
            med_char(name = "Test Name")
        else:
            full_char(name = "Test Name")

    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(True)
    else:
        main(False)
