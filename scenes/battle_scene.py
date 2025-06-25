from typing import override

from core.background.background_factory import BackgroundFactory
from core.character.character import Character
from core.character.character_factory import CharacterFactory
from core.scene.scene import Scene
from network.recv.recv_broadcast_packet import RecvBroadcastPacket
from sprites.health_bar.health_bar import HealthBar
from core.const import CHARACTER_REVERSIBLE_STATES, CHARACTER_STATES, CHARACTER_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, \
    CommandId, HEADER_SIZE, MAIN_SCENE
import pygame
from network.send.send_broadcast_packet import SendBroadcastPacket
from core.network.packet_header import PacketHeader
import threading

class BattleScene(Scene):
    def __init__(self, scene_manager, tcp_client):
        super().__init__(scene_manager, tcp_client)
        self.__char = self.__oppo = self.__bg = self.__side = None
        self.__bg_animation = self.__fighter = self.__opponent = None
        self.__health_bar_tl = self.__health_bar_tr = None
        self.__opponent_arrow = self.__fighter_arrow = None

    @override
    def _on_enter(self, data: dict | None) -> None:
        self.__char = data.get('char', None)
        self.__oppo = data.get('oppo', None)
        self.__bg = data.get('bg', None)
        self.__side = data.get('side', None)

        self.__bg_animation = BackgroundFactory.create_background(self.__bg)
        self.__fighter = CharacterFactory.create_character(self.__char)
        self.__opponent = CharacterFactory.create_character(self.__oppo)
        # Set initial positions and health bars based on side
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

    def _send_broadcast_packet(self, data: dict):
        header = PacketHeader(CommandId.BROADCAST.value, 4 * 4 + 1) 
        packet = SendBroadcastPacket(
            header=header,
            x=data['x'],
            y=data['y'],
            hp=data['hp'],
            flipped=int(data['flipped']),
            state=CHARACTER_STATES[data['state']]
        )
        self._tcp_client.send(packet.to_bytes())

    def __recv_worker(self):
        """
        This method is intended to run in a separate thread to handle network communication.
        :return:
        """
        while True:
            res = self._tcp_client.recv()
            packet_header = PacketHeader.from_bytes(res[:HEADER_SIZE])
            if packet_header.command_id == CommandId.BROADCAST.value:
                packet = RecvBroadcastPacket.from_bytes(res)
                self.__opponent.set_x(packet.x)
                self.__opponent.set_y(packet.y)
                self.__opponent.set_hp(packet.hp)
                self.__opponent.set_flipped(packet.flipped)
                self.__opponent.set_state(CHARACTER_REVERSIBLE_STATES[packet.state])
            elif packet_header.command_id == CommandId.OPPONENT_OUT.value:
                self._scene_manager.set_scene(MAIN_SCENE)
                return

    def __update_arrow(self, arrow_attr: str, owner: Character, screen: pygame.Surface, delta_time: float):
        """
        Update and draw the arrow for the given owner character.
        """
        arrow = getattr(self, arrow_attr, None)
        if arrow is None and hasattr(owner, 'get_arrow'):
            arrow = owner.get_arrow()
            setattr(self, arrow_attr, arrow)
        if arrow:
            arrow.update(delta_time)
            if arrow.get_rect().x < 0 or arrow.get_rect().x > WINDOW_WIDTH:
                setattr(self, arrow_attr, None)
            else:
                arrow.draw(screen)
        return arrow

    def draw(self, screen: pygame.Surface) -> None:
        if not all([self.__bg_animation, self.__fighter, self.__opponent]): return
        scaled_bg_image = pygame.transform.scale(self.__bg_animation.get_current_frame(), (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(scaled_bg_image, (0, 0))
        self.__fighter.draw(screen)
        self.__health_bar_tl.draw(screen)
        self.__opponent.draw(screen)
        self.__health_bar_tr.draw(screen)
        self.__fighter.look_at(self.__opponent)
        self.__opponent.look_at(self.__fighter)

    def handle_event(self, event: pygame.event.Event):
        if self.__fighter is None: return
        self.__fighter.handle_event(event)

    def update(self, screen: pygame.Surface, delta_time: float):
        if not all([self.__bg_animation, self.__fighter, self.__opponent]): return
        self.__bg_animation.update(delta_time)

        ground_y = WINDOW_HEIGHT * self.__bg_animation.get_ground_y_ratio()
        self.__fighter.apply_gravity(ground_y, delta_time)
        self.__opponent.apply_gravity(ground_y, delta_time)

        if self.__fighter.is_dead():
            pass  # Game end logic placeholder

        fighter_hurt_box = self.__fighter.get_rect()
        opponent_atk_hitbox = self.__opponent.get_attack_hitbox(screen)
        get_kick_away_box = getattr(self.__opponent, 'get_kick_away_box', None)

        # Damage logic
        if getattr(self.__opponent, 'get_kick_away_box', None):
            get_kick_away_box = self.__opponent.get_kick_away_box()
            if get_kick_away_box and get_kick_away_box.colliderect(fighter_hurt_box) and not self.__fighter.is_defend():
                self.__fighter.take_damage(int(max(0, self.__opponent.get_atk() - self.__fighter.get_armor()), 200))

        if opponent_atk_hitbox and opponent_atk_hitbox.colliderect(fighter_hurt_box) and not self.__fighter.is_defend():
            intersection = opponent_atk_hitbox.clip(fighter_hurt_box)
            damage_ratio = intersection.width / self.__fighter.get_rect().width
            damage = self.__opponent.get_atk() * damage_ratio - self.__fighter.get_armor()
            self.__fighter.take_damage(int(max(0, damage)))

        # Arrow logic
        self.__opponent_arrow = self.__update_arrow('__opponent_arrow', self.__opponent, screen, delta_time)
        self.__fighter_arrow = self.__update_arrow('__fighter_arrow', self.__fighter, screen, delta_time)

        if self.__opponent_arrow and self.__opponent_arrow.get_rect().colliderect(
                fighter_hurt_box) and not self.__fighter.is_defend():
            damage = self.__opponent_arrow.get_damage() - self.__fighter.get_armor()
            self.__fighter.take_damage(int(max(0.0, damage)))

        self.__fighter.update(screen, delta_time)
        self.__opponent.update(screen, delta_time)

        self._send_broadcast_packet(self.__fighter.get_broadcast_data())
        self.__fighter.handle_input(pygame.key.get_pressed(), delta_time)