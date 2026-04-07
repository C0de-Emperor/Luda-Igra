import pygame
from pygame import Vector2
from Tools import Queue
import os
import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from InventorySystem import ItemStack, Resource



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

        self.rect:pygame.Rect = pygame.Rect(position.x, position.y, size.x, size.y)

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

        scene = Scene.currentScene
        if scene is None:
            return

        if self in scene.objects:
            scene.objects.remove(self)

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
        self.baseHealth:float = baseHealth
        self.health:float = baseHealth

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

    def TakeDamage(self, amount: float):
        self.health -= amount
        if self.health <= 0:
            self.Die()

    def Heal(self, amount: float):
        self.health += amount
        if self.health > self.baseHealth:
            self.health = self.baseHealth

    def Die(self):
        self.Destroy()

class Player(Entity):
    player:"Player" = None

    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, sprite: str, tools: list[type["Weapon"]], baseHealth: float, speed: float = 300):
        super().__init__(position, size, False, baseHealth)
        self.LoadSprite(sprite, True)
        self.speed:float = speed

        self.tools: Queue = Queue(*tools)
        self.currentTool: type[Weapon] = None

        from InventorySystem import Inventory, Recipe
        self.inventory:Inventory = Inventory()

        self.recipeToProcess: Recipe = None
        self.recipeProcessTimer:float = 0

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
        from InventorySystem import CraftingManager
        
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


        if self.recipeToProcess != None:
            self.recipeProcessTimer += dt
            if self.recipeProcessTimer >= self.recipeToProcess.duration:
                self.recipeToProcess.craft()
                self.recipeToProcess = None
                self.recipeProcessTimer = 0

        elif not CraftingManager.craftingQueue.isEmpty():
            self.recipeToProcess = CraftingManager.craftingQueue.dequeue()
            self.recipeProcessTimer = 0



    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        screen_rect = Camera.get_screen_rect(self.rect)
        
        screen.blit(self.sprite, screen_rect)

        self._render_health_bar(screen)

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
            for k in range(self.tools.getLen()-1):
                self.tools.enqueue(self.tools.dequeue())

        if self.currentTool:
            self.currentTool.Destroy()
        self.currentTool = self.tools.peek()()

    def _render_health_bar(self, screen: pygame.surface.Surface):
        # --- PARAMÈTRES UI ---
        bar_width = 300
        bar_height = 30

        margin = 20  # distance au bord écran
        padding = 8  # espace intérieur

        bar_x = margin
        bar_y = pygame.display.Info().current_h - bar_height - margin

        # fond du conteneur
        container_rect = pygame.Rect(bar_x - padding, bar_y - padding, bar_width + padding * 2, bar_height + padding * 2)
        pygame.draw.rect(screen, (20, 20, 35), container_rect, border_radius=12)

        # --- BACKGROUND ---
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (40, 40, 40), bar_rect, border_radius=10)

        # --- HEALTH ---
        health_ratio = max(self.health, 0) / self.baseHealth
        current_width = int(bar_width * health_ratio)

        if health_ratio > 0.6:
            color = (0, 200, 0)
        elif health_ratio > 0.3:
            color = (200, 150, 0)
        else:
            color = (200, 0, 0)

        pygame.draw.rect(screen, color, (bar_x, bar_y, current_width, bar_height), border_radius=10)

        # --- BORDER ---
        pygame.draw.rect(screen, (200, 200, 220), bar_rect, 2, border_radius=10)

        # --- TEXTE ---
        font = pygame.font.SysFont("Arial", 20, bold=True)
        text = font.render(f"{int(self.health)} / {int(self.baseHealth)}", True, (240, 240, 240))

        text_rect = text.get_rect(center=bar_rect.center)
        screen.blit(text, text_rect)

    def Destroy(self):
        if getattr(self, 'currentTool', None):
            self.currentTool.Destroy()
            self.currentTool = None

        if getattr(self, 'inventory', None):
            if getattr(self.inventory, 'UI', None):
                self.inventory.UI.Destroy()
                self.inventory.UI = None
            if getattr(self.inventory, 'craftingUI', None):
                self.inventory.craftingUI.Destroy()
                self.inventory.craftingUI = None
            if getattr(self.inventory, 'craftingQueueUI', None):
                self.inventory.craftingQueueUI.Destroy()
                self.inventory.craftingQueueUI = None

        if Player.player is self:
            Player.player = None

        super().Destroy()

    def Die(self):
        from Engine import trigger_game_over
        super().Die()

        trigger_game_over()



class Gate(Object):
    def __init__(self, name:str, destination:str, position: pygame.Vector2, size: pygame.Vector2, sprite: str):
        super().__init__(position, size, True)
        self.LoadSprite(sprite, True)

        self.name:str = name
        self.destination:str = destination

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

        self.entity:type["Entity"] = entity
        self.maxSpawnCount:int = maxSpawnCount
        self.delay:int = delay
        self.count:int = 0

        self.timer:float = 0

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


        self.attackDmg:float = attackDmg
        self.speed:float = speed
        self.wanderRadius:float = wanderRadius
        self.sightRadius:float = sightRadius
        self.patrolDelay:float = patrolDelay + random.randint(-patrolDelay//5, patrolDelay//5)
        self.stopDuration:float = stopDuration + random.randint(-stopDuration//5, stopDuration//5)

        self.directionTimer:float = 0
        self.stopTimer:float = -1
        self.isChasing:bool = False
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

            if self.wanderTarget.magnitude() > 0:
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

class MeleeEnemy (Enemy):
    def __init__(self, position:Vector2, size:Vector2, sprite:str, baseHealth:float, attackDmg:float, speed:float, sightRadius:float, wanderRadius:float, patrolDelay:float, stopDuration: float, attackCooldown: float, attackRange: float):
        super().__init__(
            position, 
            size,
            sprite, 
            baseHealth, 
            attackDmg, 
            speed, 
            sightRadius, 
            wanderRadius, 
            patrolDelay, 
            stopDuration
        )

        self.attackCooldown:float = attackCooldown
        self.attackRange:float = attackRange   
        self.attackTimer:float = attackCooldown

    def Update(self, dt):
        super().Update(dt)

        if self.attackTimer > 0:
            self.attackTimer -= dt

        if (Player.player.position - self.position).magnitude() <= self.attackRange and self.attackTimer <= 0:
                self.Attack()

    def Attack(self):
        if self.attackTimer > 0:
            return

        from pygame import Vector2
        import math

        self.attackTimer = self.attackCooldown

        delta = Player.player.position - self.position

        if delta.length() == 0:
            direction = Vector2(1, 0)
        else:
            direction = delta.normalize()

        # angle pour la rotation
        angle = math.degrees(math.atan2(-direction.y, direction.x))

        # position devant l’ennemi
        hitbox_pos = self.position + direction * 25

        Hitbox(
            hitbox_pos,
            Vector2(30, 20),
            angle,
            r"data/Sprites/slash.png",
            self.attackDmg,
            True,
            0.1,
            Enemy
        )



class Weapon(Object):
    def __init__(self, position: Vector2, size: Vector2, sprite:str, offset: Vector2):
        super().__init__(position, size, False)
        self.LoadSprite(sprite, True)

        self.offset:Vector2 = offset
        self.offset_distance:float = 20

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
        self.damage:float = damage
        self.attack_range:float = attack_range
        self.cooldown:float = cooldown
        self.attack_timer:float = 0

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

            Hitbox(hitbox_pos, Vector2(30, 25), self.angle - 90, r"data/Sprites/slash.png", self.damage/3, False, 0.1, Player)

class RangedWeapon(Weapon):
    def __init__(self, position: Vector2, size: Vector2, sprite:str, cooldown: float, angleDeviation: int, bullet: type["Projectile"]):
        super().__init__(position, size, sprite, Vector2(10, 10))
        self.attack_range:float = (self.size.x // 2) + 8
        self.cooldown:float = cooldown
        self.bullet:type["Projectile"] = bullet
        self.angleDeviation:float = angleDeviation

        self.attack_timer:float = 0

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

        self.bullet(hitbox_pos, angle, direction, Player)



class Hitbox(Object):
    def __init__(self, position: Vector2, size: Vector2, angle: float, sprite: str, damage: float, scale: bool, lifetime: float, owner):
        super().__init__(position, size, False)
        self.LoadSprite(sprite, scale)
        self.damage:float = damage
        self.lifetime:float = lifetime
        self.owner:Object = owner

        self.hitEnemies:list[Object] = set()

        self.angle:float = angle
        self.rect.center = (position.x, position.y)

    def Update(self, dt):
        from SceneManager import Scene

        for obj in Scene.currentScene.objects:
            if isinstance(obj, Entity) and self.rect.colliderect(obj.rect) and not isinstance(obj, self.owner):
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
                 speed: float, lifetime: float, owner):

        super().__init__(position, size, True)
        self.LoadSprite(sprite, True)

        self.rect:pygame.Rect = pygame.Rect(0, 0, size.x, size.y)
        self.rect.center = (position.x, position.y)

        self.damage:float = damage
        self.direction:Vector2 = direction.normalize()
        self.speed:float = speed
        self.lifetime:float = lifetime
        self.angle:float = angle

        self.owner:Object = owner

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
            if isinstance(obj, Entity) and self.rect.colliderect(obj.rect) and not isinstance(obj, self.owner):
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



class LootEntry:
    def __init__(self, resource, min_amount, max_amount, weight):
        self.resource:"Resource" = resource
        self.min_amount:int = min_amount
        self.max_amount:int = max_amount
        self.weight:float = weight

class LootTable:
    def __init__(self, *entries: LootEntry, rolls=1):
        self.entries:LootEntry = list(entries)
        self.rolls:int = rolls

    def roll(self):
        from InventorySystem import ItemStack
        drops = []

        total_weight = sum(e.weight for e in self.entries)

        for _ in range(self.rolls):
            r = random.uniform(0, total_weight)

            current = 0
            for entry in self.entries:
                current += entry.weight

                if r <= current:
                    amount = random.randint(entry.min_amount, entry.max_amount)
                    drops.append(ItemStack(entry.resource, amount))
                    break

        return drops



class Harvestable(Entity):
    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, sprite: str, baseHealth:float, lootTable: LootTable):
        super().__init__(position, size, True, baseHealth)
        self.LoadSprite(sprite, True)
        
        self.lootTable:LootTable = lootTable

    def Render(self, screen, debug=False):
        screen_rect = Camera.get_screen_rect(self.rect)
        screen.blit(self.sprite, screen_rect)

        self._render_health_bar(screen)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

    def Die(self):
        drops = self.lootTable.roll()

        for drop in drops:
            self._spawn_drop(drop)

        self.Destroy()

    def _spawn_drop(self, stack):
        import random
        from pygame import Vector2

        angle = random.uniform(0, 360)
        distance = random.uniform(5, 20)

        offset = Vector2(distance, 0).rotate(angle)

        DroppedStack(self.position + offset, stack)



class DroppedStack(Object):
    def __init__(self, position, stack: "ItemStack", destroyOnLoad=True):
        super().__init__(position, pygame.Vector2(40, 40), destroyOnLoad)
        self.LoadSprite(stack.resource.icon, False)
        self.stack:"ItemStack" = stack

        self.font:pygame.font.Font = pygame.font.SysFont(None, 20)

    def Render(self, screen, debug=False):
        screen_rect = Camera.get_screen_rect(self.rect)
        screen.blit(self.sprite, screen_rect)

        # --- TEXTE QUANTITÉ ---
        amount_text = self.font.render(str(self.stack.amount), True, (255, 255, 255))

        text_rect = amount_text.get_rect()
        text_rect.bottomright = screen_rect.bottomright

        text_rect.x -= 2
        text_rect.y -= 2

        # optionnel : fond noir pour lisibilité
        bg_rect = text_rect.inflate(4, 2)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)

        screen.blit(amount_text, text_rect)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), screen_rect, 1)

    def Update(self, dt):
        # Vérifie si la souris est sur l'objet
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        screen_rect = Camera.get_screen_rect(self.rect)

        if screen_rect.collidepoint(mouse_pos):
            Player.player.inventory.add(self.stack.resource, self.stack.amount)
            
            # Créer une notification
            from UI import ItemNotification
            ItemNotification(self.stack.resource, self.stack.amount)
            
            self.Destroy()




