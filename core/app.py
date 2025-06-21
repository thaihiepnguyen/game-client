import sys

import pygame

from core.const import *
from core.scene.scene_manager import SceneManager

class Application:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        sound1 = pygame.mixer.Sound(SOUND_BACKGROUND)
        sound1.play(-1)
        self.__screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        self.__clock = pygame.time.Clock()
        self.__scene_manager = SceneManager()
        self.__scene_manager.initialize()
        self.__scene_manager.set_scene(BATTLE_SCENE)


    def run(self):
        """
        Main loop of the application.
        This method handles events, updates the current scene, and draws it to the screen.
        """
        while True:
            scene = self.__scene_manager.get_scene()
            for event in pygame.event.get():
                scene.handle_event(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw backgrounds
            scene.draw(self.__screen)

            # Update the scene
            scene.update(self.__screen, self.__clock.get_time() / 1000.0)

            pygame.display.flip()
            self.__clock.tick(LOCK_FPS)