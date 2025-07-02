from core.character.character_animation import CharacterAnimation
from typing import override
from core.animation.animation import Animation
from core.animation.sprite import Sprite


class VampireAnimation(CharacterAnimation):
    @override
    def _set_scale(self) -> float:
        return 1.6

    def _load_walk_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/vampire/Sprites/Walk.png",
            w=128,
            h=128,
            count=8,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_jump_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/vampire/Sprites/Jump.png",
            w=128,
            h=128,
            count=7,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_idle_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/vampire/Sprites/Idle.png",
            w=128,
            h=128,
            count=5,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_attack_z_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/vampire/Sprites/Attack_1.png",
            w=128,
            h=128,
            count=5,
        )
        return Animation(sprite=sprite, frame_duration=0.1)


    def _load_attack_x_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/vampire/Sprites/Attack_2.png",
            w=128,
            h=128,
            count=3,
        )
        return Animation(sprite=sprite, frame_duration=0.05)

    def _load_attack_c_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/vampire/Sprites/Attack_3.png",
            w=128,
            h=128,
            count=4,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_hit_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/vampire/Sprites/Hurt.png",
            w=128,
            h=128,
            count=1,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_death_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/vampire/Sprites/Dead.png",
            w=128,
            h=128,
            count=8,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_def_animation(self) -> Animation | None:
        sprite = Sprite(
            dir="assets/images/characters/vampire/Sprites/Protect.png",
            w=128,
            h=128,
            count=2,
        )
        return Animation(sprite=sprite, frame_duration=0.1)