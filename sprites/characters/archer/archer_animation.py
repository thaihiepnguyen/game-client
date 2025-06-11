from core.character.character_animation import CharacterAnimation
from typing import override
from core.animation.animation import Animation
from core.animation.sprite import Sprite
class ArcherAnimation(CharacterAnimation):
    @override
    def _load_walk_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/archer/Sprites/Walk.png",
            w=128,
            h=128,
            count=8,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_jump_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/archer/Sprites/Jump.png",
            w=128,
            h=128,
            count=9,
        )
        return Animation(sprite=sprite, frame_duration=0.05)

    @override
    def _load_idle_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/archer/Sprites/Idle.png",
            w=128,
            h=128,
            count=9,
        )
        return Animation(sprite=sprite, frame_duration=0.05)

    @override
    def _load_attack_z_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/archer/Sprites/Attack_1.png",
            w=128,
            h=128,
            count=5,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_attack_x_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/archer/Sprites/Attack_2.png",
            w=128,
            h=128,
            count=5,
        )
        return Animation(sprite=sprite, frame_duration=0.05)

    @override
    def _load_hit_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/archer/Sprites/Hurt.png",
            w=128,
            h=128,
            count=3,
        )
        return Animation(sprite=sprite, frame_duration=0.5)

    @override
    def _load_death_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/characters/archer/Sprites/Dead.png",
            w=128,
            h=128,
            count=5,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_def_animation(self) -> Animation | None:
        return None