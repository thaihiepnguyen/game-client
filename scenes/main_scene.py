
import pygame
from core.const import FONT, MAIN_BACKGROUND, WINDOW_HEIGHT, WINDOW_WIDTH
from core.scene.scene import Scene

class MainScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.image = pygame.image.load(MAIN_BACKGROUND).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.start_game_text = pygame.font.Font(FONT, 64).render("START GAME", True, (255, 255, 255))
        self.start_game_text_rect = self.start_game_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))

        self.play_game_text = pygame.font.Font(FONT, 40).render("1. Play", True, (255, 255, 255))
        self.play_game_text_rect = self.play_game_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.quit_game_text = pygame.font.Font(FONT, 40).render("2. Quit", True, (255, 255, 255))
        self.quit_game_text_rect = self.quit_game_text.get_rect(center=(WINDOW_WIDTH // 2, 0))
        self.quit_game_text_rect.top = self.play_game_text_rect.bottom + 10

        self.arrow = pygame.font.Font(FONT, 80).render(">", True, (255, 255, 255))
        self.arrow_rect = self.arrow.get_rect(center=(self.play_game_text_rect.left - 30, self.play_game_text_rect.centery))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (0, 0))

        screen.blit(self.start_game_text, self.start_game_text_rect)
        screen.blit(self.play_game_text, self.play_game_text_rect)
        screen.blit(self.quit_game_text, self.quit_game_text_rect)
        screen.blit(self.arrow, self.arrow_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.arrow_rect.centery = self.quit_game_text_rect.centery

    def update(self, screen: pygame.Surface, delta_time: float):
        pass
