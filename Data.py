from Objects import *
from DialogueSystem import Dialogue

######################### ENTITY
################################

class CochonTronc(MeleeEnemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(
            position, 
            size = Vector2(50, 50), 
            sprite = r"data/Sprites/cochonTronc.png", 
            baseHealth = 100, 
            attackDmg = 5, 
            speed = 60, 
            sightRadius = 400, 
            wanderRadius = 100, 
            patrolDelay = 6, 
            stopDuration = 2,
            attackCooldown = 2,
            attackRange = 50
        )


class Tree(Harvestable):
    def __init__(self, position: pygame.Vector2):
        from InventorySystem import WOOD

        super().__init__(
            position, 
            Vector2(50, 50), 
            r"data/Sprites/log.png", 
            150, 
            LootTable(
                LootEntry(WOOD, 2, 4, 3),
                LootEntry(WOOD, 1, 3, 7),
                rolls=1
            )
        )


ENTITIES: dict[str, type[Entity]] = {
    "Tree" : Tree,
    "CochonTronc": CochonTronc
}

######################### WEAPON
################################

class Sword(MeleeWeapon):
    icon:str =  r"data/Sprites/icon_sword.png"

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
    icon:str = r"data/Sprites/icon_minigun.png"

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
    icon:str = r"data/Sprites/icon_rocketLauncher.png"

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
    icon:str = r"data/Sprites/icon_flameThrower.png"

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
    def __init__(self, position, angle, direction, owner):
        super().__init__(
            position, 
            Vector2(8, 4), 
            angle,
            r"data/Sprites/bullet.png", 
            50, 
            direction, 
            800, 
            2,
            owner
        )

class Rocket(Projectile):
    def __init__(self, position, angle, direction, owner):
        super().__init__(
            position, 
            Vector2(30, 10), 
            angle,
            r"data/Sprites/rocket.png",
            75, 
            direction, 
            1000, 
            2,
            owner
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
            0.05,
            self.owner
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
            0.05,
            self.owner
        )

        self.Destroy()

class Flame(Projectile):
    def __init__(self, position, angle, direction, owner):
        super().__init__(
            position, 
            Vector2(30, 20), 
            angle,
            r"data/Sprites/flame.png",
            2, 
            direction, 
            300, 
            0.7,
            owner
        )

    def OnEnemyHit(self, enemy: Enemy):
        enemy.TakeDamage(self.damage)

    def OnHarvestableHit(self, object: Harvestable):
        object.TakeDamage(self.damage)

##################### DIALOGUES
################################

class NPC1(NPC):
    def __init__(self, position:Vector2):
        super().__init__(
            position=position,
            size=Vector2(50, 50),
            sprite=r"data/sprites/toruk_makto.png",
            baseHealth=100,
            interactRadius=100,
            dialogueQueue=Queue(Dialogue("Bonjour à toi, jeune aventurier !!", 2), Dialogue("J'adore les sushis grillés, ainsi que les bananes flambées au rhum !", 5)),
            name="Jean Claude Montparnasse"
        )

NPCS: dict[str, type[NPC]] ={
    "NPC1":NPC1
}

######################## EFFECTS
################################

class HealEffect(Effect):
    def __init__(self, amount: float):
        super().__init__(0, (235, 64, 52))
        self.amount = amount

    def Apply(self, target: Entity):
        target.Heal(self.amount)

class RegenEffect(Effect):
    def __init__(self, amount_per_sec, duration):
        super().__init__(duration, (224, 43, 200))
        self.amount_per_sec = amount_per_sec

    def Update(self, target: Entity, dt):
        target.Heal(self.amount_per_sec * dt)
        self.duration -= dt

class SpeedEffect(Effect):
    def __init__(self, multiplier, duration):
        super().__init__(duration, (28, 133, 232))
        self.multiplier = multiplier

    def Apply(self, target: Entity):
        target.speed *= self.multiplier

    def Update(self, target: Entity, dt):
        self.duration -= dt

        if self.is_finished():
            target.speed /= self.multiplier

######################## POTIONS
################################

class HealthPotion(Potion):
    effect = HealEffect(20)

    def __init__(self):
        super().__init__(
            Vector2(0, 0),
            HealthPotion.effect
        )

class RegenPotion(Potion):
    effect = RegenEffect(2, 10)

    def __init__(self):
        super().__init__(
            Vector2(0, 0),
            RegenPotion.effect
        )

class SpeedPotion(Potion):
    effect = SpeedEffect(1.2, 15)

    def __init__(self):
        super().__init__(
            Vector2(0, 0),
            SpeedPotion.effect
        )
