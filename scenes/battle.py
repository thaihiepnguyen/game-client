from typing import override

from core.scene import Scene
from core.const import BACKGROUND_IMAGE
from sprites.fighter import Fighter
from core.gui.button import Button
import pygame

class BattleScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.__bg_image = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        self.__fighter = Fighter(x=100, y=100)
        self.__testBtn = Button(
            text="Test Button",
            font=pygame.font.Font(None, 36),
            pos=(50, 50),
            size=(200, 50),
            color=(255, 0, 0)
        )

        self.__testBtn.on_click(lambda event: print("Button clicked!"))


    @override
    def draw(self, screen: pygame.Surface) -> None:
        scaled_bg_image = pygame.transform.scale(self.__bg_image, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_bg_image, (0, 0))
        self.__fighter.draw(screen)
        self.__testBtn.draw(screen)

    @override
    def handle_event(self, event: pygame.event.Event):
        self.__testBtn.handle_event(event)

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        speed = 200
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.__fighter.move(screen, -speed * delta_time, 0)
        if keys[pygame.K_d]:
            self.__fighter.move(screen, speed * delta_time, 0)