from abc import ABC, abstractmethod
from bascenev1lib.actor.playerspaz import PlayerSpaz


class Effect(ABC):
    
    name: str | None

    def __init__(self, **custom):
        self.custom = custom
        self.setup()


    def setup(self):
        pass
    
    
    def update_custom(self, **new):
        self.custom.update(new)
        self.setup()


    @abstractmethod
    def apply(self, spaz: PlayerSpaz):
        raise NotImplementedError()


    @abstractmethod
    def remove(self, spaz: PlayerSpaz):
        raise NotImplementedError()