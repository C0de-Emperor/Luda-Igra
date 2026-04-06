# Document d'Analyse du Projet
_réalisé avec la bibliothèque inspect et une IA_

## Fichier : Data.py

### Bullet

**Hérite de :** [Projectile](#projectile)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### CochonTronc

**Hérite de :** [MeleeEnemy](#meleeenemy)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### Flame

**Hérite de :** [Projectile](#projectile)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* OnEnemyHit(enemy: Objects.Enemy)
* OnHarvestableHit(object: Objects.Harvestable)

---

### FlameThrower

**Hérite de :** [RangedWeapon](#rangedweapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### MiniGun

**Hérite de :** [RangedWeapon](#rangedweapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### Rocket

**Hérite de :** [Projectile](#projectile)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* OnEnemyHit(enemy: Objects.Enemy)
* OnHarvestableHit(object: Objects.Harvestable)

---

### RocketLaucher

**Hérite de :** [RangedWeapon](#rangedweapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### Sword

**Hérite de :** [MeleeWeapon](#meleeweapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### Tree

**Hérite de :** [Harvestable](#harvestable)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

## Fichier : Engine.py

## Fichier : InventorySystem.py

### CraftingManager

**Attributs (propres) :**
* recipes : `list`
* craftingQueue : `Queue`

**Méthodes (propres) :**
* register(cls, recipe)
* get_craftable(cls)

---

### Inventory

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* add(resource, amount)
* remove(resource, amount)
* get(resource)

---

### ItemRecipe

**Hérite de :** `Recipe`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* craft()
* addToQueue()

---

### ItemStack

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* add(quantity: int)
* remove(quantity: int)
* is_empty()

---

### Recipe

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* can_craft()
* craft()
* addToQueue()

---

### Resource

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### ResourceManager

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* register(cls, resource)

---

### WeaponRecipe

**Hérite de :** `Recipe`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* craft()
* addToQueue()

---

## Fichier : Main.py

## Fichier : Objects.py

### Camera

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* get_screen_rect(world_rect: pygame.rect.Rect) -> pygame.rect.Rect
* world_to_screen_point(world_pos: pygame.math.Vector2) -> pygame.math.Vector2
* screen_to_world_point(screen_pos: pygame.math.Vector2) -> pygame.math.Vector2

---

### DroppedStack

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Render(screen, debug=False)
* Update(dt)

---

### Enemy

**Hérite de :** [Entity](#entity)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* _choose_wander_target()
* Render(screen, debug=False)
* Update(dt)
* _check_collision(walls, axis)

---

### Entity

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* _render_health_bar(screen)
* TakeDamage(amount: float)
* Heal(amount: float)
* Die()

---

### Gate

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Render(screen: pygame.surface.Surface, debug: bool = False)

---

### Harvestable

**Hérite de :** [Entity](#entity)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Render(screen, debug=False)
* Die()
* _spawn_drop(stack)

---

### Hitbox

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Render(screen, debug=False)

---

### LootEntry

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### LootTable

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* roll()

---

### MeleeEnemy

**Hérite de :** [Enemy](#enemy)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Attack()

---

### MeleeWeapon

**Hérite de :** [Weapon](#weapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Attack()

---

### Object

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* HandleEvent(event)
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* LoadSprite(sprite: str, scale: bool)

---

### Player

**Hérite de :** [Entity](#entity)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* _get_movement_direction() -> pygame.math.Vector2
* _check_collision(walls, axis)
* Update(dt)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* HandleEvent(event)
* GetColliders()
* ChangeTool(direction)
* _render_health_bar(screen: pygame.surface.Surface)
* Destroy()
* Die()

---

### Projectile

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Render(screen, debug=False)
* OnEnemyHit(enemy: Objects.Enemy)
* OnHarvestableHit(object: 'Harvestable')
* OnEntityHit(entity: Objects.Entity)
* OnWallHit()

---

### RangedWeapon

**Hérite de :** [Weapon](#weapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Attack()

---

### SpawnArea

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* _spawn()
* Update(dt)
* Render(screen: pygame.surface.Surface, debug: bool = False)

---

### Weapon

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Render(screen, debug=False)
* Update(dt)
* Attack()

---

## Fichier : SceneManager.py

### Scene

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* GetAllColliders(ignoreObjects: list[Objects.Object] = None) -> list[pygame.rect.Rect]
* load(point: str)

---

## Fichier : TilemapManager.py

### Tilemap

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* _load_spawn_Area()
* _load_collisions()
* _load_points()
* _load_gates()
* Render(screen: pygame.surface.Surface, debug: bool = False)
* GetColliders() -> list[pygame.rect.Rect]

---

## Fichier : Tools.py

### Queue

**Hérite de :** `Generic`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* enqueue(value: ~T)
* dequeue() -> ~T
* getLen() -> int
* isEmpty() -> bool
* rotate()
* peek()

---

## Fichier : UI.py

### CraftingQueueUI

**Hérite de :** [UIElement](#uielement)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Render(screen, debug=False)

---

### CraftingUI

**Hérite de :** [UIElement](#uielement)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* get_height()
* HandleEvent(event)
* Update(dt)
* Render(screen, debug=False)

---

### InventoryUI

**Hérite de :** [UIElement](#uielement)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* HandleEvent(event)
* Render(screen: pygame.surface.Surface, debug: bool = False)

---

### ItemNotification

**Hérite de :** [UIElement](#uielement)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* get_offset_y(index)
* Update(dt)
* Render(screen, DEBUG)
* Destroy()

---

### UIElement

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

