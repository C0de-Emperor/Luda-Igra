import pygame

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

class Player (Object):
    def __init__(self, position: pygame.Vector2):
        self.position = position

        super().__init__()

    def Render(self, screen):
        pygame.draw.circle(screen, "red", self.position, 40)

    def Update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.position.y -= 300 * dt
        if keys[pygame.K_s]:
            self.position.y += 300 * dt
        if keys[pygame.K_q]:
            self.position.x -= 300 * dt
        if keys[pygame.K_d]:
            self.position.x += 300 * dt

    