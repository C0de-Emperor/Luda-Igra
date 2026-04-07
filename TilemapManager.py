import pygame
import pytmx
import pyscroll
from Objects import Player, Object, Gate



class Tilemap(Object):
    def __init__(self, path: str):
        super().__init__(pygame.Vector2(0, 0), pygame.Vector2(0, 0), True)

        self.path:str = path

        self.tmx_data:Tilemap = pytmx.load_pygame(path)
        self.map_data:pyscroll.data.TiledMapData = pyscroll.data.TiledMapData(self.tmx_data)
        self.collisions: list[pygame.Rect] = []
        
        self._load_collisions()
        self._load_gates()
        self._load_points()
        self._load_spawn_Area()

    def _load_spawn_Area(self):
        from Objects import SpawnArea
        from Data import ENTITIES

        areas_layer = self.tmx_data.get_layer_by_name("SpawnArea")
        for area in areas_layer:
            rect = pygame.Rect(area.x, area.y, area.width, area.height)

            entityName, count, delay = area.name.split("-")

            entity = ENTITIES[entityName]

            SpawnArea(entity, int(count), int(delay), pygame.Vector2(rect.x, rect.y), pygame.Vector2(rect.width, rect.height))

    def _load_collisions(self):
        """Charge les rects de collision depuis le layer 'Collisions'"""
        try:
            collision_layer = self.tmx_data.get_layer_by_name("Collisions")
            for collision in collision_layer:
                rect = pygame.Rect(collision.x, collision.y, collision.width, collision.height)
                self.collisions.append(rect)
        except (ValueError, AttributeError):
            print("WARNING: Couche de collision 'Collisions' non trouvée dans le tilemap")

    def _load_points(self):
        try:
            points_layer = self.tmx_data.get_layer_by_name("Points")
            self.points: dict[str, pygame.Vector2] = {}
            for point in points_layer:
                self.points[point.name] = pygame.Vector2(point.x, point.y)

        except (ValueError, AttributeError):
            print(f"ERROR: 'Points' layer not found in tilemap '{self.path}'")
            return
    
    def _load_gates(self):
        gates_layer = self.tmx_data.get_layer_by_name("Gates")
        for gate in gates_layer:
            rect = pygame.Rect(gate.x, gate.y, gate.width, gate.height)

            destination, name = gate.name.split("/")

            Gate(name, destination, pygame.Vector2(rect.x, rect.y), pygame.Vector2(rect.width, rect.height), "data/Sprites/toruk_makto.png")

    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        if hasattr(self, 'group'):

            # Centre la caméra sur le joueur
            if Player.player:
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

    def GetColliders(self) -> list[pygame.Rect]:
        return self.collisions



"""
Layers




"""
