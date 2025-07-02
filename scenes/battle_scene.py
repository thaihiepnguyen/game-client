from typing import override

from core.background.background_factory import BackgroundFactory
from core.character.character_factory import CharacterFactory
from core.scene.scene import Scene
from network.recv.arrow_packet import ArrowPacket
from network.recv.end_game_packet import EndGamePacket
from network.recv.recv_broadcast_packet import RecvBroadcastPacket
from network.send.atk_packet import AtkPacket
from network.send.def_packet import DefPacket
from network.send.move_packet import MovePacket
from sprites.characters.archer.arrow.arrow import Arrow
from sprites.health_bar.health_bar import HealthBar
from core.const import CHARACTER_REVERSIBLE_STATES, CHARACTER_WIDTH, FONT, WINDOW_HEIGHT, WINDOW_WIDTH, Colors, \
    CommandId, HEADER_SIZE, MAIN_SCENE
import pygame
from core.network.packet_header import PacketHeader
import threading


class BattleScene(Scene):
    def __init__(self, scene_manager, tcp_client):
        super().__init__(scene_manager, tcp_client)
        self.__timer_font = pygame.font.Font(FONT, 80)
        self.__timer = None
        self.__last_time = 0
        self.__result = None
        self.__is_end_game = False
        self.__ground_y = 0

        # Centralized text rendering
        self.__end_texts = self._create_end_texts()
        self.__enter_to_back_text, self.__enter_to_back_text_rect = self._render_text(
            "Press Enter to go back", 40, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80)
        )

        self.__char = self.__oppo = self.__bg = self.__side = None
        self.__bg_animation = self.__fighter = self.__opponent = None
        self.__health_bar_tl = self.__health_bar_tr = None

    def _render_text(self, text, size, center):
        font = pygame.font.Font(FONT, size)
        surface = font.render(text, True, Colors.WHITE.value)
        rect = surface.get_rect(center=center)
        return surface, rect

    def _create_end_texts(self):
        messages = {
            1: "YOU WIN!",
            2: "YOU LOST!",
            3: "DRAW!",
            4: "OPPONENT OUT!"
        }
        return {
            key: self._render_text(msg, 64, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            for key, msg in messages.items()
        }

    @override
    def on_enter(self, data: dict | None) -> None:
        self.__timer = 90
        self.__result = None
        self.__is_end_game = False

        self.__char = data.get('char', None)
        self.__oppo = data.get('oppo', None)
        self.__bg = data.get('bg', None)
        self.__side = data.get('side', None)

        self.__bg_animation = BackgroundFactory.create_background(self.__bg)
        self.__ground_y = self.__bg_animation.get_ground_y_ratio() * WINDOW_HEIGHT
        self.__fighter = CharacterFactory.create_character(self.__char)
        self.__opponent = CharacterFactory.create_character(self.__oppo)

        positions = [
            (100, 'topleft'),
            (WINDOW_WIDTH - 100 - CHARACTER_WIDTH, 'topright')
        ]
        fighter_idx, opponent_idx = (0, 1) if not self.__side else (1, 0)

        self.__fighter.set_x(positions[fighter_idx][0])
        self.__fighter.set_y(200)
        self.__opponent.set_x(positions[opponent_idx][0])
        self.__opponent.set_y(200)

        self.__health_bar_tl = HealthBar(
            pos='topleft',
            character=self.__fighter if fighter_idx == 0 else self.__opponent
        )
        self.__health_bar_tr = HealthBar(
            pos='topright',
            character=self.__fighter if fighter_idx == 1 else self.__opponent
        )

        threading.Thread(target=self.__recv_worker, daemon=True).start()

    def __recv_worker(self):
        while True:
            res = self._tcp_client.recv()
            packet_header = PacketHeader.from_bytes(res[:HEADER_SIZE])
            if packet_header.command_id == CommandId.BROADCAST.value:
                packet = RecvBroadcastPacket.from_bytes(res)
                self.__fighter.set_x(packet.x_c)
                self.__fighter.set_y(packet.y_c)
                self.__fighter.set_hp(packet.hp_c)
                self.__fighter.set_state(CHARACTER_REVERSIBLE_STATES[packet.state_c])

                self.__opponent.set_x(packet.x_o)
                self.__opponent.set_y(packet.y_o)
                self.__opponent.set_hp(packet.hp_o)
                self.__opponent.set_state(CHARACTER_REVERSIBLE_STATES[packet.state_o])

            elif packet_header.command_id == CommandId.ARROW.value:
                packet = ArrowPacket.from_bytes(res)
                arrow = Arrow(x=packet.x, y=packet.y, is_flipped=packet.direction != 1)
                target = self.__fighter if packet.owner == 1 else self.__opponent
                if hasattr(target, 'add_arrow'):
                    target.add_arrow(arrow)

            elif packet_header.command_id == CommandId.END_GAME.value:
                packet = EndGamePacket.from_bytes(res)
                self.__is_end_game = True
                self.__result = packet.result
                return

            elif packet_header.command_id == CommandId.OPPONENT_OUT.value:
                self.__is_end_game = True
                self.__result = 4
                return

    def draw(self, screen: pygame.Surface) -> None:
        if not all([self.__bg_animation, self.__fighter, self.__opponent, self.__health_bar_tl, self.__health_bar_tr]):
            return
        scaled_bg_image = pygame.transform.scale(self.__bg_animation.get_current_frame(), (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(scaled_bg_image, (0, 0))

        self.__fighter.draw(self.__ground_y, screen)
        self.__health_bar_tl.draw(screen)
        self.__opponent.draw(self.__ground_y, screen)
        self.__health_bar_tr.draw(screen)
        self.__fighter.look_at(self.__opponent)
        self.__opponent.look_at(self.__fighter)

    def handle_event(self, event: pygame.event.Event):
        if not self.__is_end_game:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.__fighter.attack_z()
                    header = PacketHeader(command_id=CommandId.ATK.value, packet_length=4)
                    packet = AtkPacket(header, atk=1)
                    self._tcp_client.send(packet.to_bytes())

                elif event.key == pygame.K_x:
                    self.__fighter.attack_x()
                    header = PacketHeader(command_id=CommandId.ATK.value, packet_length=4)
                    packet = AtkPacket(header, atk=2)
                    self._tcp_client.send(packet.to_bytes())

                elif event.key == pygame.K_c:
                    self.__fighter.attack_c()
                    header = PacketHeader(command_id=CommandId.ATK.value, packet_length=4)
                    packet = AtkPacket(header, atk=3)
                    self._tcp_client.send(packet.to_bytes())

                elif event.key == pygame.K_SPACE:
                    header = PacketHeader(command_id=CommandId.JUMP.value, packet_length=0)
                    self._tcp_client.send(header.to_bytes())
                    self.__fighter.jump()

                elif event.key == pygame.K_LEFT:
                    self.__fighter.walk_left()
                    header = PacketHeader(command_id=CommandId.MOVE.value, packet_length=4)
                    packet = MovePacket(header, x=1)
                    self._tcp_client.send(packet.to_bytes())

                elif event.key == pygame.K_RIGHT:
                    self.__fighter.walk_right()
                    header = PacketHeader(command_id=CommandId.MOVE.value, packet_length=4)
                    packet = MovePacket(header, x=2)
                    self._tcp_client.send(packet.to_bytes())

                elif event.key == pygame.K_LSHIFT:
                    self.__fighter.defend()
                    header = PacketHeader(command_id=CommandId.DEF.value, packet_length=4)
                    packet = DefPacket(header, defense=1)
                    self._tcp_client.send(packet.to_bytes())

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.__fighter.stop_movement()
                    header = PacketHeader(command_id=CommandId.MOVE.value, packet_length=4)
                    packet = MovePacket(header, x=3)
                    self._tcp_client.send(packet.to_bytes())
                elif event.key == pygame.K_LSHIFT:
                    self.__fighter.undefend()
                    header = PacketHeader(command_id=CommandId.DEF.value, packet_length=4)
                    packet = DefPacket(header, defense=0)
                    self._tcp_client.send(packet.to_bytes())
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self._scene_manager.set_scene(MAIN_SCENE)

    def update(self, screen: pygame.Surface, delta_time: float):
        if not all([self.__bg_animation, self.__fighter, self.__opponent]):
            return

        if pygame.time.get_ticks() - self.__last_time >= 1000 and not self.__is_end_game:
            self.__last_time = pygame.time.get_ticks()
            self.__timer -= 1

        self.__bg_animation.update(delta_time)
        self.__fighter.update(screen, delta_time)
        self.__opponent.update(screen, delta_time)

        timer_text = self.__timer_font.render(str(int(self.__timer)), True, Colors.WHITE.value)
        screen.blit(timer_text, (WINDOW_WIDTH // 2 - timer_text.get_width() // 2, 5))

        if self.__is_end_game and self.__result is not None:
            text_surf, text_rect = self.__end_texts.get(self.__result, (None, None))
            if text_surf and text_rect:
                screen.blit(text_surf, text_rect)
            screen.blit(self.__enter_to_back_text, self.__enter_to_back_text_rect)