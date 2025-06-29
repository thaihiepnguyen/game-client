


from core.character.character import Character
from core.const import CharacterId
from sprites.characters.archer.archer_animation import ArcherAnimation
from sprites.characters.fighter.fighter_animation import FighterAnimation
from sprites.characters.gorgon.gorgon_animation import GorgonAnimation
from sprites.characters.vampire.vampire import Vampire
from sprites.characters.vampire.vampire_animation import VampireAnimation
from sprites.characters.wizard.wizard import Wizard
from sprites.characters.wizard.wizard_animation import WizardAnimation
from sprites.characters.yamabushi_tengu.yamabushi_tengu_animation import YamabushiTenguAnimation
from sprites.characters.archer.archer import Archer
from sprites.characters.fighter.fighter import Fighter
from sprites.characters.gorgon.gorgon import Gorgon
from sprites.characters.yamabushi_tengu.yamabushi_tengu import YamabushiTengu

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
            return Archer(ArcherAnimation())
        elif id == CharacterId.GORGON.value:
            return Gorgon(GorgonAnimation())
        elif id == CharacterId.FIGHTER.value:
            return Fighter(FighterAnimation())
        elif id == CharacterId.TENGU.value:
            return YamabushiTengu(YamabushiTenguAnimation())
        elif id == CharacterId.VAMPIRE.value:
            return Vampire(VampireAnimation())
        elif id == CharacterId.WIZARD.value:
            return Wizard(WizardAnimation())
        else:
            raise ValueError(f"Unknown character type: {id}")