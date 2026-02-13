import pygame, pytmx, pyscroll

class Tilemap:
    def __init__(self, tilemapPath):
        self.tmx_data = pytmx.load_pygame(tilemapPath)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)

        self.collisions=[]
        for coll in self.tmx_data.get_layer_by_name("Collisions"):
            self.collisions.append(pygame.Rect(coll.x, coll.y, coll.width, coll.height))
        
        self.spawnPoint = (self.tmx_data.get_object_by_name("spawnPoint").x, self.tmx_data.get_object_by_name("spawnPoint").y)
    
    def loadTilemap(self, screen):
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, screen.get_size())
        self.group = pyscroll.PyscrollGroup(self.map_layer, default_layer=0)

class Biome:
    def __init__(self, biomePath, tilemapPaths, tileMapAutomatMatrix):
        self.biomePath=biomePath

        self.tilemaps:list[Tilemap]=[]
        for path in tilemapPaths:
            self.tilemaps.append(Tilemap("data/tilemaps/"+path))
        
        self.tileMapAutomatMatrix = tileMapAutomatMatrix


pygame.init()
pygame.key.set_repeat(200, 1)
screen=pygame.display.set_mode((800, 800), pygame.RESIZABLE)

biomeTest=Biome("", ["carte.tmx"], [])
tm=biomeTest.tilemaps[0]

playerRect=pygame.Rect(0,0,10,10)
playerRect.x, playerRect.y=tm.spawnPoint

tm.loadTilemap(screen)

running=True
while running:
    for k in pygame.event.get():
        if k.type == pygame.QUIT:
            running=False
        if k.type == pygame.KEYDOWN:
            playerRect.x += 10
            playerRect.y += 10

    print(playerRect.x, playerRect.y)
    tm.group.center(playerRect)
    tm.group.draw(screen)

    pygame.display.flip()

pygame.quit()