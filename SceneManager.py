from Objects import Object
import pygame
import pyscroll
import importlib.util
import sys
import os

class Scene:
    currentScene = None
    
    def __init__(self, name: str):
        self.name: str = name
        self.path = f"data/Scenes/{name}.py"

        module_name = os.path.splitext(os.path.basename(self.path))[0]

        spec = importlib.util.spec_from_file_location(module_name, self.path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        self.module = module
        if not hasattr(self.module, "load"):
            raise Exception(f"the module : {self.path} has no function load")

        self.tilemap = None
        self.objects: list["Object"] = []

    def GetAllColliders(self) -> list[pygame.rect.Rect]:
        colliders = []

        for obj in self.objects:
            colliders.extend(obj.GetColliders())

        return colliders

    def load(self, screen: pygame.surface.Surface):
        """Initialise la Scene"""
        Scene.currentScene = self

        self.module.load(self)

        if not self.tilemap:
            return

        self.tilemap.map_layer = pyscroll.orthographic.BufferedRenderer(
            self.tilemap.map_data, screen.get_size()
        )
        self.tilemap.group = pyscroll.PyscrollGroup(self.tilemap.map_layer, default_layer=0)

class Biome:
    """Regroupement de Scenes"""
    def __init__(self, scenes: list[Scene], automatList: list[list[int]] = []):
        self.scenes: list[Scene] = scenes
        self.automatList = automatList
   
    def load(self, index: int , screen: pygame.surface.Surface):
        Biome.currentBiome = self

        self.scenes[index].load(screen)
        #Tilemap.loadTilemap(self.scenes[index].tilemap, screen)

class BiomeManager  :
    biomeManager=None

    def __init__(self, biomesDict:dict):
        self.biomesDict:dict=biomesDict
        self.currentBiome:Biome=None

        BiomeManager.biomeManager = self
    
    def loadBiome(self, biomeName):
        try:
            self.currentBiome=self.biomesDict[biomeName]
        except:
            print(f"no biome matching for biome name: {biomeName}")

biome1 = Biome([
        Scene("Carte"),
        Scene("Donjon")
    ])

BiomeManager({"defaultBiome": biome1})