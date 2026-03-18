from Objects import *


####################### ENTITIES
################################

class CochonTronc(Enemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, Vector2(50, 50), r"data/Sprites/cochonTronc.png", 100, 10, 60, 400, 100, 6, 2)


class Tree(Harvestable):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, Vector2(50, 50), r"data/Sprites/log.png", 150, ItemStack(WOOD, 15))


ENTITIES: dict[str, type[Entity]] = {
    "Tree" : Tree,
    "CochonTronc": CochonTronc
}

######################### WEAPON
################################

class Sword(MeleeWeapon):
    def __init__(self):
        super().__init__(
            Vector2(0, 0), 
            pygame.Vector2(20, 50),
            r"data/Sprites/sword.png", 
            30, 
            50,
            0.3
        )

class MiniGun(RangedWeapon):
    def __init__(self):
        super().__init__(
            Vector2(0, 0), 
            pygame.Vector2(50, 20), 
            r"data/Sprites/minigun.png",
            0.05,
            5,
            Bullet
        )

class RocketLaucher(RangedWeapon):
    def __init__(self):
        super().__init__(
            Vector2(0, 0), 
            pygame.Vector2(50, 20), 
            r"data/Sprites/rocketLauncher.png",
            0.75,
            1,
            Rocket
        )

class FlameThrower(RangedWeapon):
    def __init__(self):
        super().__init__(
            Vector2(0, 0), 
            pygame.Vector2(50, 20), 
            r"data/Sprites/flameThrower.png",
            0.05,
            10,
            Flame
        )

##################### PROJECTILE
################################

class Bullet(Projectile):
    def __init__(self, position, angle, direction):
        super().__init__(
            position, 
            Vector2(8, 4), 
            angle,
            r"data/Sprites/bullet.png", 
            50, 
            direction, 
            800, 
            2
        )

class Rocket(Projectile):
    def __init__(self, position, angle, direction):
        super().__init__(
            position, 
            Vector2(30, 10), 
            angle,
            r"data/Sprites/rocket.png",
            75, 
            direction, 
            1000, 
            2
        )

    def OnEnemyHit(self, enemy: Enemy):
        import random
        explosion_radius = 250

        Hitbox(
            self.position, 
            Vector2(explosion_radius, explosion_radius), 
            random.randint(0, 360),
            r"data/Sprites/explosion.png",
            self.damage,
            True,
            0.05
        )

        self.Destroy()

    def OnHarvestableHit(self, object: Harvestable):
        import random
        explosion_radius = 250

        Hitbox(
            self.position, 
            Vector2(explosion_radius, explosion_radius), 
            random.randint(0, 360),
            r"data/Sprites/explosion.png",
            self.damage,
            True,
            0.05
        )

        self.Destroy()

class Flame(Projectile):
    def __init__(self, position, angle, direction):
        super().__init__(
            position, 
            Vector2(30, 20), 
            angle,
            r"data/Sprites/flame.png",
            2, 
            direction, 
            300, 
            2
        )

    def OnEnemyHit(self, enemy: Enemy):
        enemy.TakeDamage(self.damage)


    def OnHarvestableHit(self, object: Harvestable):
        object.TakeDamage(self.damage)

