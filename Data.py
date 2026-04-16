from Objects import *
from DialogueSystem import Dialogue

######################### ENTITY
################################

class CochonTronc(MeleeEnemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(
            position, 
            size = Vector2(20, 20), 
            sprite = r"data/Sprites/cochonTronc2.png", 
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
    
    def Die(self):
        self.Destroy()
        
        from Engine import trigger_game_won
        trigger_game_won()

class Taupe(MeleeEnemy):
    def __init__(self, position: pygame.Vector2):
        super().__init__(
            position, 
            size = Vector2(20, 20), 
            sprite = r"data/Sprites/taupe.png", 
            baseHealth = 80, 
            attackDmg = 8, 
            speed = 32, 
            sightRadius = 300, 
            wanderRadius = 400, 
            patrolDelay = 6, 
            stopDuration = 2,
            attackCooldown = 2,
            attackRange = 50,
            attackSprite=r"data/Sprites/slash.png"
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
                LootEntry(STONE, 3, 5, 7),
                rolls=2
            )
        )


ENTITIES: dict[str, type[Entity]] = {
    "Tree" : Tree,
    "Rock" : Rock,
    "CochonTronc": CochonTronc,
    "Taupe" : Taupe,
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
            sprite=r"data/sprites/cochonTronc.png",
            interactRadius=30,
            dialogueQueue=Queue(
                Dialogue("Jeune prince Ljubazni Junak !!! Je vous attendais !", 5), 
                Dialogue("Pendant votre absence, le dragon maléfique Gnusni Zlikovac a envahi le royaume avec ses sbires.",7),
                Dialogue("Votre père, le roi, fut dévoré par le dragon après 3 jours de combats,", 6),
                Dialogue("Par pitié, libérez le royaume de son joug et terrassez les sbires du dragon !", 5)
            ),
            name="Chambellan"
        )

class NPC2(NPC):
    def __init__(self, position:Vector2):
        super().__init__(
            position=position,
            size=Vector2(15, 15),
            sprite=r"data/sprites/toruk_makto.png",
            interactRadius=30,
            dialogueQueue=Queue(
                Dialogue("Vous voila enfin de retour, jeune prince !", 5), 
                Dialogue("N'oubliez pas l'entraînement que je vous ai prodigué ces 10 dernières années,", 5),
                Dialogue("Utilisez ZQSD pour vous déplacer et clic-gauche pour attaquer.", 7),
                Dialogue("Aussi, n'oubliez pas: si vous avez plusieurs armes, utilisez la molette pour passer de l'une à l'autre !", 8)
            ),
            name="Maitre d'armes"
        )

class NPC3(NPC):
    def __init__(self, position:Vector2):
        super().__init__(
            position=position,
            size=Vector2(15, 15),
            sprite=r"data/sprites/paysanDos.png",
            interactRadius=30,
            dialogueQueue=Queue(
                Dialogue("Vous voulez récolter ce bois ci ?", 5), 
                Dialogue("Pas de problème, mettez-y quelques coup d'épée pour les couper,", 5),
                Dialogue("Regardez intensément les souches coupées pour les récupérer,", 7),
                Dialogue("Je vous rappelle que votre sac à dos s'ouvre en appuyant sur E.", 7)
            ),
            name="Bûcheron"
        )

class NPC4(NPC):
    def __init__(self, position:Vector2):
        super().__init__(
            position=position,
            size=Vector2(15, 15),
            sprite=r"data/sprites/paysan.png",
            interactRadius=30,
            dialogueQueue=Queue(
                Dialogue("Messire, messire !", 2), 
                Dialogue("Les ignobles cochons troncs ont envahi la plaine voisine ;", 5),
                Dialogue("Il pourraient attaquer ma ferme et ma famille à n'importe quel moment", 5),
                Dialogue("Je vous implore de les terrasser au plus vite possible!", 5)
            ),
            name="Paysan"
        )

class NPC5(NPC):
    def __init__(self, position:Vector2):
        super().__init__(
            position=position,
            size=Vector2(15, 15),
            sprite=r"data/sprites/paysan.png",
            interactRadius=30,
            dialogueQueue=Queue(
                Dialogue("Comment forger ?", 5), 
                Dialogue("Il faut aller demander au maître artisan, mais il est emprisonné par les taupes maléfiques au fond de la mine!", 7),
                Dialogue("Allez le lui demander en personne, il est très sympathique!", 5)
            ),
            name="Mineur"
        )

class NPC6(NPC):
    def __init__(self, position:Vector2):
        super().__init__(
            position=position,
            size=Vector2(15, 15),
            sprite=r"data/sprites/paysan.png",
            interactRadius=30,
            dialogueQueue=Queue(
                Dialogue("Comment forger ?", 5), 
                Dialogue("C'est très simple voyons !", 5),
                Dialogue("Il suffit de disposer des bon matériaux et d'appuyer sur C.", 7)
            ),
            name="Maître artisan"
        )

class NPC7(NPC):
    def __init__(self, position:Vector2):
        super().__init__(
            position=position,
            size=Vector2(15, 15),
            sprite=r"data/sprites/paysan.png",
            interactRadius=30,
            dialogueQueue=Queue(
                Dialogue("Les monstres ont saccagé toute la ville, toute ma famille a été dévorée,", 5), 
                Dialogue("Vengez moi et terrassez ces ignobles monstres !", 5),
            ),
            name="Habitant"
        )

class NPC8(NPC):
    def __init__(self, position:Vector2):
        super().__init__(
            position=position,
            size=Vector2(15, 15),
            sprite=r"data/sprites/paysan.png",
            interactRadius=30,
            dialogueQueue=Queue(
                Dialogue("J'ai entendu des exilés dire que le dragon a pris pied à l'ouest du royaume !", 7), 
                Dialogue("Et d'autres m'ont confié qu'il y existe un portail magique, permettant de se mettre hors de portée du dragon !", 7),
            ),
            name="Tavernier"
        )


NPCS: dict[str, type[NPC]] ={
    "NPC1": NPC1,
    "NPC2": NPC2,
    "NPC3": NPC3,
    "NPC4": NPC4,
    "NPC5": NPC5,
    "NPC6": NPC6,
    "NPC7": NPC7,
    "NPC8": NPC8
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
