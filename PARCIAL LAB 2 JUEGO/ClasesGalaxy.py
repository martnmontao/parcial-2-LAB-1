import pygame
import random

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Imagenes juego/NAVE.png")
        self.rect = self.image.get_rect()
        self.salud = 100
        self.rect.x = 400
    def update(self):
        lista_tecla = pygame.key.get_pressed()
        self.rect.y = 740
        if lista_tecla[pygame.K_d]:
            self.rect.x += 8
        if lista_tecla[pygame.K_a]:
            self.rect.x -= 8
        if self.rect.x > 840:
            self.rect.x = 840
        if self.rect.x < 0:
            self.rect.x = 0
        return self.rect
    
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Imagenes juego/laser.png")
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y -= 8

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Imagenes juego/ENEMIGO.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(900 - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 5)
        self.velocidad_x = random.randrange(-3, 3)
    def update(self):
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        if self.rect.y > 800:
            self.rect.y = 0
        if self.rect.x > 900:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = 900

class LaserEnemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Imagenes juego/laser.png")
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y += 5

explosion_animacion = []

for imagen in range(9):
    path = f"Imagenes juego/explosion{imagen}.png"
    imagen_explosion = pygame.image.load(path)
    explosion_animacion.append(imagen_explosion)

class Explosion(pygame.sprite.Sprite):
    def __init__(self,centrar):
        super().__init__()
        self.image = explosion_animacion[0]
        self.rect = self.image.get_rect()
        self.rect.center = centrar
        self.frame = 0
        #self.tiempo_transcurrido = pygame.time.get_ticks()#Analiza en que segundo del juego ocurre una colision para hacer la animacion
        #self.velocidad_animacion = 50#Velocidad de la explosion
    def update(self):
        #ahora = pygame.time.get_ticks()#Toma el tiempo que tarda la animacion de la explosion
        #if ahora - self.tiempo_transcurrido > self.velocidad_animacion:
            #self.tiempo_transcurrido = ahora
        self.frame += 1
        if self.frame == len(explosion_animacion):
            self.kill()
        else:
            centrar = self.rect.center 
            self.image = explosion_animacion[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = centrar
        







