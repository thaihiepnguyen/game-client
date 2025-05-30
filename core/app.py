import sys

import pygame

from core.const import *
from core.scene_manager import SceneManager

class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()
        self.scene_manager = SceneManager()
        self.scene_manager.initialize()
        self.scene_manager.set_scene(BATTLE_SCENE)


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
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # Draw background
            scene.draw(self.screen)

            # Update the scene
            scene.update(self.screen, self.clock.get_time() / 1000.0)

            pygame.display.flip()
            self.clock.tick(LOCK_FPS)