import pygame
import pytmx
import pyscroll
from Objects import Player, Object


class Tilemap(Object):
    currentTilemap = None

    def __init__(self, tilemapPath: str):
        super().__init__(pygame.Vector2(0, 0))

        self.tmx_data = pytmx.load_pygame(tilemapPath)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.collisions: list[pygame.Rect] = []
        
        self._load_collisions()
        self._load_spawn_point()

    def _load_collisions(self):
        """Charge les rects de collision depuis le layer 'Collisions'"""
        try:
            collision_layer = self.tmx_data.get_layer_by_name("Collisions")
            for collision in collision_layer:
                rect = pygame.Rect(collision.x, collision.y, collision.width, collision.height)
                self.collisions.append(rect)
        except (ValueError, AttributeError):
            print("WARNING: Couche de collision 'Collisions' non trouvée dans le tilemap")

    def _load_spawn_point(self):
        try:
            spawn_obj = self.tmx_data.get_object_by_name("spawnPoint")
            self.spawn_point = pygame.Vector2(spawn_obj.x, spawn_obj.y)
        except (ValueError, AttributeError):
            print("WARNING: Spawn point 'spawnPoint' non trouvé dans le tilemap")
            self.spawn_point = pygame.Vector2(0, 0)

    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        if hasattr(self, 'group') and hasattr(self, 'map_layer'):
            # Centre la caméra sur le joueur
            self.group.center(Player.player.rect)
            # Dessine le tilemap
            self.group.draw(screen)

            # Récupère l'offset de la caméra
            view_rect = self.group.view
            self.camera_offset = pygame.Vector2(view_rect.x, view_rect.y)
            
            if debug:
                for collision_rect in self.collisions:
                    screen_rect = collision_rect.move(-self.camera_offset.x, -self.camera_offset.y)
                    pygame.draw.rect(screen, (0, 255, 0), screen_rect, 2)

    @staticmethod
    def loadTilemap(tilemap: "Tilemap", screen: pygame.surface.Surface):
        """Initialise le rendu du tilemap avec pyscroll"""
        Tilemap.currentTilemap = tilemap
        tilemap.map_layer = pyscroll.orthographic.BufferedRenderer(
            tilemap.map_data, screen.get_size()
        )
        tilemap.group = pyscroll.PyscrollGroup(tilemap.map_layer, default_layer=0)


class Biome:
    """Regroupement de Tilemap"""
    currentBiome = None

    def __init__(self, biomePath: str, tilemapNames: list[str], tileMapAutomatMatrix=None):
        self.biome_path = biomePath
        self.tilemaps: list[Tilemap] = []
        
        for name in tilemapNames:
            path = f"data/tilemaps/{name}.tmx"
            self.tilemaps.append(Tilemap(path))

    @staticmethod
    def loadBiome(biome: "Biome", tilemap: "Tilemap", screen: pygame.surface.Surface):
        Biome.currentBiome = biome

        Tilemap.loadTilemap(tilemap, screen)
