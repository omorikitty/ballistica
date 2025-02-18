from .interface import Effect
from .tag import CustomTag
from myspaz.effects import EffectFactory



@EffectFactory.register
class Tag(Effect):

    name = "tag"

    def __init__(self, **custom):
        super().__init__(**custom)
        self._tag = None

    def setup(self):
        default_color = [(1.0, 0.7, 0.8), (0.7, 0.6, 1.0), (0.6, 0.8, 1.0)]
        self.color = self.custom.get("color", (1.0, 1.0, 1.0))
        self.array_color = self.custom.get("array_c", default_color)
        self.animate = self.custom.get("animate_c", False)
        self.tag = self.custom.get("tag", "something")

        self.animate_array = {i * 0.5: color[i-1] for i, color in enumerate(self.array_color)}

    def apply(self, spaz):
        assert spaz.node
        self._tag = CustomTag(
            owner=spaz.node,
            tag=self.tag,
            col=self.color,
            animate=self.animate,
            animate_array=self.animate_array,
        )
        
    def update_custom(self, **new):
        super().update_custom(**new)
        # change attr for tag
        print("aplicando actualizacion...")
        if self._tag:
            self._tag.tag_text.text = self.tag
            self._tag.tag_text.color = self.color

    def remove(self, spaz):
        pass
