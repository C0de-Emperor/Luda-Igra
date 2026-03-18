import pygame
from pygame import Vector2
from Tools import Queue
import os

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from InventorySystem import ItemStack


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
    
    @staticmethod
    def world_to_screen_point(world_pos: Vector2) -> Vector2:
        from SceneManager import Scene
        screen_pos = Vector2(world_pos.x, world_pos.y)
        if Scene.currentScene.tilemap and hasattr(Scene.currentScene.tilemap, 'camera_offset'):
            screen_pos -= Scene.currentScene.tilemap.camera_offset
        return screen_pos
    
    @staticmethod
    def screen_to_world_point(screen_pos: Vector2) -> Vector2:
        from SceneManager import Scene
        world_pos = Vector2(screen_pos.x, screen_pos.y)
        if Scene.currentScene.tilemap and hasattr(Scene.currentScene.tilemap, 'camera_offset'):
            world_pos += Scene.currentScene.tilemap.camera_offset
        return world_pos


class Object:
    def __init__(self, position: Vector2, size:Vector2, destroyOnLoad: bool = True):
        from SceneManager import Scene

        self.size: Vector2 = size
        self.destroyOnLoad: bool = destroyOnLoad

        self.rect = pygame.Rect(position.x, position.y, size.x, size.y)

        Scene.currentScene.objects.append(self)

    @property
    def position(self):
        return Vector2(self.rect.centerx, self.rect.centery)

    @position.setter
    def position(self, value: Vector2):
        self.rect.center = (int(value.x), int(value.y))

    def Update(self, dt):
        pass

    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        pass

    def HandleEvent(self, event):
        pass

    def Destroy(self):
        from SceneManager import Scene

        if self in Scene.currentScene.objects:
            Scene.currentScene.objects.remove(self)
            del self

    def GetColliders(self) -> list[pygame.rect.Rect]:
        return []

    def LoadSprite(self, sprite: str, scale: bool):
        if isinstance(sprite, str):
            if not os.path.exists(sprite):
                raise FileNotFoundError(f"Image not found: {sprite}")

            if scale:
                self.sprite = pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), (int(self.size.x), int(self.size.y)))
            else:
                self.sprite = pygame.image.load(sprite).convert_alpha()
            
        elif isinstance(sprite, pygame.Surface):
            self.sprite = pygame.transform.scale(sprite, (int(self.size.x), int(self.size.y)))
        else:

            raise TypeError(f"Unsupported image type: {type(sprite)}")

class Entity(Object):
    def __init__(self, position: Vector2, size: Vector2, destroyOnLoad: bool = True, baseHealth: float = 1):
        super().__init__(position, size, destroyOnLoad)
        self.baseHealth = baseHealth
        self.health = baseHealth

    def TakeDamage(self, amount: float):
        self.health -= amount
        if self.health <= 0:
            self.Die()

    def Die(self):
        self.Destroy()

class Player(Object):
    player = None

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, sprite: str, tools: list[type["Weapon"]], speed: float = 300):
        super().__init__(position, size, False)
        self.LoadSprite(sprite, True)

        self.tools: Queue = Queue(*tools)
        self.currentTool: type[Weapon] = None

        from InventorySystem import Inventory
        self.inventory = Inventory()

        self.speed = speed

        if Player.player != None:
            print("Error : 2 player in the scene")
        Player.player = self

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

    def _check_collision(self, walls, axis):
        for wall in walls:
            if self.rect.colliderect(wall):

                if axis == "x":
                    if self.rect.centerx < wall.centerx:
                        self.rect.right = wall.left
                    else:
                        self.rect.left = wall.right

                else:
                    if self.rect.centery < wall.centery:
                        self.rect.bottom = wall.top
                    else:
                        self.rect.top = wall.bottom

    def Update(self, dt):
        from SceneManager import Scene
        
        if Scene.currentScene is None:
            return
        
        direction = self._get_movement_direction()
        colliders = Scene.currentScene.GetAllColliders([self])

        if direction.x != 0:
            self.rect.x += direction.x * self.speed * dt
            self._check_collision(colliders, "x")

        if direction.y != 0:
            self.rect.y += direction.y * self.speed * dt
            self._check_collision(colliders, "y")

    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        screen_rect = Camera.get_screen_rect(self.rect)
        
        screen.blit(self.sprite, screen_rect)

        if debug:
            pygame.draw.rect(screen, (180, 3, 252), screen_rect, 2)
        
    def HandleEvent(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.ChangeTool(event.y)

    def GetColliders(self):
        return [self.rect]
    
    def ChangeTool(self, direction):

        if self.tools.isEmpty():
            return

        if direction > 0:
            # tool suivant
            self.tools.enqueue(self.tools.dequeue())

        else:
            # rotation inverse
            prev = None
            current = self.tools.front

            while current.next:
                prev = current
                current = current.next

            if prev:
                prev.next = None
                current.next = self.tools.front
                self.tools.front = current

        if self.currentTool:
            self.currentTool.Destroy()
        self.currentTool = self.tools.peek()()

        

class ObjectWithCollider(Object):
    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, destroyOnLoad: bool = True):
        super().__init__(position, size, destroyOnLoad)
        

    def GetColliders(self):
        return [self.rect]
    
    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        screen_rect = Camera.get_screen_rect(self.rect)
        
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

class Gate(Object):
    def __init__(self, name:str, destination:str, position: pygame.Vector2, size: pygame.Vector2, sprite: str):
        super().__init__(position, size, True)
        self.LoadSprite(sprite, True)

        self.name = name
        self.destination = destination

    def Update(self, dt):
        from SceneManager import SCENES
        coll = self.rect.colliderect(Player.player.rect)

        if coll:
            SCENES[self.destination].load(self.name)

    def Render(self, screen: pygame.surface.Surface, debug: bool=False):
        screen_rect = Camera.get_screen_rect(self.rect)

        if debug:
            pygame.draw.rect(screen, (0, 0, 255), screen_rect, 1)

        screen.blit(self.sprite, screen_rect)

class SpawnArea(Object):
    def __init__(self, entity: type["Entity"], maxSpawnCount: int, delay: int, position: pygame.Vector2, size: pygame.Vector2):
        import random
        super().__init__(position, size, True)

        self.entity = entity
        self.maxSpawnCount = maxSpawnCount
        self.delay = delay
        self.count = 0

        self.timer = 0

        for i in range(random.randint(0, self.maxSpawnCount)):
            self._spawn()

    def _spawn(self):
        import random
        pos = self.position.copy()

        pos.x += random.randint(-int(self.size.x/2), int(self.size.x/2))
        pos.y += random.randint(-int(self.size.y/2), int(self.size.y/2))

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

class Enemy(Entity):
    def __init__(self, position:Vector2, size:Vector2, sprite:str, baseHealth:float, attackDmg:float, speed:float, sightRadius:float, wanderRadius:float, patrolDelay:float, stopDuration: float):
        super().__init__(position, size, True, baseHealth)
        self.LoadSprite(sprite, True)
        import random


        self.attackDmg = attackDmg
        self.speed = speed
        self.wanderRadius = wanderRadius
        self.sightRadius = sightRadius
        self.patrolDelay = patrolDelay + random.randint(-patrolDelay//5, patrolDelay//5)
        self.stopDuration = stopDuration + random.randint(-stopDuration//5, stopDuration//5)

        self.directionTimer = 0
        self.stopTimer = -1
        self.isChasing=False
        self._choose_wander_target()

    def _choose_wander_target(self):
        import random

        self.wanderTarget = Vector2(
            random.randint(-self.wanderRadius, self.wanderRadius),
            random.randint(-self.wanderRadius, self.wanderRadius)
        )

    def Render(self, screen, debug=False):
        screen_rect = Camera.get_screen_rect(self.rect)
        screen.blit(self.sprite, screen_rect)

        self._render_health_bar(screen)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

    def Update(self, dt):
        from SceneManager import Scene
        
        if Scene.currentScene is None:
            return

        distanceToPlayer = self.position - Player.player.position

        if distanceToPlayer.magnitude() <= 30:
            return

        self.isChasing = distanceToPlayer.magnitude() <= self.sightRadius

        if self.isChasing:
            direction =- distanceToPlayer.normalize()
        elif self.directionTimer > -1:
            self.directionTimer += dt

            if self.directionTimer >= self.patrolDelay:
                self.directionTimer = -1
                self.stopTimer = 0
                self._choose_wander_target()

            direction = self.wanderTarget.normalize()
        else:
            self.stopTimer += dt

            if self.stopTimer >= self.stopDuration:
                self.stopTimer = -1
                self.directionTimer = 0
                
            return  
           

        colliders = Scene.currentScene.GetAllColliders([self, Player.player])

        if direction.x != 0:
            self.rect.x += direction.x * self.speed * dt
            self._check_collision(colliders, "x")

        if direction.y != 0:
            self.rect.y += direction.y * self.speed * dt
            self._check_collision(colliders, "y")
    
    def _check_collision(self, walls, axis):
        for wall in walls:
            if self.rect.colliderect(wall):

                if axis == "x":
                    if self.rect.centerx < wall.centerx:
                        self.rect.right = wall.left
                    else:
                        self.rect.left = wall.right

                else:
                    if self.rect.centery < wall.centery:
                        self.rect.bottom = wall.top
                    else:
                        self.rect.top = wall.bottom

    def _render_health_bar(self, screen):
        # position de l'ennemi à l'écran
        screen_rect = Camera.get_screen_rect(self.rect)

        bar_width = screen_rect.width
        bar_height = 5
        bar_x = screen_rect.centerx - bar_width // 2
        bar_y = screen_rect.top - 10  # au-dessus de l'ennemi

        # fond rouge
        pygame.draw.rect(screen, (255,0,0), (bar_x, bar_y, bar_width, bar_height))

        # vert proportionnel à la vie
        health_ratio = max(self.health, 0) / self.baseHealth
        pygame.draw.rect(screen, (0,255,0), (bar_x, bar_y, int(bar_width * health_ratio), bar_height))



class Weapon(Object):
    def __init__(self, position: Vector2, size: Vector2, sprite:str, offset: Vector2):
        super().__init__(position, size, False)
        self.LoadSprite(sprite, True)

        self.offset = offset
        self.offset_distance = 20

    def Render(self, screen, debug=False):
        screen_rect = Camera.get_screen_rect(self.rect)

        sprite = self.sprite

        # flip si l'arme passe derrière
        if not (-90 <= self.angle <= 90):
            sprite = pygame.transform.flip(sprite, False, True)

        # rotation
        rotated_sprite = pygame.transform.rotozoom(sprite, self.angle, 1)
        rotated_rect = rotated_sprite.get_rect(center=screen_rect.center)

        screen.blit(rotated_sprite, rotated_rect)

        if debug:
            pygame.draw.rect(screen, (0, 0, 255), screen_rect, 1)

            player_screen_pos = Camera.world_to_screen_point(Player.player.position)
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            pygame.draw.line(screen, (255, 0, 0), player_screen_pos, mouse_pos, 1)
    
    def Update(self, dt):
        import math
        # position du joueur à l'écran
        player_screen_pos = Camera.world_to_screen_point(Player.player.position)

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        delta = mouse_pos - player_screen_pos

        if delta.length() > 0:
            direction = delta.normalize()
        else:
            direction = Vector2(0,0)

        self.position = Player.player.position + direction * self.offset_distance + self.offset

        # rotation
        self.angle = math.degrees(math.atan2(-delta.y, delta.x))

        if pygame.mouse.get_pressed()[0]:
            self.Attack()

    def Attack(self):
        pass

class MeleeWeapon(Weapon):
    def __init__(self, position: Vector2, size: Vector2, sprite:str, damage: float, attack_range: float, cooldown: float):
        super().__init__(position, size, sprite, Vector2(0, -10))
        self.damage = damage
        self.attack_range = attack_range
        self.cooldown = cooldown
        self.attack_timer = 0

    def Update(self, dt):
        super().Update(dt)

        if self.attack_timer > 0:
            self.attack_timer -= dt

    def Attack(self):
        if self.attack_timer > 0:
            return

        self.attack_timer = self.cooldown

        import math

        # angles du slash
        slash_angles = [-25, 0, 25]

        for offset in slash_angles:
            angle = self.angle + offset

            direction = Vector2(
                math.cos(math.radians(angle)),
                -math.sin(math.radians(angle))
            ).normalize()

            hitbox_pos = self.position + direction * self.attack_range

            Hitbox(hitbox_pos, Vector2(30, 25), self.angle - 90, r"data/Sprites/slash.png", self.damage/3, False)

class RangedWeapon(Weapon):
    def __init__(self, position: Vector2, size: Vector2, sprite:str, cooldown: float, angleDeviation: int, bullet: type["Projectile"]):
        super().__init__(position, size, sprite, Vector2(10, 10))
        self.attack_range = (self.size.x // 2) + 8
        self.cooldown = cooldown
        self.bullet = bullet
        self.angleDeviation = angleDeviation

        self.attack_timer = 0

    def Update(self, dt):
        super().Update(dt)

        if self.attack_timer > 0:
            self.attack_timer -= dt

    def Attack(self):
        if self.attack_timer > 0:
            return

        import random, math
        from pygame import Vector2

        self.attack_timer = self.cooldown

        mouse_world = Camera.screen_to_world_point(Vector2(pygame.mouse.get_pos()))
        delta = mouse_world - self.position
        if delta.length() > 0:
            direction = delta.normalize()
        else:
            direction = Vector2(1, 0)

        if self.angleDeviation > 0:
            spread_angle = random.uniform(-self.angleDeviation, self.angleDeviation)
            angle_rad = math.atan2(direction.y, direction.x) + math.radians(spread_angle)
            direction = Vector2(math.cos(angle_rad), math.sin(angle_rad)).normalize()

        hitbox_pos = self.position + direction * (self.attack_range + 5)

        angle = math.degrees(math.atan2(-direction.y, direction.x))

        self.bullet(hitbox_pos, angle, direction)


class Hitbox(Object):
    def __init__(self, position: Vector2, size: Vector2, angle: float, sprite: str, damage: float, scale: bool, lifetime=0.1):
        super().__init__(position, size, False)
        self.LoadSprite(sprite, scale)
        self.damage = damage
        self.lifetime = lifetime

        self.hitEnemies = set()

        self.angle = angle
        self.rect.center = (position.x, position.y)

    def Update(self, dt):
        from SceneManager import Scene

        for obj in Scene.currentScene.objects:
            if isinstance(obj, Entity) and self.rect.colliderect(obj.rect):
                if obj not in self.hitEnemies:
                    obj.TakeDamage(self.damage)
                    self.hitEnemies.add(obj)

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.Destroy()

    def Render(self, screen, debug=False):
        screen_rect = Camera.get_screen_rect(self.rect)

        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rect = rotated_sprite.get_rect(center=screen_rect.center)

        screen.blit(rotated_sprite, rotated_rect)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

class Projectile(Object):
    def __init__(self, position: Vector2, size: Vector2, angle: float,
                 sprite: str, damage: float, direction: Vector2,
                 speed: float, lifetime: float):

        super().__init__(position, size, True)
        self.LoadSprite(sprite, True)

        self.rect = pygame.Rect(0, 0, size.x, size.y)
        self.rect.center = (position.x, position.y)

        self.damage = damage
        self.direction = direction.normalize()
        self.speed = speed
        self.lifetime = lifetime
        self.angle = angle

    def Update(self, dt):
        from SceneManager import Scene

        self.position += self.direction * self.speed * dt

        colliders = Scene.currentScene.GetAllColliders([])
        for col in colliders:
            if self.rect.colliderect(col):
                self.OnWallHit()
                return

        for obj in Scene.currentScene.objects:
            if obj is self:
                continue
            if isinstance(obj, Entity) and self.rect.colliderect(obj.rect):
                if isinstance(obj, Enemy):
                    self.OnEnemyHit(obj)
                elif isinstance(obj, Harvestable):
                    self.OnHarvestableHit(obj)
                else:
                    self.OnEntityHit(obj)
                return

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.Destroy()

    def Render(self, screen, debug=False):
        screen_rect = Camera.get_screen_rect(self.rect)

        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rect = rotated_sprite.get_rect(center=screen_rect.center)

        screen.blit(rotated_sprite, rotated_rect)

        if debug:
            pygame.draw.rect(screen, (255,0,0), screen_rect, 1)

    def OnEnemyHit(self, enemy: Enemy):
        enemy.TakeDamage(self.damage)
        self.Destroy()

    def OnHarvestableHit(self, object: "Harvestable"):
        object.TakeDamage(self.damage)
        self.Destroy()

    def OnEntityHit(self, entity: Entity):
        entity.TakeDamage(self.damage)
        self.Destroy()

    def OnWallHit(self):
        self.Destroy()



class Harvestable(Entity):
    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, sprite: str, baseHealth:float, stack: "ItemStack"):
        super().__init__(position, size, True, baseHealth)
        self.LoadSprite(sprite, True)
        self.stack = stack

    def Render(self, screen, debug=False):
        screen_rect = Camera.get_screen_rect(self.rect)
        screen.blit(self.sprite, screen_rect)

        self._render_health_bar(screen)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

    def Die(self):
        self._spawn_loot()
        self.Destroy()

    def _render_health_bar(self, screen):
        # position de l'ennemi à l'écran
        screen_rect = Camera.get_screen_rect(self.rect)

        bar_width = screen_rect.width
        bar_height = 5
        bar_x = screen_rect.centerx - bar_width // 2
        bar_y = screen_rect.top - 10  # au-dessus de l'ennemi

        # fond rouge
        pygame.draw.rect(screen, (255,0,0), (bar_x, bar_y, bar_width, bar_height))

        # vert proportionnel à la vie
        health_ratio = max(self.health, 0) / self.baseHealth
        pygame.draw.rect(screen, (0,255,0), (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

    def _spawn_loot(self):
        import random
        from pygame import Vector2
        from InventorySystem import ItemStack

        for _ in range(self.stack.amount + random.randint(-1, 1)):
            angle = random.uniform(0, 360)
            distance = random.uniform(15, 45)
            offset = Vector2(distance, 0).rotate(angle)

            DroppedStack(self.position + offset, ItemStack(self.stack.resource, 1))

class DroppedStack(Object):
    def __init__(self, position, stack: "ItemStack", destroyOnLoad=True):
        super().__init__(position, pygame.Vector2(40, 40), destroyOnLoad)
        self.LoadSprite(stack.resource.icon, False)
        self.stack = stack

    def Render(self, screen, debug=False):
        screen_rect = Camera.get_screen_rect(self.rect)
        screen.blit(self.sprite, screen_rect)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

    def Update(self, dt):
        # Vérifie si la souris est sur l'objet
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        screen_rect = Camera.get_screen_rect(self.rect)

        if screen_rect.collidepoint(mouse_pos):
            Player.player.inventory.add(self.stack.resource, self.stack.amount)
            self.Destroy()




