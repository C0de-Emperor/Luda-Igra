import pygame
import pyscroll

class Scene:
    currentScene = None
    
    def __init__(self, name: str):
        from Objects import Object

        self.name: str = name
        self.objects: list["Object"] = []
        

    def GetAllColliders(self) -> list[pygame.rect.Rect]:
        colliders = []

        for obj in self.objects:
            colliders.extend(obj.GetColliders())

        return colliders

    def load(self, point: str):
        """Initialise la Scene"""
        from Main import SCREEN
        from TilemapManager import Tilemap
        from Objects import Player

        objectsToKeep = []

        if Scene.currentScene:
            # objets à conserver
            objectsToKeep = [obj for obj in Scene.currentScene.objects if obj.destroyOnLoad == False]

            Scene.currentScene.objects = []


        Scene.currentScene = self
        
        self.tilemap = Tilemap(f"data/Tilemaps/{self.name}.tmx")

        # Mettre le tilemap en premier pour qu'il soit rendu avant les autres objets
        self.objects.extend(objectsToKeep)

        if Player.player:
            if point not in self.tilemap.points.keys():
                print(f"ERROR : '{point}' not in '{self.tilemap.path}' points")
                return

            Player.player.position = self.tilemap.points[point]
            Player.player._update_rect()


        self.tilemap.map_layer = pyscroll.orthographic.BufferedRenderer(
            self.tilemap.map_data, SCREEN.get_size()
        )
        self.tilemap.group = pyscroll.PyscrollGroup(self.tilemap.map_layer, default_layer=0)

SCENES = {
    "carte" : Scene("carte"),
    "dungeon": Scene("donjon")
}
