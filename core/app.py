import pygame
import sys
from core.scene_manager import SceneManager
from core.const import LOCK_FPS, BACKGROUND_IMAGE, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, LOGIN_SCENE


class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.scene_manager = SceneManager()
        self._load_scenes()

        self.scene_manager.set_scene(LOGIN_SCENE)
    
    def _load_scenes(self):
        """
        Load all scenes into the scene manager.
        This method should be called to initialize the scenes.
        """
        from scenes.login import LoginScene
        self.scene_manager.add_scene(LOGIN_SCENE, LoginScene)
        # Add more scenes as needed
        # self.scene_manager.add_scene("main_menu", MainMenuScene())

    def run(self):
        """
        Main loop of the application.
        This method handles events, updates the current scene, and draws it to the screen.
        """
        while True:
            scene = self.scene_manager.get_scene()
            for event in pygame.event.get():
                scene.handle_event(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw background
            scene.draw(self.screen)

            # Update the scene
            scene.update(self.clock.get_time() / 1000.0)


            pygame.display.flip()
            self.clock.tick(LOCK_FPS)