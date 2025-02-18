from typing import Type, Dict
from .interface import Effect

class EffectFactory:
    _effects: Dict[str, Type[Effect]] = {}

    @classmethod
    def register(cls, effect_cls: Type[Effect]):
        if not effect_cls.name:
            raise ValueError(f"La clase {effect_cls.__name__} debe definir un atributo 'name'")
        cls._effects[effect_cls.name] = effect_cls
        print(f"Effect: {effect_cls.name} registrado correctamente")
        return effect_cls

    @classmethod
    def create(cls, effect_name: str, **custom) -> Effect | None:
        effect_cls = cls._effects.get(effect_name)
        return effect_cls(**custom) if effect_cls else None