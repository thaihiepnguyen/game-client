


from core.const import BackgroundId


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
            from sprites.backgrounds.tokyo.tokyo_animation import TokyoAnimation
            return TokyoAnimation()
        elif BackgroundId.STREET.value == id:
            from sprites.backgrounds.street.street_animation import StreetAnimation
            return StreetAnimation()
        elif BackgroundId.COUNTRY_SIDE.value == id:
            from sprites.backgrounds.countryside.countryside_animation import CountrysideAnimation
            return CountrysideAnimation()
        elif BackgroundId.BRIDGE.value == id:
            from sprites.backgrounds.bridge.bridge_animation import BridgeAnimation
            return BridgeAnimation()
        elif BackgroundId.TEMPLE.value == id:
            from sprites.backgrounds.temple.temple_animation import TempleAnimation
            return TempleAnimation()
        else:
            raise ValueError(f"Unknown background type: {id}")