from Objects import *
from DialogueSystem import Dialogue

######################### ENTITY
################################

class CochonTronc(MeleeEnemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(
            position, 
            size = Vector2(20, 20), 
            sprite = r"data/Sprites/cochonTronc.png", 
            baseHealth = 100, 
            attackDmg = 5, 
            speed = 33, 
            sightRadius = 400, 
            wanderRadius = 100, 
            patrolDelay = 6, 
            stopDuration = 2,
            attackCooldown = 2,
            attackRange = 50,
            attackSprite=r"data/Sprites/slash.png"
        )

class Dragon(RangeEnemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(
            position, 
            size = Vector2(30, 30), 
            sprite = r"data/Sprites/dragon2.png", 
            baseHealth = 3000, 
            attackDmg = 10, 
            speed = 35, 
            sightRadius = 400, 
            wanderRadius = 100, 
            patrolDelay = 6, 
            stopDuration = 2,
            attackCooldown = 0.1,
            attackRange = 500,
            bullet = FireBall,
            angleDeviation=40
        )

class Tree(Harvestable):
    def __init__(self, position: pygame.Vector2):
        from InventorySystem import WOOD

        super().__init__(
            position, 
            Vector2(30, 30), 
            r"data/Sprites/Oak_Tree.png", 
            150, 
            LootTable(
                LootEntry(WOOD, 2, 4, 3),
                LootEntry(WOOD, 1, 3, 7),
                rolls=1
            )
        )

class Rock(Harvestable):
    def __init__(self, position: pygame.Vector2):
        from InventorySystem import GOLD_ORE, IRON_ORE, STONE

        super().__init__(
            position, 
            Vector2(30, 30), 
            r"data/Sprites/rock.png", 
            200, 
            LootTable(
                LootEntry(GOLD_ORE, 1, 3, 1),
                LootEntry(IRON_ORE, 2, 4, 3),
                LootEntry(IRON_ORE, 3, 5, 7),
                rolls=2
            )
        )


ENTITIES: dict[str, type[Entity]] = {
    "Tree" : Tree,
    "Rock" : Rock,
    "CochonTronc": CochonTronc,
    "Dragon": Dragon
}

######################### WEAPON
################################

class Sword(MeleeWeapon):
    icon:str =  r"data/Sprites/icon_sword.png"

    def __init__(self):
        super().__init__(
            Vector2(0, 0), 
            pygame.Vector2(10, 20),
            r"data/Sprites/sword.png", 
            30, 
            20,
            0.3
        )

class MiniGun(RangedWeapon):
    icon:str = r"data/Sprites/icon_minigun.png"

    def __init__(self):
        super().__init__(
            Vector2(0, 0), 
            pygame.Vector2(20, 7), 
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
            pygame.Vector2(20, 7), 
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
            pygame.Vector2(20, 7), 
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
            Vector2(2, 1), 
            angle,
            r"data/Sprites/bullet.png", 
            10, 
            direction, 
            150, 
            2,
            owner
        )

class Rocket(Projectile):
    def __init__(self, position, angle, direction, owner):
        super().__init__(
            position, 
            Vector2(12, 5), 
            angle,
            r"data/Sprites/rocket.png",
            75, 
            direction, 
            350, 
            2,
            owner
        )

    def OnEnemyHit(self, enemy: Enemy):
        import random
        explosion_radius = 100

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
        explosion_radius = 100

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
            Vector2(12, 5), 
            angle,
            r"data/Sprites/flame.png",
            2, 
            direction, 
            200, 
            0.3,
            owner
        )

    def OnEnemyHit(self, enemy: Enemy):
        enemy.TakeDamage(self.damage)

    def OnHarvestableHit(self, object: Harvestable):
        object.TakeDamage(self.damage)

class FireBall(Projectile):
    def __init__(self, position, angle, direction, owner):
        super().__init__(
            position, 
            Vector2(5, 5), 
            angle,
            r"data/Sprites/fireball.png",
            30, 
            direction, 
            150, 
            2,
            owner
        )


##################### DIALOGUES
################################

class NPC1(NPC):
    def __init__(self, position:Vector2):
        super().__init__(
            position=position,
            size=Vector2(15, 15),
            sprite=r"data/sprites/paysan.png",
            interactRadius=30,
            dialogueQueue=Queue(
                Dialogue("Bonjour à toi, jeune aventurier !!", 2), 
                Dialogue("Les cochons troncs ont ravagés mes cultures, et menacent de m'attaquer !", 4),
                Dialogue("Pour la survie de ma famille, je te supplie de les pourfendre.", 3)
            ),
            name="Paysan"
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
