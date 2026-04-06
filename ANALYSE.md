# Document d'analyse du projet
_réalisé à l'aide de la bibliothèque inspect et d'une IA_

## Fichier : Data.py

### Type de données : `Bullet`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* OnEnemyHit(enemy: Objects.Enemy)
* OnEntityHit(entity: Objects.Entity)
* OnHarvestableHit(object: 'Harvestable')
* OnWallHit()
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `CochonTronc`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Attack()
* Destroy()
* Die()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* Heal(amount: float)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* TakeDamage(amount: float)
* Update(dt)
* _check_collision(walls, axis)
* _choose_wander_target()
* _render_health_bar(screen)

---

### Type de données : `Flame`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* OnEnemyHit(enemy: Objects.Enemy)
* OnEntityHit(entity: Objects.Entity)
* OnHarvestableHit(object: Objects.Harvestable)
* OnWallHit()
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `FlameThrower`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Attack()
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `MiniGun`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Attack()
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `Rocket`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* OnEnemyHit(enemy: Objects.Enemy)
* OnEntityHit(entity: Objects.Entity)
* OnHarvestableHit(object: Objects.Harvestable)
* OnWallHit()
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `RocketLaucher`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Attack()
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `Sword`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Attack()
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `Tree`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* Die()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* Heal(amount: float)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* TakeDamage(amount: float)
* Update(dt)
* _render_health_bar(screen)
* _spawn_drop(stack)

---

## Fichier : Engine.py

**Erreur sur InventorySystem** : cannot convert without pygame.display initialized

## Fichier : Main.py

## Fichier : Objects.py

### Type de données : `Camera`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* get_screen_rect(world_rect: pygame.rect.Rect) -> pygame.rect.Rect
* screen_to_world_point(screen_pos: pygame.math.Vector2) -> pygame.math.Vector2
* world_to_screen_point(world_pos: pygame.math.Vector2) -> pygame.math.Vector2

---

### Type de données : `DroppedStack`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `Enemy`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* Die()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* Heal(amount: float)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* TakeDamage(amount: float)
* Update(dt)
* _check_collision(walls, axis)
* _choose_wander_target()
* _render_health_bar(screen)

---

### Type de données : `Entity`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* Die()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* Heal(amount: float)
* LoadSprite(sprite: str, scale: bool)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* TakeDamage(amount: float)
* Update(dt)
* _render_health_bar(screen)

---

### Type de données : `Gate`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* Update(dt)

---

### Type de données : `Harvestable`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* Die()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* Heal(amount: float)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* TakeDamage(amount: float)
* Update(dt)
* _render_health_bar(screen)
* _spawn_drop(stack)

---

### Type de données : `Hitbox`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `LootEntry`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* (Aucune méthode publique)

---

### Type de données : `LootTable`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* roll()

---

### Type de données : `MeleeEnemy`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Attack()
* Destroy()
* Die()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* Heal(amount: float)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* TakeDamage(amount: float)
* Update(dt)
* _check_collision(walls, axis)
* _choose_wander_target()
* _render_health_bar(screen)

---

### Type de données : `MeleeWeapon`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Attack()
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `Object`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* Update(dt)

---

### Type de données : `Player`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* ChangeTool(direction)
* Destroy()
* Die()
* GetColliders()
* HandleEvent(event)
* Heal(amount: float)
* LoadSprite(sprite: str, scale: bool)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* TakeDamage(amount: float)
* Update(dt)
* _check_collision(walls, axis)
* _get_movement_direction() -> pygame.math.Vector2
* _render_health_bar(screen: pygame.surface.Surface)

---

### Type de données : `Projectile`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* OnEnemyHit(enemy: Objects.Enemy)
* OnEntityHit(entity: Objects.Entity)
* OnHarvestableHit(object: 'Harvestable')
* OnWallHit()
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `RangedWeapon`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Attack()
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `SpawnArea`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* Update(dt)
* _spawn()

---

### Type de données : `Weapon`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Attack()
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

## Fichier : SceneManager.py

### Type de données : `Scene`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* GetAllColliders(ignoreObjects: list[Objects.Object] = None) -> list[pygame.rect.Rect]
* load(point: str)

---

## Fichier : TilemapManager.py

### Type de données : `Tilemap`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* Update(dt)
* _load_collisions()
* _load_gates()
* _load_points()
* _load_spawn_Area()

---

## Fichier : Tools.py

### Type de données : `Queue`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* dequeue() -> ~T
* enqueue(value: ~T)
* getLen() -> int
* isEmpty() -> bool
* peek()
* rotate()

---

## Fichier : UI.py

### Type de données : `CraftingQueueUI`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)

---

### Type de données : `CraftingUI`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, debug=False)
* Update(dt)
* get_height()

---

### Type de données : `InventoryUI`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* Update(dt)

---

### Type de données : `ItemNotification`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen, DEBUG)
* Update(dt)
* get_offset_y(index)

---

### Type de données : `UIElement`

**Attributs :**
* (Aucun attribut détecté)

**Méthodes :**
* Destroy()
* GetColliders() -> list[pygame.rect.Rect]
* HandleEvent(event)
* LoadSprite(sprite: str, scale: bool)
* Render(screen: pygame.surface.Surface, debug: bool = False)
* Update(dt)

---

