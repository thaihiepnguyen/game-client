from core.character.character_animation import CharacterAnimation
from typing import override
from core.animation.animation import Animation
from core.animation.sprite import Sprite
from typing import Dict


class GorgonAnimation(CharacterAnimation):
    @override
    def _set_scale(self) -> float:
        return 2

    @override
    def _load_walk_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/gorgon/Sprites/Walk.png",
            w=128,
            h=128,
            count=13,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_jump_animation(self) -> Animation | None:
        return None

    @override
    def _load_idle_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/gorgon/Sprites/Idle.png",
            w=128,
            h=128,
            count=7,
        )
        return Animation(sprite=sprite, frame_duration=0.05)

    @override
    def _load_attack_z_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/gorgon/Sprites/Special.png",
            w=128,
            h=128,
            count=5,
        )
        return Animation(sprite=sprite, frame_duration=0.07)

    @override
    def _load_attack_x_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/gorgon/Sprites/Attack_3.png",
            w=128,
            h=128,
            count=10,
        )
        return Animation(sprite=sprite, frame_duration=0.07)

    @override
    def _load_hit_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/gorgon/Sprites/Hurt.png",
            w=128,
            h=128,
            count=3,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_death_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/gorgon/Sprites/Dead.png",
            w=128,
            h=128,
            count=3,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_def_animation(self) -> Animation | None:
        return None