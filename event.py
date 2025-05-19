class Event:
    id = 0;

    def __init__(self, name, local=""):
        self.name = name;
        self.local = local;
        self.id = Event.id;
        Event.id += 1;