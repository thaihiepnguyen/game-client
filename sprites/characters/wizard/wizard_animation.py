from core.character.character_animation import CharacterAnimation
from typing import override
from core.animation.animation import Animation
from core.animation.sprite import Sprite


class WizardAnimation(CharacterAnimation):
    @override
    def _set_scale(self) -> float:
        return 2

    def _load_walk_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/wizard/Sprites/Walk.png",
            w=128,
            h=128,
            count=7,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_jump_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/wizard/Sprites/Jump.png",
            w=128,
            h=128,
            count=8,
        )
        return Animation(sprite=sprite, frame_duration=0.04)

    def _load_idle_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/wizard/Sprites/Idle.png",
            w=128,
            h=128,
            count=8,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_attack_z_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/wizard/Sprites/Attack_1.png",
            w=128,
            h=128,
            count=7,
        )
        return Animation(sprite=sprite, frame_duration=0.05)


    def _load_attack_x_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/wizard/Sprites/Attack_2.png",
            w=128,
            h=128,
            count=9,
        )
        return Animation(sprite=sprite, frame_duration=0.05)

    def _load_attack_c_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/wizard/Sprites/Magic_sphere.png",
            w=128,
            h=128,
            count=16,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_hit_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/wizard/Sprites/Hurt.png",
            w=128,
            h=128,
            count=4,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_death_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/wizard/Sprites/Dead.png",
            w=128,
            h=128,
            count=4,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    def _load_def_animation(self) -> Animation | None:
        return None