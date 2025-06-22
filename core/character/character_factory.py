


from core.character.character import Character
from core.const import CharacterId
from sprites.characters.archer.archer_animation import ArcherAnimation
from sprites.characters.fighter.fighter_animation import FighterAnimation
from sprites.characters.gorgon.gorgon_animation import GorgonAnimation
from sprites.characters.yamabushi_tengu.yamabushi_tengu_animation import YamabushiTenguAnimation


class CharacterFactory:
    """
    Factory class for creating character instances.
    """

    @staticmethod
    def create_character(id: CharacterId) -> Character:
        """
        Create a character instance based on the character type.
        """
        
        if id == CharacterId.ARCHER.value:
            from sprites.characters.archer.archer import Archer
            return Archer(ArcherAnimation())
        elif id == CharacterId.GORGON.value:
            from sprites.characters.gorgon.gorgon import Gorgon
            return Gorgon(GorgonAnimation())
        elif id == CharacterId.FIGHTER.value:
            from sprites.characters.fighter.fighter import Fighter
            return Fighter(FighterAnimation())
        elif id == CharacterId.TENGU.value:
            from sprites.characters.yamabushi_tengu.yamabushi_tengu import YamabushiTengu
            return YamabushiTengu(YamabushiTenguAnimation())
        else:
            return Archer(ArcherAnimation())