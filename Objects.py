import pygame
from pygame import Vector2
import os


KEYS_MOVEMENT = {
    pygame.K_z: Vector2(0, -1),
    pygame.K_s: Vector2(0, 1),
    pygame.K_q: Vector2(-1, 0),
    pygame.K_d: Vector2(1, 0),
}


class Object:
    def __init__(self, position: Vector2):
        from SceneManager import Scene

        self.position: Vector2 = position
        Scene.currentScene.objects.append(self)

    def Update(self, dt):
        pass

    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        pass

    def Destroy(self):
        if self in Object.instances:
            Object.instances.remove(self)
            del self

    def GetColliders(self) -> list[pygame.rect.Rect]:
        return []

    def LoadSprite(self, sprite: str):
        if isinstance(sprite, str):
            if not os.path.exists(sprite):
                raise FileNotFoundError(f"Image not found: {sprite}")
            self.sprite = pygame.image.load(sprite).convert_alpha()
        elif isinstance(sprite, pygame.Surface):
            self.sprite = sprite
        else:

            raise TypeError(f"Unsupported image type: {type(sprite)}")


class Player(Object):
    player = None

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, sprite: str, speed: float = 300):
        self.speed = speed
        self.size = size

        super().__init__(position)
        self.LoadSprite(sprite)
        
        self.rect = pygame.Rect(0, 0, size.x, size.y)
        self._update_rect()

        Player.player = self

    def _update_rect(self):
        """Synchronise le rect avec la position (centré)."""
        self.rect.center = (int(self.position.x), int(self.position.y))

    def _get_movement_direction(self) -> Vector2:
        """Retourne la direction de déplacement basée sur les touches."""
        direction = Vector2(0, 0)
        keys = pygame.key.get_pressed()
        
        for key, movement in KEYS_MOVEMENT.items():
            if keys[key]:
                direction += movement
        
        if direction.length_squared() > 0:
            direction = direction.normalize()
        
        return direction

    def _check_collision(self, walls: list[pygame.Rect], axis: str) -> bool:
        """
        Vérifie les collisions sur un axe.
        Retourne True si collision détectée.
        """
        for wall in walls:
            if self.rect.colliderect(wall):
                if axis == "x":
                    # Ajuste la position X selon la direction
                    if self.position.x < wall.centerx:
                        self.position.x = wall.left - self.rect.width / 2
                    else:
                        self.position.x = wall.right + self.rect.width / 2
                else:  # axis == "y"
                    # Ajuste la position Y selon la direction
                    if self.position.y < wall.centery:
                        self.position.y = wall.top - self.rect.height / 2
                    else:
                        self.position.y = wall.bottom + self.rect.height / 2
                
                self._update_rect()
                return True
        return False

    def Update(self, dt):
        from SceneManager import Scene
        
        if Scene.currentScene is None:
            return
        
        direction = self._get_movement_direction()
            
        colliders = Scene.currentScene.GetAllColliders()

        # Déplacement et collision en X
        if direction.x != 0:
            self.position.x += direction.x * self.speed * dt
            self._update_rect()
            self._check_collision(colliders, "x")

        # Déplacement et collision en Y
        if direction.y != 0:
            self.position.y += direction.y * self.speed * dt
            self._update_rect()
            self._check_collision(colliders, "y")

    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        # Scale le sprite à la bonne taille
        scaled_sprite = pygame.transform.scale(self.sprite, (int(self.size.x), int(self.size.y)))
        
        # Applique l'offset de la caméra pour l'affichage (même offset que pyscroll)
        from SceneManager import Scene
        screen_rect = self.rect.copy()
        
        if Scene.currentScene.tilemap and hasattr(Scene.currentScene.tilemap, 'camera_offset'):
            screen_rect.x -= Scene.currentScene.tilemap.camera_offset.x
            screen_rect.y -= Scene.currentScene.tilemap.camera_offset.y
        
        screen.blit(scaled_sprite, screen_rect)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)
        
class ObjectWithCollider(Object):
    def __init__(self, position: pygame.Vector2, size: pygame.Vector2):
        self.size = size

        super().__init__(position)
        
        self.rect = pygame.Rect(0, 0, size.x, size.y)
        self._update_rect()
    
    def _update_rect(self):
        """Synchronise le rect avec la position (centré)."""
        self.rect.center = (int(self.position.x), int(self.position.y))

    def GetColliders(self):
        return [self.rect]
    
    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        screen_rect = self.rect.copy()

        from SceneManager import Scene

        if Scene.currentScene.tilemap and hasattr(Scene.currentScene.tilemap, 'camera_offset'):
            screen_rect.x -= Scene.currentScene.tilemap.camera_offset.x
            screen_rect.y -= Scene.currentScene.tilemap.camera_offset.y
        
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

class Gate(Object):
    def __init__(self, gateCoordinates, position: pygame.Vector2, size: pygame.Vector2, sprite: str):
        self.gateCoordinates=gateCoordinates
        self.size=size
        
        super().__init__(position)
        self.LoadSprite(sprite)

        self.rect=pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        self._update_rect()

    def _update_rect(self):
        """Synchronise le rect avec la position (centré)."""
        self.rect.center = (int(self.position.x), int(self.position.y))

    def Render(self, screen: pygame.surface.Surface, debug: bool=False):
        screen_rect=self.rect.copy()

        from SceneManager import Scene

        if Scene.currentScene.tilemap and hasattr(Scene.currentScene.tilemap, 'camera_offset'):
            screen_rect.x -= Scene.currentScene.tilemap.camera_offset.x
            screen_rect.y -= Scene.currentScene.tilemap.camera_offset.y
        
        if debug:
            pygame.draw.rect(screen, (0, 0, 255), screen_rect, 1)

        scaled_sprite = pygame.transform.scale(self.sprite, (int(self.size.x), int(self.size.y)))
        screen.blit(scaled_sprite, screen_rect)

        coll = self.rect.colliderect(Player.player.rect)

        if coll:
            from SceneManager import BiomeManager

            BiomeManager.biomeManager.loadBiome(self.gateCoordinates[0])
            BiomeManager.biomeManager.currentBiome.load(self.gateCoordinates[1], screen)
            