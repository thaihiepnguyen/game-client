import pygame
from core.scene import Scene
from core.scene_manager import SceneManager

class LoginScene(Scene):
    def __init__(self, scene_manager: SceneManager):
        super().__init__(scene_manager)

        self.background_color = (0, 0, 0) 
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen: pygame.Surface):
        screen.fill(self.background_color)
        text = self.font.render("Login Scene", True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            pygame.quit()

    def update(self, delta_time: float):
        pass
