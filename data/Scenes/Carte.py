from Objects import Player, ObjectWithCollider
from SceneManager import Scene
from pygame import Vector2
from TilemapManager import Tilemap

def load(scene: Scene):
    scene.tilemap = Tilemap("data/Tilemaps/carte.tmx")

    Player(
        Scene.currentScene.tilemap.spawn_point, 
        Vector2(50, 50),
        r"player.png",
        speed = 300
    )

    ObjectWithCollider(Vector2(500, 500), Vector2(200, 200))
