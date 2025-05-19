from event import Event;

class EventOnline(Event):
    def __init__(self, name, _=""):
        local = f"https://ambientevirtual.com/eventos?id={EventOnline.id}";
        super().__init__(name, local)