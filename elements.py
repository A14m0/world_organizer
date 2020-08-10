# class for defining characters and their attributes
class Character:
    def __init__(self):
        self.attributes = []
    
    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def __str__(self):
        ret_str = ""
        for element in self.attributes:
            ret_str = ret_str + element
        
        return ret_str

# class that defines a question element or answer to a question
class Attribute:
    def __init__(self):
        self.ele1 = ""
        self.ele2 = ""

    def set_e1(self, e1):
        self.ele1 = e1

    def set_e2(self, e2):
        self.ele2 = e2

    def __str__(self):
        return "%s: %s" % (self.ele1, self.ele2)


# class for printing fancy text
class bcolors:
    HEADER = '\033[95m'
    CYAN = '\033[0;36m'
    DARKRED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    BRIGHTYELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    BRIGHTPURPLE = '\033[1;35m\033[1;41m'
    BLUE = '\033[0;34m'
    BRIGHTBLUE = '\033[1;34m'
    BLACK = '\033[0;30m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BACK_RED = '\033[0;41m'
    BACK_BRIGHTRED = '\033[1;41m'
    BACK_GREEN = '\033[0;42m'
    BACK_BRIGHTGREEN = '\033[1;42m'
    BACK_YELLOW = '\033[0;43m'
    BACK_BRIGHTYELLOW = '\033[1;43m'
    BACK_BLUE = '\033[0;44m'
    BACK_BRIGHTBLUE = '\033[1;44m'
    BACK_PURPLE = '\033[0;45m'
    BACK_BRIGHTPURPLE = '\033[1;45m'
    BLACK_RED = '\033[0;30m\033[1;41m'



# class that defines a particular world event
class Event:
    def __init__(self, date, time, location, description):
        self.Date = date
        self.Time = time
        self.Location = location
        self.Description = description

# class that defines a world location
class World:
    def __init__(self, name, description, notes):
        self.name = name
        self.description = description
        self.notes = notes

    def __str__(self):
        return "Name: %s\nDescription: %s\nNotes: %s\n" % \
                        (self.name, self.description, self.notes)

# class that holds specific information about a story
class Story:
    def __init__(self):
        self.characters = []
        self.events = []
        self.worlds = []
        self.notes = []

    def add_character(self, character):
        self.characters.append(character)

    def add_event(self, event):
        self.events.append(event)

    def add_world(self, world):
        self.worlds.append(world)

    def add_note(self, note):
        self.notes.append(note)

    def save(self):
        return None

    def load(self, path):
        return None
        
    def get_title(self):
        return "Test Story"
    
    def get_characters(self):
        return self.characters

    def get_events(self):
        return self.events