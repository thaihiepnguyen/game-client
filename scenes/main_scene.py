
import pygame
from core.const import BATTLE_SCENE, FONT, MAIN_BACKGROUND, WINDOW_HEIGHT, WINDOW_WIDTH, Colors, CommandId
from core.network.packet_header import PacketHeader
from core.scene.scene import Scene
from network.send.wait_for_match_packet import WaitForMatchPacket
from network.recv.room_packet import RoomPacket
import threading

class MainScene(Scene):
    def __init__(self, scene_manager, tcp_client):
        super().__init__(scene_manager, tcp_client)
        self.cnt = 0
        self.is_waiting_for_match = False
        
        self.image = pygame.image.load(MAIN_BACKGROUND).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.start_game_text = pygame.font.Font(FONT, 64).render("START GAME", True, Colors.WHITE.value)
        self.start_game_text_rect = self.start_game_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))

        self.wait_for_match_text = pygame.font.Font(FONT, 40).render("Waiting for match...", True, Colors.WHITE.value)
        self.wait_for_match_text_rect = self.wait_for_match_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.play_game_text = pygame.font.Font(FONT, 40).render("1. Play", True, Colors.WHITE.value)
        self.play_game_text_rect = self.play_game_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.quit_game_text = pygame.font.Font(FONT, 40).render("2. Quit", True, Colors.WHITE.value)
        self.quit_game_text_rect = self.quit_game_text.get_rect(center=(WINDOW_WIDTH // 2, 0))
        self.quit_game_text_rect.top = self.play_game_text_rect.bottom + 10

        self.option_texts = [self.play_game_text_rect, self.quit_game_text_rect]

        self.arrow = pygame.font.Font(FONT, 80).render(">", True, Colors.WHITE.value)
        self.arrow_rect = self.arrow.get_rect(center=(self.play_game_text_rect.left - 30, self.play_game_text_rect.centery))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (0, 0))

        if self.is_waiting_for_match:
            screen.blit(self.wait_for_match_text, self.wait_for_match_text_rect)
        else:
            screen.blit(self.start_game_text, self.start_game_text_rect)
            screen.blit(self.play_game_text, self.play_game_text_rect)
            screen.blit(self.quit_game_text, self.quit_game_text_rect)
            screen.blit(self.arrow, self.arrow_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.cnt = (self.cnt + 1) % len(self.option_texts)
                self.arrow_rect.centery = self.option_texts[self.cnt].centery
            elif event.key == pygame.K_UP:
                self.cnt = (self.cnt - 1) % len(self.option_texts)
                self.arrow_rect.centery = self.option_texts[self.cnt].centery
            elif event.key == pygame.K_RETURN:
                if self.cnt == 0:
                    self.is_waiting_for_match = True
                    header = PacketHeader(command_id=CommandId.WAIT_FOR_MATCH.value, packet_length=0)
                    packet = WaitForMatchPacket(header)
                    self._tcp_client.send(packet.to_bytes())

                    threading.Thread(target=self.__recv_worker).start()
                elif self.cnt == 1:
                    pygame.quit()
                    exit()

    def update(self, screen: pygame.Surface, delta_time: float):
        pass

    def __recv_worker(self):
        """
        This method is intended to run in a separate thread to handle network communication.
        It can be used to listen for incoming packets or send packets without blocking the main thread.
        """
        while True:
            res = self._tcp_client.recv()
            if res:
                packet = RoomPacket.from_bytes(res)
                if packet.header.command_id == CommandId.WAIT_FOR_MATCH.value:
                    self.is_waiting_for_match = False
                    self._scene_manager.set_scene(BATTLE_SCENE, {
                        'char': packet.char,
                        'oppo': packet.oppo,
                        'bg': packet.bg,
                        'side': packet.side
                    })
                    return