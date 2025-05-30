from core.scene import Scene
from core.const import BACKGROUND_IMAGE
from sprites.fighter import Fighter
import pygame

class BattleScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.bg_image = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        self.fighter = Fighter(100, 100)

    def draw(self, screen: pygame.Surface) -> None:
        scaled_bg_image = pygame.transform.scale(self.bg_image, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_bg_image, (0, 0))
        self.fighter.draw(screen)

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, screen: pygame.Surface, delta_time: float):
        speed = 200
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.fighter.move(screen, -speed * delta_time, 0)
        if keys[pygame.K_d]:
            self.fighter.move(screen, speed * delta_time, 0)