import babase
import bascenev1 as bs
import bascenev1lib
from bascenev1lib.actor.playerspaz import *
from database.manager import InventoryPlayer
from .effects import EFFECT_MAP
from typing import Sequence

class EffectPlayerSpaz(PlayerSpaz):
    def __init__(self,
                 player: bs.Player,
                 color: Sequence[float],
                 highlight: Sequence[float],
                 character: str,
                 powerups_expire: bool = True,
                 *args,
                 **kwargs):

        super().__init__(player=player,
                         color=color,
                         highlight=highlight,
                         character=character,
                         powerups_expire=powerups_expire,
                         *args,
                         **kwargs)
        
        self._activations = {}
        account_id = player._sessionplayer.get_v1_account_id()
        self.effects = InventoryPlayer(account_id)
        bs.timer(10, babase.WeakCall(self.switchtag), True)
        
        self.apply_effect()

    def switchtag(self):
        """ esto es solo un test para notar los cambios en tiempo real del juego"""
        import random
        print("cambiando tag...")
        nametag = ["zen", "hola", "test", "hello world"]
        c = random.choice(nametag)

        self.effects.add_effect(effect="tag", duration=10, tag=c)

        if "tag" in self._activations:
            self._activations["tag"].update_customization(tag=c)
        else:
            self.apply_effect()

        print(f"tag cambiado a {c}")

    def apply_effect(self):
        effects = self.effects.inventory()
        item = effects.get("item", {})
        for effect_name, custom_data in item.items():
            eff_cls = EFFECT_MAP.get(effect_name)
            if not eff_cls:
                continue
            custom = custom_data.get("custom", {})
            eff = eff_cls(**custom)
            self._activations[effect_name] = eff
            eff.apply(self)
            
            


def apply():
    print("aplicando efectos al jugador")
    bascenev1lib.actor.playerspaz.PlayerSpaz = EffectPlayerSpaz