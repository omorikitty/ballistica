from .interface import Effect
from .tag import CustomTag
import bascenev1 as bs

EFFECT_MAP = {}

def effect(cls):
    if cls.name is None:
        raise ValueError(f"the class {cls.__name__} duty define an attr name")
    if not cls.name in EFFECT_MAP:
        EFFECT_MAP[cls.name] = cls
        print(f'effect {cls.name} add succes')


@effect
class Tag(Effect):

    name = "tag"

    def __init__(self, **custom):
        super().__init__(**custom)

    def setup_customization(self):
        default_color = [(1.0, 0.7, 0.8), (0.7, 0.6, 1.0), (0.6, 0.8, 1.0)]
        self.color = self.custom.get("color", (1.0, 1.0, 1.0))
        self.animay = self.custom.get(
            "array", {i * 0.5: color for i, color in enumerate(default_color)}
        )
        self.anim = self.custom.get("anim", False)
        self.tag = self.custom.get("tag", "something")

    def apply(self, spaz):
        assert spaz.node
        self._tag = CustomTag(
            owner=spaz.node,
            tag=self.tag,
            col=self.color,
            anim=self.anim,
            animay=self.animay,
        )
        
    def update_customization(self, **new):
        super().update_customization(**new)
        # change attr for tag
        print("aplicando actualizacion...")
        if hasattr(self, "_tag"):
            self._tag.tag_text.text = self.tag
            self._tag.tag_text.color = self.color

    def remove(self, spaz):
        pass
