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
        self.__fighter = Fighter(
            x=100, 
            y=200, 
            speed=300, 
            weight=1,
            jump_velocity=30
        )
        self.__opponent = Fighter(
            x=500, 
            y=200, 
            speed=300, 
            weight=1,
            jump_velocity=30
        )
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
        self.__opponent.draw(screen)
        self.__testBtn.draw(screen)

    @override
    def handle_event(self, event: pygame.event.Event):
        self.__testBtn.handle_event(event)

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        speed = self.__fighter.get_speed()
        ground_y = screen.get_height() * 4.075 / 5
        self.__fighter.apply_gravity(ground_y, delta_time)
        self.__opponent.apply_gravity(ground_y, delta_time)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.__fighter.move(screen, -speed * delta_time) # each frame move speed * delta_time pixels
        if keys[pygame.K_RIGHT]:
            self.__fighter.move(screen, speed * delta_time)
        if keys[pygame.K_SPACE]:
            self.__fighter.jump()