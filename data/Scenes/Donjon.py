from Objects import Player
from SceneManager import Scene
from pygame import Vector2
from TilemapManager import Tilemap

def load(scene: Scene):
    #scene.tilemap = Tilemap("data/Tilemaps/Donjon.tmx")

    Player(
        #Scene.currentScene.tilemap.spawn_point,
        Vector2(0, 0),
        Vector2(50, 50),
        r"player.png",
        speed = 300
    )
