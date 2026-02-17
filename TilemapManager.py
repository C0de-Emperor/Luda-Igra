import pygame
import pytmx
import pyscroll
from Objects import Player, Object



class Tilemap(Object):
    def __init__(self, path: str):
        from SceneManager import Scene
        super().__init__(pygame.Vector2(0, 0))

        self.tmx_data = pytmx.load_pygame(path)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.collisions: list[pygame.Rect] = []
        
        self._load_collisions()
        self._load_spawn_point()

        Scene.currentScene.tilemap = self

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

    def GetColliders(self) -> list[pygame.rect.Rect]:
        return self.collisions




