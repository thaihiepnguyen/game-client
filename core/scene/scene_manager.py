from core.network.tcp_client import TCPClient
from scenes.battle_scene import BattleScene
from scenes.main_scene import MainScene
from core.scene import scene
from core.const import *

class SceneManager:
    def __init__(self, tcp_client: TCPClient):
        self.__scenes = {}
        self.__current_scene = None
        self._tcp_client = tcp_client

    def _add_scene(self, name: str, scene: type[scene.Scene]) -> None:
        """
        Add a scene to the manager.
        :param name: The name of the scene to add.
        :param scene: The scene class to add, which should inherit from Scene.Scene.
        """
        self.__scenes[name] = scene(self, self._tcp_client)

    def initialize(self) -> None:
        """
        Initialize the scene manager, setting up any necessary resources.
        This method can be extended to load resources or perform setup tasks.
        """
        scenes = {
            MAIN_SCENE: MainScene,
            BATTLE_SCENE: BattleScene,
            # Add more scenes here as needed
        }

        for name, scene_class in scenes.items():
            self._add_scene(name, scene_class)

    def set_scene(self, name: str, data=None) -> None:
        """
        Set the current scene by name.
        :param name: The name of the scene to set as current.
        """
        if name in self.__scenes:
            self.__current_scene = self.__scenes[name]
            if data is not None:
                self.__current_scene.on_enter(data)
        else:
            raise ValueError(f"Scene '{name}' not found in SceneManager.")
    
    def get_scene(self) -> scene.Scene:
        """
        Get the current scene.
        :return: The current scene instance.
        """
        return self.__current_scene