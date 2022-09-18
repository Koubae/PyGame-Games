from .entity import Entity


class Padel(Entity):
    """Representation of a Padel / Player Object"""
    def __init__(self, *args):
        super().__init__(*args)
        self.player: str = ""
        self.speed: int = 12
        self.score: int = 0

    def score_add(self) -> None:
        """Adds score to the Padel Player"""
        self.score += 1
