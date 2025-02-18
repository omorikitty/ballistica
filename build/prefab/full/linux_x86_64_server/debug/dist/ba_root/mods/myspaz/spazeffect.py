import babase
import asyncio
import bascenev1 as bs
import bascenev1lib
from bascenev1lib.actor.playerspaz import *
from database.managers import ManagerFactory
from myspaz.effects.interface import Effect
from myspaz.effects import EffectFactory
from typing import Sequence

class EffectPlayerSpaz(PlayerSpaz):
    def __init__(
        self,
        player: bs.Player,
        color: Sequence[float],
        highlight: Sequence[float],
        character: str,
        powerups_expire: bool = True,
        *args,
        **kwargs,
    ):

        super().__init__(
            player=player,
            color=color,
            highlight=highlight,
            character=character,
            powerups_expire=powerups_expire,
            *args,
            **kwargs,
        )
        self._active_effects: dict[str, Effect] = {}
        self.account_id = player._sessionplayer.get_v1_account_id()
        self.customer = ManagerFactory.get("customers")
        self.inv = self.customer.getInventory(self.account_id)
        self.customer.register(self.account_id, self)
        self.timer = bs.timer(10, bs.WeakCall(self._change_tag_test), True)

    def _change_tag_test(self):
        import random
        nametag = ["test", "change...", "hello", "noob"]
        color = (random.random(), random.random(), random.random())
        tag = random.choice(nametag)
        self.customer.addEffect(self.account_id, "tag", 10, **{"tag": tag, "color": color})

    def apply(self):
        for effect, data in self.inv.get("item", {}).items():
            if effectclass := EffectFactory.create(effect, **data.get("custom", {})):
                effectclass.apply(self)
                self._active_effects[effect] = effectclass
    
    def on_expire(self) -> None:
        self.customer.unregister(self.account_id)
        super().on_expire()

            

        


def apply():
    print("Inicializando clase para los efectos...")
    bascenev1lib.actor.playerspaz.PlayerSpaz = EffectPlayerSpaz
