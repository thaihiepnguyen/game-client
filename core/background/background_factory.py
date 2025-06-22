


from core.const import BackgroundId

from sprites.backgrounds.tokyo.tokyo_animation import TokyoAnimation
from sprites.backgrounds.countryside.countryside_animation import CountrysideAnimation
from sprites.backgrounds.bridge.bridge_animation import BridgeAnimation
from sprites.backgrounds.temple.temple_animation import TempleAnimation
from sprites.backgrounds.street.street_animation import StreetAnimation

class BackgroundFactory:
    """
    Factory class for creating background objects.
    """

    @staticmethod
    def create_background(id: BackgroundId):
        """
        Create a background object based on the specified type.

        :param background_type: Type of the background to create.
        :param kwargs: Additional parameters for the background.
        :return: An instance of the specified background type.
        """
        if BackgroundId.TOKYO.value == id:
            return TokyoAnimation()
        elif BackgroundId.STREET.value == id:
            return StreetAnimation()
        elif BackgroundId.COUNTRY_SIDE.value == id:
            return CountrysideAnimation()
        elif BackgroundId.BRIDGE.value == id:
            return BridgeAnimation()
        elif BackgroundId.TEMPLE.value == id:
            return TempleAnimation()
        else:
            raise ValueError(f"Unknown background type: {id}")