import json
import ui_classes

# base class that defines required generic functions
class Base:
    def get_text(self):
        pass


# class for defining characters and their attributes
class Character(Base):
    def __init__(self, name):
        self.name = name
        self.attributes = []
    
    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def __str__(self):
        ret_str = ""
        for element in self.attributes:
            ret_str = ret_str + element + "\n"
        
        return ret_str

    def get_text(self):
        return self.name

# class that defines a question element or answer to a question
class Attribute(Base):
    def __init__(self):
        self.ele1 = ""
        self.ele2 = ""

    def set_e1(self, e1):
        self.ele1 = e1

    def set_e2(self, e2):
        self.ele2 = e2

    def __str__(self):
        return "%s: %s" % (self.ele1, self.ele2)


# class that defines a particular world event
class Event(Base):
    def __init__(self, short, date, time, location, description):
        self.short = short
        self.Date = date
        self.Time = time
        self.Location = location
        self.Description = description

    def get_text(self):
        return self.short


# class that defines a world location
class Location(Base):
    def __init__(self, name, description, notes):
        self.name = name
        self.description = description
        self.notes = notes

    def __str__(self):
        return "Name: %s\nDescription: %s\nNotes: %s\n" % \
                        (self.name, self.description, self.notes)

    def get_text(self):
        return self.name


# class that defines a world property
class World_Prop(Base):
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes

    def __str__(self):
        return "Name: %s, Notes: %s" % (self.name, self.notes)

    def get_text(self):
        return self.name

# class that holds specific information about a story
class Story(Base):
    def __init__(self, title, questions):
        self.characters = []
        self.events = []
        self.locations = []
        self.world_attributes = []
        self.notes = ""
        
        self.path = None
        self.title = title
        self.questions = questions

    def add_character(self, character):
        self.characters.append(character)

    def add_event(self, event):
        self.events.append(event)

    def add_location(self, loc):
        self.locations.append(loc)

    def add_world_attr(self, attr):
        self.world_attributes.append(attr)

    def update_character(self, character):
        indx = 0
        for char in self.characters:
            if char.get_text() == character.get_text():
                self.characters[indx] = character
                return
            indx += 1
        
        self.add_character(character)

    def update_event(self, event):
        indx = 0
        for evt in self.events:
            if evt.get_text() == event.get_text():
                self.events[indx] = event
                return
            indx += 1
        
        self.add_event(event)

    def update_location(self, location):
        indx = 0
        for loc in self.locations:
            if loc.get_text() == location.get_text():
                self.locations[indx] = location
                return
            indx += 1
        
        self.add_location(location)

    def update_world_attr(self, attribute):
        indx = 0
        for attr in self.world_attributes:
            if attr.get_text() == attribute.get_text():
                self.world_attributes[indx] = attribute
                return
            indx += 1
        
        self.add_world_attr(attribute)

    def save(self):
        # initialize the json structure
        data = {}
        data["Title"] = self.title
        data["Notes"] = self.notes
        data["Characters"] = []
        data["Events"] = []
        data["Locations"] = []
        data["World_Properties"] = []

        # read all characters
        for character in self.characters:
            tmp_dat = {}
            tmp_dat["Name"] = character.get_text()
            tmp_dat["Attributes"] = []

            # read all of the target character's attributes
            for attr in character.attributes:
                tmp_dat["Attributes"].append({
                    "Element1": attr.ele1,
                    "Element2": attr.ele2
                })
            # append character to the data
            data["Characters"].append(tmp_dat)
        
        # same thing for events...
        for event in self.events:
            tmp_dat = {}
            tmp_dat["Short"] = event.get_text()
            tmp_dat["Date"] = event.Date
            tmp_dat["Time"] = event.Time
            tmp_dat["Location"] = event.Location
            tmp_dat["Description"] = event.Description

            # append event to the data
            data["Events"].append(tmp_dat)

        # ... and for locations...
        for location in self.locations:
            tmp_dat = {}
            tmp_dat["Name"] = location.get_text()
            tmp_dat["Description"] = location.description
            tmp_dat["Notes"] = location.notes

            # append location to the data
            data["Locations"].append(tmp_dat)

        # ... and for world properties
        for prop in self.world_attributes:
            tmp_dat = {}
            tmp_dat["Name"] = prop.get_text()
            tmp_dat["Notes"] = prop.notes

            # append location to the data
            data["World_Properties"].append(tmp_dat)


        if self.path is None:
            self.path = ui_classes.save_path()
        
        with open(self.path, "w") as f:
            json.dump(data, f)
            f.close()

        return

    def load(self, path):
        self.path = path

        with open(self.path, "r") as f:
            dat = json.load(f)

        # clear out the current lists
        self.characters.clear()
        self.events.clear()
        self.locations.clear()
        self.world_attributes.clear()
        self.notes = ""

        # load the title
        self.title = dat["Title"]
        self.notes = dat["Notes"]

        # load all of the characters stored in the story
        for character in dat["Characters"]:
            char = Character(character["Name"])
            for attr in character["Attributes"]:
                tmp_attr = Attribute()
                tmp_attr.set_e1(attr["Element1"])
                tmp_attr.set_e2(attr["Element2"])
                char.add_attribute(tmp_attr)
            self.add_character(char)

        # load all events 
        for event in dat["Events"]:
            tmp_evt = Event(event["Short"], event["Date"], 
                            event["Time"], event["Location"], 
                            event["Description"])
            self.add_event(tmp_evt)

        # load all locations
        for location in dat["Locations"]:
            tmp_loc = Location(location["Name"], 
                            location["Description"], 
                            location["Notes"])
            self.add_location(tmp_loc)

        # load all world attributes
        for propert in dat["World_Properties"]:
            tmp_prop = World_Prop(propert["Name"], 
                            propert["Notes"])
            self.add_world_attr(tmp_prop)

        return None

    def clear(self):
        self.characters = []
        self.events = []
        self.locations = []
        self.world_attributes = []

        self.title = "None"
        
    def get_title(self):
        return self.title
    
    def get_characters(self):
        return self.characters

    def get_events(self):
        return self.events

    def get_locations(self):
        return self.locations

    def get_world_attr(self):
        return self.world_attributes