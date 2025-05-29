import core.scene as Scene


class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, name: str, scene: Scene.Scene):
        """
        Add a scene to the manager.

        Args:
            name (str): The name of the scene.
            scene (Scene.Scene): The scene instance to add.
        """
        self.scenes[name] = scene(self)

    def set_scene(self, name: str):
        """
        Set the current scene by name.

        Args:
            name (str): The name of the scene to set as current.
        """
        if name in self.scenes:
            self.current_scene = self.scenes[name]
        else:
            raise ValueError(f"Scene '{name}' not found in SceneManager.")
    
    def get_scene(self) -> Scene.Scene:
        """
        Get the current scene.

        Returns:
            Scene.Scene: The current scene instance.
        """
        return self.current_scene