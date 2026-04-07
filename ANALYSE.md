# Document d'Analyse du Projet
_réalisé avec la bibliothèque inspect_

## Fichier : Data.py

### Bullet

**Hérite de :** [Projectile](#projectile)

**Attributs (propres) :**
* (Aucun attribut propre détecté)

**Méthodes (propres) :**
* (Aucune méthode propre)

---

### CochonTronc

**Hérite de :** [MeleeEnemy](#meleeenemy)

**Attributs (propres) :**
* (Aucun attribut propre détecté)

**Méthodes (propres) :**
* (Aucune méthode propre)

---

### Flame

**Hérite de :** [Projectile](#projectile)

**Attributs (propres) :**
* (Aucun attribut propre détecté)

**Méthodes (propres) :**
* OnEnemyHit(enemy: Objects.Enemy)
* OnHarvestableHit(object: Objects.Harvestable)

---

### FlameThrower

**Hérite de :** [RangedWeapon](#rangedweapon)

**Attributs (propres) :**
* icon : `str`

**Méthodes (propres) :**
* (Aucune méthode propre)

---

### MiniGun

**Hérite de :** [RangedWeapon](#rangedweapon)

**Attributs (propres) :**
* icon : `str`

**Méthodes (propres) :**
* (Aucune méthode propre)

---

### Rocket

**Hérite de :** [Projectile](#projectile)

**Attributs (propres) :**
* (Aucun attribut propre détecté)

**Méthodes (propres) :**
* OnEnemyHit(enemy: Objects.Enemy)
* OnHarvestableHit(object: Objects.Harvestable)

---

### RocketLaucher

**Hérite de :** [RangedWeapon](#rangedweapon)

**Attributs (propres) :**
* icon : `str`

**Méthodes (propres) :**
* (Aucune méthode propre)

---

### Sword

**Hérite de :** [MeleeWeapon](#meleeweapon)

**Attributs (propres) :**
* icon : `str`

**Méthodes (propres) :**
* (Aucune méthode propre)

---

### Tree

**Hérite de :** [Harvestable](#harvestable)

**Attributs (propres) :**
* (Aucun attribut propre détecté)

**Méthodes (propres) :**
* (Aucune méthode propre)

---

## Fichier : Engine.py

## Fichier : InventorySystem.py

### CraftingManager

**Attributs (propres) :**
* craftingQueue : `Queue`
* recipes : `list`

**Méthodes (propres) :**
* register(recipe)
* get_craftable()

---

### Inventory

**Attributs (propres) :**
* UI : `InventoryUI`
* craftingQueueUI : `CraftingQueueUI`
* craftingUI : `CraftingUI`
* padding : `float`
* slot_size : `int`

**Méthodes (propres) :**
* add(resource, amount)
* remove(resource, amount)
* get(resource)

---

### ItemRecipe

**Hérite de :** `Recipe`

**Attributs (propres) :**
* output : `ItemStack`

**Méthodes (propres) :**
* craft()
* addToQueue()

---

### ItemStack

**Attributs (propres) :**
* amount : `int`
* resource : `Resource`

**Méthodes (propres) :**
* add(quantity: int)
* remove(quantity: int)
* is_empty()

---

### Recipe

**Attributs (propres) :**
* duration : `float`
* inputs : `list[ItemStack]`
* isCraftable : `bool`

**Méthodes (propres) :**
* can_craft()
* craft()
* addToQueue()

---

### Resource

**Attributs (propres) :**
* icon : `str`
* name : `str`

**Méthodes (propres) :**
* (Aucune méthode propre)

---

### ResourceManager

**Attributs (propres) :**
* resources : `list`

**Méthodes (propres) :**
* register(resource)

---

### WeaponRecipe

**Hérite de :** `Recipe`

**Attributs (propres) :**
* isCraftable : `any`
* output : `type[Weapon]`

**Méthodes (propres) :**
* craft()
* addToQueue()

---

## Fichier : Main.py

## Fichier : Objects.py

### Camera

**Attributs (propres) :**
* (Aucun attribut propre détecté)

**Méthodes (propres) :**
* get_screen_rect(world_rect: pygame.rect.Rect) -> pygame.rect.Rect
* world_to_screen_point(world_pos: pygame.math.Vector2) -> pygame.math.Vector2
* screen_to_world_point(screen_pos: pygame.math.Vector2) -> pygame.math.Vector2

---

### DroppedStack

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* stack : `ItemStack`

**Méthodes (propres) :**
* Render(screen, debug=False)
* Update(dt)

---

### Enemy

**Hérite de :** [Entity](#entity)

**Attributs (propres) :**
* attackDmg : `float`
* directionTimer : `float`
* isChasing : `bool`
* patrolDelay : `float`
* sightRadius : `float`
* speed : `float`
* stopDuration : `float`
* stopTimer : `float`
* wanderRadius : `float`
* wanderTarget : `any`

**Méthodes (propres) :**
* _choose_wander_target()
* Render(screen, debug=False)
* Update(dt)
* _check_collision(walls, axis)

---

### Entity

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* baseHealth : `float`
* health : `float`

**Méthodes (propres) :**
* _render_health_bar(screen)
* TakeDamage(amount: float)
* Heal(amount: float)
* Die()

---

### Gate

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* destination : `str`
* name : `str`

**Méthodes (propres) :**
* Update(dt)
* Render(screen: pygame.surface.Surface, debug: bool = False)

---

### Harvestable

**Hérite de :** [Entity](#entity)

**Attributs (propres) :**
* lootTable : `LootTable`

**Méthodes (propres) :**
* Render(screen, debug=False)
* Die()
* _spawn_drop(stack)

---

### Hitbox

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* angle : `float`
* damage : `float`
* hitEnemies : `list[Object]`
* lifetime : `float`
* owner : `Object`

**Méthodes (propres) :**
* Update(dt)
* Render(screen, debug=False)

---

### LootEntry

**Attributs (propres) :**
* max_amount : `int`
* min_amount : `int`
* resource : `Resource`
* weight : `float`

**Méthodes (propres) :**
* (Aucune méthode propre)

---

### LootTable

**Attributs (propres) :**
* entries : `LootEntry`
* rolls : `int`

**Méthodes (propres) :**
* roll()

---

### MeleeEnemy

**Hérite de :** [Enemy](#enemy)

**Attributs (propres) :**
* attackCooldown : `float`
* attackRange : `float`
* attackTimer : `float`

**Méthodes (propres) :**
* Update(dt)
* Attack()

---

### MeleeWeapon

**Hérite de :** [Weapon](#weapon)

**Attributs (propres) :**
* attack_range : `float`
* attack_timer : `float`
* cooldown : `float`
* damage : `float`

**Méthodes (propres) :**
* Update(dt)
* Attack()

---

### Object

**Attributs (propres) :**
* destroyOnLoad : `bool`
* size : `Vector2`
* sprite : `any`

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
* currentTool : `type[Weapon]`
* inventory : `Inventory`
* player : `Player`
* recipeProcessTimer : `float`
* recipeToProcess : `Recipe`
* speed : `float`
* tools : `Queue`

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
* angle : `float`
* damage : `float`
* direction : `Vector2`
* lifetime : `float`
* owner : `Object`
* speed : `float`

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
* angleDeviation : `float`
* attack_range : `float`
* attack_timer : `float`
* bullet : `type[Projectile]`
* cooldown : `float`

**Méthodes (propres) :**
* Update(dt)
* Attack()

---

### SpawnArea

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* count : `int`
* delay : `int`
* entity : `type[Entity]`
* maxSpawnCount : `int`
* timer : `float`

**Méthodes (propres) :**
* _spawn()
* Update(dt)
* Render(screen: pygame.surface.Surface, debug: bool = False)

---

### Weapon

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* angle : `any`
* offset : `Vector2`
* offset_distance : `float`
* position : `any`

**Méthodes (propres) :**
* Render(screen, debug=False)
* Update(dt)
* Attack()

---

## Fichier : SceneManager.py

### Scene

**Attributs (propres) :**
* name : `str`
* objects : `list[Object]`
* tilemap : `any`

**Méthodes (propres) :**
* GetAllColliders(ignoreObjects: list[Objects.Object] = None) -> list[pygame.rect.Rect]
* load(point: str)

---

## Fichier : TilemapManager.py

### Tilemap

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* camera_offset : `any`
* collisions : `screen_rect`
* path : `str`
* tmx_data : `Tilemap`

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
* elements : `list`

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
* crafting_ui : `CraftingUI`
* icon_size : `float`
* spacing : `float`

**Méthodes (propres) :**
* Render(screen, debug=False)

---

### CraftingUI

**Hérite de :** [UIElement](#uielement)

**Attributs (propres) :**
* delay : `float`
* show : `bool`
* slotHeight : `int`

**Méthodes (propres) :**
* get_height()
* HandleEvent(event)
* Update(dt)
* Render(screen, debug=False)

---

### InventoryUI

**Hérite de :** [UIElement](#uielement)

**Attributs (propres) :**
* inventory : `Inventory`
* show : `any`

**Méthodes (propres) :**
* HandleEvent(event)
* Render(screen: pygame.surface.Surface, debug: bool = False)

---

### ItemNotification

**Hérite de :** [UIElement](#uielement)

**Attributs (propres) :**
* amount : `int`
* lifetime : `float`
* max_lifetime : `float`
* notifications : `list`
* position : `any`
* resource : `Resource`

**Méthodes (propres) :**
* get_offset_y(index)
* Update(dt)
* Render(screen, DEBUG)
* Destroy()

---

### UIElement

**Hérite de :** [Object](#object)

**Attributs (propres) :**
* (Aucun attribut propre détecté)

**Méthodes (propres) :**
* (Aucune méthode propre)

---

