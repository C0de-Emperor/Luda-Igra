# Documentation Technique du Projet

## Fichier : Data.py

### <a name='Bullet'></a>Type de données : `Bullet`

**Hérite de :** [Projectile](#Projectile)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### <a name='CochonTronc'></a>Type de données : `CochonTronc`

**Hérite de :** [MeleeEnemy](#MeleeEnemy)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### <a name='Flame'></a>Type de données : `Flame`

**Hérite de :** [Projectile](#Projectile)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* OnEnemyHit(enemy: Objects.Enemy)
* OnHarvestableHit(object: Objects.Harvestable)

---

### <a name='FlameThrower'></a>Type de données : `FlameThrower`

**Hérite de :** [RangedWeapon](#RangedWeapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### <a name='MiniGun'></a>Type de données : `MiniGun`

**Hérite de :** [RangedWeapon](#RangedWeapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### <a name='Rocket'></a>Type de données : `Rocket`

**Hérite de :** [Projectile](#Projectile)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* OnEnemyHit(enemy: Objects.Enemy)
* OnHarvestableHit(object: Objects.Harvestable)

---

### <a name='RocketLaucher'></a>Type de données : `RocketLaucher`

**Hérite de :** [RangedWeapon](#RangedWeapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### <a name='Sword'></a>Type de données : `Sword`

**Hérite de :** [MeleeWeapon](#MeleeWeapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### <a name='Tree'></a>Type de données : `Tree`

**Hérite de :** [Harvestable](#Harvestable)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

## Fichier : Engine.py

## Fichier : InventorySystem.py

### <a name='CraftingManager'></a>Type de données : `CraftingManager`

**Attributs (propres) :**
* recipes : `list`
* craftingQueue : `Queue`

**Méthodes (propres) :**
* register(cls, recipe)
* get_craftable(cls)

---

### <a name='Inventory'></a>Type de données : `Inventory`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* add(resource, amount)
* remove(resource, amount)
* get(resource)

---

### <a name='ItemRecipe'></a>Type de données : `ItemRecipe`

**Hérite de :** `Recipe`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* craft()
* addToQueue()

---

### <a name='ItemStack'></a>Type de données : `ItemStack`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* add(quantity: int)
* remove(quantity: int)
* is_empty()

---

### <a name='Recipe'></a>Type de données : `Recipe`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* can_craft()
* craft()
* addToQueue()

---

### <a name='Resource'></a>Type de données : `Resource`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### <a name='ResourceManager'></a>Type de données : `ResourceManager`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* register(cls, resource)

---

### <a name='WeaponRecipe'></a>Type de données : `WeaponRecipe`

**Hérite de :** `Recipe`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* craft()
* addToQueue()

---

## Fichier : Main.py

## Fichier : Objects.py

### <a name='Camera'></a>Type de données : `Camera`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* get_screen_rect(world_rect: pygame.rect.Rect) -> pygame.rect.Rect
* world_to_screen_point(world_pos: pygame.math.Vector2) -> pygame.math.Vector2
* screen_to_world_point(screen_pos: pygame.math.Vector2) -> pygame.math.Vector2

---

### <a name='DroppedStack'></a>Type de données : `DroppedStack`

**Hérite de :** [Object](#Object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Render(screen, debug=False)
* Update(dt)

---

### <a name='Enemy'></a>Type de données : `Enemy`

**Hérite de :** [Entity](#Entity)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* _choose_wander_target()
* Render(screen, debug=False)
* Update(dt)
* _check_collision(walls, axis)

---

### <a name='Entity'></a>Type de données : `Entity`

**Hérite de :** [Object](#Object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* _render_health_bar(screen)
* TakeDamage(amount: float)
* Heal(amount: float)
* Die()

---

### <a name='Gate'></a>Type de données : `Gate`

**Hérite de :** [Object](#Object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Render(screen: pygame.surface.Surface, debug: bool = False)

---

### <a name='Harvestable'></a>Type de données : `Harvestable`

**Hérite de :** [Entity](#Entity)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Render(screen, debug=False)
* Die()
* _spawn_drop(stack)

---

### <a name='Hitbox'></a>Type de données : `Hitbox`

**Hérite de :** [Object](#Object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Render(screen, debug=False)

---

### <a name='LootEntry'></a>Type de données : `LootEntry`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

### <a name='LootTable'></a>Type de données : `LootTable`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* roll()

---

### <a name='MeleeEnemy'></a>Type de données : `MeleeEnemy`

**Hérite de :** [Enemy](#Enemy)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Attack()

---

### <a name='MeleeWeapon'></a>Type de données : `MeleeWeapon`

**Hérite de :** [Weapon](#Weapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Attack()

---

### <a name='Object'></a>Type de données : `Object`

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

### <a name='Player'></a>Type de données : `Player`

**Hérite de :** [Entity](#Entity)

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

### <a name='Projectile'></a>Type de données : `Projectile`

**Hérite de :** [Object](#Object)

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

### <a name='RangedWeapon'></a>Type de données : `RangedWeapon`

**Hérite de :** [Weapon](#Weapon)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Update(dt)
* Attack()

---

### <a name='SpawnArea'></a>Type de données : `SpawnArea`

**Hérite de :** [Object](#Object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* _spawn()
* Update(dt)
* Render(screen: pygame.surface.Surface, debug: bool = False)

---

### <a name='Weapon'></a>Type de données : `Weapon`

**Hérite de :** [Object](#Object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Render(screen, debug=False)
* Update(dt)
* Attack()

---

## Fichier : SceneManager.py

### <a name='Scene'></a>Type de données : `Scene`

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* GetAllColliders(ignoreObjects: list[Objects.Object] = None) -> list[pygame.rect.Rect]
* load(point: str)

---

## Fichier : TilemapManager.py

### <a name='Tilemap'></a>Type de données : `Tilemap`

**Hérite de :** [Object](#Object)

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

### <a name='Queue'></a>Type de données : `Queue`

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

### <a name='CraftingQueueUI'></a>Type de données : `CraftingQueueUI`

**Hérite de :** [UIElement](#UIElement)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* Render(screen, debug=False)

---

### <a name='CraftingUI'></a>Type de données : `CraftingUI`

**Hérite de :** [UIElement](#UIElement)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* get_height()
* HandleEvent(event)
* Update(dt)
* Render(screen, debug=False)

---

### <a name='InventoryUI'></a>Type de données : `InventoryUI`

**Hérite de :** [UIElement](#UIElement)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* HandleEvent(event)
* Render(screen: pygame.surface.Surface, debug: bool = False)

---

### <a name='ItemNotification'></a>Type de données : `ItemNotification`

**Hérite de :** [UIElement](#UIElement)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* get_offset_y(index)
* Update(dt)
* Render(screen, DEBUG)
* Destroy()

---

### <a name='UIElement'></a>Type de données : `UIElement`

**Hérite de :** [Object](#Object)

**Attributs (propres) :**
* (Aucun attribut spécifique détecté)

**Méthodes (propres) :**
* (Aucune méthode spécifique)

---

