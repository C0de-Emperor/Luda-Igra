from Objects import Player, ObjectWithCollider
from SceneManager import Scene
from pygame import Vector2
from TilemapManager import Tilemap

def load(scene: Scene):
    scene.tilemap = Tilemap("data/Tilemaps/carte.tmx")

    Player(
        Scene.currentScene.tilemap.spawn_point, 
        Vector2(100, 100),
        r"data/sprites/toruk_makto.png",
        speed = 300
    )

