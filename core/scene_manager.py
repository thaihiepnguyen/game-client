import core.scene as Scene
from scenes.battle import BattleScene
from scenes.login import LoginScene
from core.const import *

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def _add_scene(self, name: str, scene: type[Scene.Scene]) -> None:
        """
        Add a scene to the manager.
        :param name: The name of the scene to add.
        :param scene: The scene class to add, which should inherit from Scene.Scene.
        """
        self.scenes[name] = scene(self)

    def initialize(self) -> None:
        """
        Initialize the scene manager, setting up any necessary resources.
        This method can be extended to load resources or perform setup tasks.
        """
        scenes = {
            LOGIN_SCENE: LoginScene,
            BATTLE_SCENE: BattleScene,
            # Add more scenes here as needed
        }

        for name, scene_class in scenes.items():
            self._add_scene(name, scene_class)

    def set_scene(self, name: str) -> None:
        """
        Set the current scene by name.
        :param name: The name of the scene to set as current.
        """
        if name in self.scenes:
            self.current_scene = self.scenes[name]
        else:
            raise ValueError(f"Scene '{name}' not found in SceneManager.")
    
    def get_scene(self) -> Scene.Scene:
        """
        Get the current scene.
        :return: The current scene instance.
        """
        return self.current_scene