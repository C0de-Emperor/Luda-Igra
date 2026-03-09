import pygame
from pygame import Vector2
import os


KEYS_MOVEMENT = {
    pygame.K_z: Vector2(0, -1),
    pygame.K_s: Vector2(0, 1),
    pygame.K_q: Vector2(-1, 0),
    pygame.K_d: Vector2(1, 0),
}


class Camera:
    @staticmethod
    def get_screen_rect(world_rect: pygame.Rect) -> pygame.Rect:
        from SceneManager import Scene
        screen_rect = world_rect.copy()
        if Scene.currentScene.tilemap and hasattr(Scene.currentScene.tilemap, 'camera_offset'):
            screen_rect.x -= Scene.currentScene.tilemap.camera_offset.x
            screen_rect.y -= Scene.currentScene.tilemap.camera_offset.y
        return screen_rect


class Object:
    def __init__(self, position: Vector2, destroyOnLoad: bool = True):
        from SceneManager import Scene

        self.position: Vector2 = position
        self.destroyOnLoad: bool = destroyOnLoad

        Scene.currentScene.objects.append(self)

    def Update(self, dt):
        pass

    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        pass

    def Destroy(self):
        from SceneManager import Scene

        if self in Scene.currentScene.objects:
            Scene.currentScene.objects.remove(self)
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

        super().__init__(position, False)
        self.LoadSprite(sprite)
        
        self.rect = pygame.Rect(0, 0, size.x, size.y)
        self._update_rect()

        if Player.player != None:
            print("Error : 2 player in the scene")
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
        
        screen_rect = Camera.get_screen_rect(self.rect)
        
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
        screen_rect = Camera.get_screen_rect(self.rect)
        
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

class Gate(Object):
    def __init__(self, name:str, destination:str, position: pygame.Vector2, size: pygame.Vector2, sprite: str):
        self.name = name
        self.destination = destination
        self.size=size
        
        super().__init__(position, True)
        self.LoadSprite(sprite)

        self.rect=pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        self._update_rect()

    def _update_rect(self):
        """Synchronise le rect avec la position (centré)."""
        self.rect.center = (int(self.position.x), int(self.position.y))

    def Update(self, dt):
        from SceneManager import SCENES
        coll = self.rect.colliderect(Player.player.rect)

        if coll:
            SCENES[self.destination].load(self.name)

    def Render(self, screen: pygame.surface.Surface, debug: bool=False):
        screen_rect = Camera.get_screen_rect(self.rect)

        if debug:
            pygame.draw.rect(screen, (0, 0, 255), screen_rect, 1)

        scaled_sprite = pygame.transform.scale(self.sprite, (int(self.size.x), int(self.size.y)))
        screen.blit(scaled_sprite, screen_rect)

class SpawnArea(Object):
    def __init__(self, entity: type["Enemy"], maxSpawnCount: int, delay: int, position: pygame.Vector2, size: pygame.Vector2):
        import random

        self.size=size
        self.entity = entity
        self.maxSpawnCount = maxSpawnCount
        self.delay = delay
        self.count = 0

        self.timer = 0

        super().__init__(position, True)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)

        for i in range(random.randint(0, self.maxSpawnCount)):
            self._spawn()

    def _spawn(self):
        import random

        pos = self.position.copy()

        pos.x += random.randint(0, int(self.size.x))
        pos.y += random.randint(0, int(self.size.y))

        self.entity(pos)

        self.count += 1

    def Update(self, dt):
        self.timer += dt

        if self.timer >= self.delay and self.count < self.maxSpawnCount:
            self._spawn()
            self.timer = 0

    def Render(self, screen: pygame.surface.Surface, debug: bool=False):
        screen_rect = Camera.get_screen_rect(self.rect)
        
        if debug:
            pygame.draw.rect(screen, (255, 85, 0), screen_rect, 1)
            
class Enemy(Object):
    def __init__(self, position:Vector2, size:Vector2, sprite:str, baseHealth:float, attackDmg:float, movespeed:float, sightRadius:float):
        super().__init__(position, True)
        self.LoadSprite(sprite)

        self.size=size

        self.baseHealth = baseHealth
        self.attackDmg = attackDmg
        self.movespeed=movespeed
        self.sightRadius = sightRadius

        self.isChasing=False
        self.randomDirection=Vector2(0,0)
        
        self.rect = pygame.Rect(0, 0, size.x, size.y)
        self._update_rect()

    def _update_rect(self):
        """Synchronise le rect avec la position (centré)."""
        self.rect.center = (int(self.position.x), int(self.position.y))
    
    def Render(self, screen, debug=False):
        # Scale le sprite à la bonne taille
        scaled_sprite = pygame.transform.scale(self.sprite, (int(self.size.x), int(self.size.y)))
        
        screen_rect = Camera.get_screen_rect(self.rect)
        screen.blit(scaled_sprite, screen_rect)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

    def Update(self, dt):
        from SceneManager import Scene
        import random
        
        if Scene.currentScene is None:
            return

        deltaPos = Vector2(self.position.x - Player.player.position.x, self.position.y - Player.player.position.y)
        self.isChasing = deltaPos.magnitude() <= self.sightRadius

        if self.isChasing:
            direction =- deltaPos.normalize()
        else:
            if pygame.time.get_ticks() % 1000 * 5 <= 10:
                print(self.randomDirection)
                self.randomDirection=Vector2(random.randint(20, 200), random.randint(20, 200)).normalize()

            direction=self.randomDirection
        
        colliders = Scene.currentScene.GetAllColliders()+[Player.player.rect]

        # Déplacement et collision en X
        if direction.x != 0:
            self.position.x += direction.x * self.movespeed * dt
            self._update_rect()
            self._check_collision(colliders, "x")

        # Déplacement et collision en Y
        if direction.y != 0:
            self.position.y += direction.y * self.movespeed * dt
            self._update_rect()
            self._check_collision(colliders, "y")
        
        self._update_rect()
    
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

class CochonTronc(Enemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, Vector2(50, 50), "data/sprites/toruk_makto.png", 100, 10, 60, 400)

ENEMIES: dict[str, type[Enemy]] = {
    "CochonTronc" : CochonTronc
}
