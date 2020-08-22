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
        y = self.height()

        # initialize the File menu
        self.menu_file = QtWidgets.QMenu(self)
        self.menu_file.setTitle("File")
        self.menu_file.addAction("New Story", self.new_story)
        self.menu_file.addAction("Load Story", self.load_story)
        self.menu_file.addSeparator()
        self.menu_file.addAction("Save Story", self.story.save)

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
        self.char_tree.itemDoubleClicked.connect(self.char_double_click)
        self.event_tree.itemDoubleClicked.connect(self.evt_double_click)
        self.location_tree.itemDoubleClicked.connect(self.loc_double_click)
        self.world_prop_tree.itemDoubleClicked.connect(self.prop_double_click)

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
        self.story_str_label.setGeometry(60, y-70, self.width(), 25)
        self.char_num_label.setGeometry(60, y-50, self.width(), 25)
        self.event_num_label.setGeometry(60, y-30, self.width(), 25)

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

    def load_story(self):
        path = ui_classes.open_file("Story Files (*.json)")
        if path != "":
            self.story.load(path)
            self.reload_trees()
        return

    def new_story(self):
        
        win = ui_classes.NewStory_Diag(self)
        win.exec()

        self.reload_trees()
        return

    def char_double_click(self, char, col):
        win = ui_classes.AddChar_Diag(self, char.data(0, QtCore.Qt.UserRole))
        win.exec()
        self.reload_trees()
        return


    def evt_double_click(self, evt, col):
        win = ui_classes.AddEvent_Diag(self, evt.data(0, QtCore.Qt.UserRole))
        win.exec()
        self.reload_trees()
        return

    
    def loc_double_click(self, loc, col):
        win = ui_classes.AddLocation_Diag(self, loc.data(0, QtCore.Qt.UserRole))
        win.exec()
        self.reload_trees()
        return

    
    def prop_double_click(self, prop, col):
        win = ui_classes.AddWorldProp_Diag(self, prop.data(0, QtCore.Qt.UserRole))
        win.exec()
        self.reload_trees()
        return


class TreeView_Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, story):
        super().__init__()
        self.setWindowTitle("Test Window 2")
        self.setGeometry(100, 100, 800, 550)
        self.story = story
        self.entries = []
        self.UiComponents()
        self.show()
        self.resized.connect(self.update)
        self.update()

    def UiComponents(self):
        # set up the main view of the central widget
        self.main_view = QtWidgets.QTreeWidget(self)
        self.main_view.setColumnCount(2)
        self.main_view.setGeometry(40, 40, self.width()-80, self.height()-80)
        self.main_view.doubleClicked.connect(self.handle_open)

        # initialize the File menu
        self.menu_file = QtWidgets.QMenu(self)
        self.menu_file.setTitle("File")
        self.menu_file.addAction("New Story", self.new_story)
        self.menu_file.addAction("Load Story", self.load_story)
        self.menu_file.addSeparator()
        self.menu_file.addAction("Save Story", self.story.save)

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

    # junk file
    def Junk(self):
        print("Button was pressed")
        
    def load_story(self):
        path = ui_classes.open_file("Story Files (*.json)")
        if path != "":
            self.story.load(path)
            self.reload()
        return

    def new_story(self):
        
        win = ui_classes.NewStory_Diag(self)
        win.exec()

        self.reload()
        return


    # triggers resize events 
    def resizeEvent(self, event):
        self.resized.emit()
        return super(TreeView_Window, self).resizeEvent(event)

    def update(self):
        self.main_view.setGeometry(40, 40, self.width() -80 , self.height()-80)
        return

    def contextMenuEvent(self, event):
        cmenu = QtWidgets.QMenu(self)

        new_loc = cmenu.addAction("New Location")
        new_char = cmenu.addAction("New Character")
        new_event = cmenu.addAction("New Event")
        new_world_prop = cmenu.addAction("New World Property")

        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        data = None
        add_type = ""

        win = None

        if action == quitAct:
            self.close()
        elif action == new_char:
            add_type = "Character"
            win = ui_classes.ComplexityLvl_Diag(self)
        elif action == new_event:
            add_type = "Event"
            win = ui_classes.AddEvent_Diag(self)
        elif action == new_loc:
            add_type = "Location"
            win = ui_classes.AddLocation_Diag(self)
        elif action == new_world_prop:
            add_type = "World Property"
            win = ui_classes.AddWorldProp_Diag(self)
        else:
            print("No Known Action")
            return

        win.exec()

        data = self.story.most_recent

        selected = self.main_view.selectedItems()
        if len(selected) > 1:
            print("Too many selected")
            return
        elif len(selected) == 0:
            item = QtWidgets.QTreeWidgetItem(self.main_view)
            self.entries.append(item)
            item.setText(0, add_type)
            item.setText(1,data.get_text())
            item.setData(1, QtCore.Qt.UserRole, QtCore.QVariant(data))
            self.main_view.addTopLevelItem(item)
        else:
            item = QtWidgets.QTreeWidgetItem(selected[0])
            self.entries.append(item)
            item.setText(0, add_type)
            item.setText(1, data.get_text())
            item.setData(1, QtCore.Qt.UserRole, QtCore.QVariant(data))
            selected[0].addChild(item)



    def handle_open(self, char):
        dat = char.data(QtCore.Qt.UserRole)
        win = None
        if isinstance(dat, Character):
            print("Class Character Detected")
            win = ui_classes.AddChar_Diag(self, dat)
        elif isinstance(dat, Event):
            print("Class Event Detected")
            win = ui_classes.AddEvent_Diag(self, dat)
        elif isinstance(dat, Location):
            print("Class Location Detected")
            win = ui_classes.AddLocation_Diag(self, dat)
        elif isinstance(dat, World_Prop):
            print("Class World_Property Detected")
            win = ui_classes.AddWorldProp_Diag(self, dat)
        else:
            print("Illegal class %s" % type(dat))
        
        
        win.exec()
        self.reload()
        return

    def reload(self):
        for entry in self.entries:
            entry.setText(1, entry.data(1, QtCore.Qt.UserRole).get_text())

def main():
    App = QtWidgets.QApplication(sys.argv) 
    story = Story("Default", questions)
    
    # create the instance of our Window 
    if len(sys.argv) > 1:
        window = TreeView_Window(story)
    else:
        window = MainWin(story) 

    # start the app 
    sys.exit(App.exec())
    

if __name__ == "__main__":
    main()
