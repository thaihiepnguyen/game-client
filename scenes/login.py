from typing import override

import pygame
from core.scene.scene import Scene

class LoginScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)

        self.background_color = (0, 0, 0) 
        self.font = pygame.font.Font(None, 36)

    @override
    def draw(self, screen: pygame.Surface):
        screen.fill(self.background_color)
        text = self.font.render("Login Scene", True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

    @override
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            print(f"Key pressed: {pygame.key.name(event.key)}")

    @override
    def update(self, screen: pygame.Surface, delta_time: float):
        pass
