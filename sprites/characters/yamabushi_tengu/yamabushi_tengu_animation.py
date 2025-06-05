from core.character.character_animation import CharacterAnimation
from typing import override
from core.animation.animation import Animation
from core.animation.sprite import Sprite


class YamabushiTenguAnimation(CharacterAnimation):
    @override
    def _load_run_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/yamabushi_tengu/Sprites/Run.png",
            w=128,
            h=128,
            count=8,
        )
        return Animation(sprite=sprite, frame_duration=0.1)
    
    @override
    def _load_walk_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/yamabushi_tengu/Sprites/Walk.png",
            w=128,
            h=128,
            count=8,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_jump_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/yamabushi_tengu/Sprites/Jump.png",
            w=128,
            h=128,
            count=15,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_idle_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/yamabushi_tengu/Sprites/Idle_2.png",
            w=128,
            h=128,
            count=5,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_attack_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/yamabushi_tengu/Sprites/Attack_2.png",
            w=128,
            h=128,
            count=6,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_hit_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/yamabushi_tengu/Sprites/Hurt.png",
            w=128,
            h=128,
            count=3,
        )
        return Animation(sprite=sprite, frame_duration=0.1)

    @override
    def _load_death_animation(self) -> Animation:
        sprite = Sprite(
            dir="assets/images/yamabushi_tengu/Sprites/Dead.png",
            w=128,
            h=128,
            count=6,
        )
        return Animation(sprite=sprite, frame_duration=0.1)