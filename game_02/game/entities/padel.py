from .entity import Entity


class Padel(Entity):


    def __init__(self, *args):
        super().__init__(*args)
        self.player: str = ""
        self.speed: int = 12
