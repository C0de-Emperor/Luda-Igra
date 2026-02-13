import pygame
from pygame import Vector2
import os

class Object :
    instances: list["Object"] = []

    def __init__(self):
        Object.instances.append(self)

    def Update (self, dt):
        pass

    def Render (self, screen):
        pass

    def Destroy(self):
        if self in Object.instances:
            Object.instances.remove(self)
            del self

class Player (Object):
    def __init__(self, position: pygame.Vector2, size: pygame.Vector2, sprite:str, speed: float = 300):
        self.position = position
        self.speed = speed
        self.size = size

        if isinstance(sprite, str):
            if not os.path.exists(sprite):
                raise Exception(f"Image not found: {sprite}", isFatal=True)
            else:
                img = pygame.image.load(sprite).convert_alpha()
                self.sprite: pygame.Surface = img
        elif isinstance(sprite, pygame.Surface):
            self.sprite: pygame.Surface = sprite
        else:
            raise Exception(f"Unsupported image type: {type(image)}", isFatal=True)

        super().__init__()

    def Render(self, screen: pygame.surface.Surface):
        surf = pygame.transform.scale(self.sprite, (int(self.size.x), int(self.size.y)))

        world_pos = Vector2(self.position.x - self.size.x/2, self.position.y - self.size.y/2)

        screen.blit(surf, world_pos)

    def Update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.position.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.position.y += self.speed * dt
        if keys[pygame.K_q]:
            self.position.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.position.x += self.speed * dt
        if keys[pygame.K_t]:
            self.Destroy()

    