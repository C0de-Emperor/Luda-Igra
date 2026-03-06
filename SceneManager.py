from Objects import Object
import pygame
import pyscroll
from TilemapManager import Tilemap

class Scene:
    currentScene = None
    
    def __init__(self, name: str): # passer une tilemap ?
        self.name: str = name
        self.objects: list["Object"] = []
        

    def GetAllColliders(self) -> list[pygame.rect.Rect]:
        colliders = []

        for obj in self.objects:
            colliders.extend(obj.GetColliders())

        return colliders

    def load(self):
        """Initialise la Scene"""
        from Main import SCREEN

        Scene.currentScene = self

        self.tilemap = Tilemap(f"data/Tilemaps/{self.name}.tmx")

        self.tilemap.map_layer = pyscroll.orthographic.BufferedRenderer(
            self.tilemap.map_data, SCREEN.get_size()
        )
        self.tilemap.group = pyscroll.PyscrollGroup(self.tilemap.map_layer, default_layer=0)

SCENES = {
    "Map" : Scene("carte")
}
