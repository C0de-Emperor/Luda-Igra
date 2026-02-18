from Objects import Player
from SceneManager import Scene
from pygame import Vector2
from TilemapManager import Tilemap

def load(scene: Scene):
    scene.tilemap = Tilemap("data/Tilemaps/Donjon.tmx")

    Player(
        Scene.currentScene.tilemap.spawn_point,
        Vector2(50, 50),
        r"data/sprites/toruk_makto.png",
        speed = 300
    )
