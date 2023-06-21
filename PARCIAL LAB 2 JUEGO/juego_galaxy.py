import pygame
import ClasesGalaxy
import funcionesGalaxy
ROJO = (255,0,0)
DARKSLATEBLUE = (72, 61, 139)
DARKVIOLET=(148, 0, 211)
DARK = (0,0,0)

funcionesGalaxy.crear_base_datos("baseDatosGalaxy.db")
  
def menu() -> str:   
    pygame.init()
    pygame.display.set_caption("Galaxy premium")
    iniciar_juego = False
    imagen_fondo = pygame.image.load("Imagenes juego/FONDOESPACIO.jpg")
    imagen_enter_name = pygame.image.load("Imagenes juego/NOMBRE.png")
    pygame.mixer.music.load("Sonidos juego/musicaMenu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops = -1)

    dimension = (900,800)
    pantalla = pygame.display.set_mode(dimension)
    ingresar_nombre = pygame.font.SysFont("gamer",40)
    ingreso = ""
    ingreso_rect = pygame.Rect(310,400,280,40)
    correr_juego = True

    while correr_juego:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr_juego = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                     iniciar_juego = True            
                if evento.key == pygame.K_BACKSPACE:
                    ingreso = ingreso[0:-1]
                else:
                     ingreso += evento.unicode
                            
        if len(ingreso) > 18 or iniciar_juego == True:
            ingreso = ingreso[0:-1]

        if iniciar_juego == True:
             return ingreso
        
        pantalla.blit(imagen_fondo, [0,0])

        pygame.draw.rect(pantalla,DARKSLATEBLUE,(175,300,563,65))#Fondo de enter name
        pantalla.blit(imagen_enter_name, (175,300))

        pygame.draw.rect(pantalla,DARKSLATEBLUE, ingreso_rect)#Fondo donde se ingresa el nombre
        pygame.draw.rect(pantalla, DARKVIOLET, ingreso_rect, 4)#Borde del fondo donde se ingresa el nombre

        ingresar_nombre_superficie = ingresar_nombre.render(ingreso, True, DARK)#Color de la letra             
        pantalla.blit(ingresar_nombre_superficie,(ingreso_rect.x + 5,ingreso_rect.y + 5))#Donde se dibuja el rectangulo donde se ingresa el nombre
        pygame.display.flip()
    pygame.quit()

def juego(nombre):
    pygame.init()
    pygame.display.set_caption("Galaxy premium")

    fps = pygame.time.Clock()

    dimension = (1200,800)

    pantalla = pygame.display.set_mode(dimension)

    correr_juego = True

    fondo_imagen = pygame.image.load("Imagenes juego/FONDOESPACIO.jpg")
    fondo_ranking = pygame.image.load("Imagenes juego/puntajeRanking1.png")

    sonido_laser = pygame.mixer.Sound("Sonidos juego/disparolaser.mp3")
    sonido_laser.set_volume(0.1)

    sonido_explosion_nave = pygame.mixer.Sound("Sonidos juego/explosionNave.mp3")
    sonido_explosion_nave.set_volume(0.2)

    sonido_daño_nave = pygame.mixer.Sound("Sonidos juego/dañoNave.mp3")
    sonido_daño_nave.set_volume(0.4)

    pygame.mixer.music.load("Sonidos juego/musicaFondo.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

    lista_sprites = pygame.sprite.Group()
    lista_laser = pygame.sprite.Group()
    lista_enemigos = pygame.sprite.Group()
    lista_laser_enemigo = pygame.sprite.Group()

    fuente_texto_score = pygame.font.SysFont("gamer",50)
    texto_score = fuente_texto_score.render("Score:", True, ROJO)


    for i in range(5):
        enemigos = ClasesGalaxy.Enemigo()   
        lista_enemigos.add(enemigos)
        lista_sprites.add(enemigos)
        

    nave = ClasesGalaxy.Nave()
    lista_sprites.add(nave)

    milisegundos_transcurridos = pygame.USEREVENT
    pygame.time.set_timer(milisegundos_transcurridos, 1000)

    score = 0
    
    while correr_juego:
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr_juego = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    sonido_laser.play()
                    laser = ClasesGalaxy.Laser()
                    laser.rect.x = nave.rect.x + 25
                    laser.rect.y = nave.rect.y - 15
                    lista_sprites.add(laser)
                    lista_laser.add(laser)
            if evento.type == milisegundos_transcurridos:
                    laser_enemigo = ClasesGalaxy.LaserEnemigo()
                    laser_enemigo.rect.x = enemigos.rect.x + 16
                    laser_enemigo.rect.y = enemigos.rect.y + 50
                    lista_laser_enemigo.add(laser_enemigo)
                    lista_sprites.add(laser_enemigo)

        golpes_con_enemigo = pygame.sprite.spritecollide(nave, lista_enemigos, True)   
        golpes_laser_enemigo = pygame.sprite.spritecollide(nave, lista_laser_enemigo, True)
        if golpes_laser_enemigo or golpes_con_enemigo:
            nave.salud -= 25
            sonido_daño_nave.play()
            if nave.salud == 0: 
                correr_juego = False

        golpes_laser = pygame.sprite.groupcollide(lista_laser, lista_enemigos, True, True)
        for golpe in golpes_laser:
            sonido_explosion_nave.play()
            score += 100
            explosion = ClasesGalaxy.Explosion(golpe.rect.center)     
            enemigos = ClasesGalaxy.Enemigo()
            lista_sprites.add(enemigos)
            lista_enemigos.add(enemigos)
            lista_sprites.add(explosion)
      
        lista_sprites.update() 
      
        pantalla.blit(fondo_imagen,(0,0))    
        lista_sprites.draw(pantalla)
        pantalla.blit(fondo_ranking,(900,0))
        pantalla.blit(texto_score,(1010,10))

        funcionesGalaxy.mostrar_score(pantalla, str(score), 50, 1060, 50)
        funcionesGalaxy.dibujar_barra_salud(pantalla,5,5,nave.salud)
                
        pygame.display.flip()
        fps.tick(60)
         

    funcionesGalaxy.agregar_dato_a_bd("baseDatosGalaxy.db",nombre,score)     
    pygame.quit()
    
def ranking_final():
    pygame.init()
    pygame.display.set_caption("Galaxy premium")
    imagen_fondo_ranking = pygame.image.load("Imagenes juego/FONDOESPACIO.jpg")
    pygame.mixer.music.load("Sonidos juego/musicaMenu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops = -1)

    dimension = (900,800)
    pantalla = pygame.display.set_mode(dimension)

    lista_tupla_datos_juego = funcionesGalaxy.obtener_dato_de_bd("baseDatosGalaxy.db")
    pantalla.blit(imagen_fondo_ranking, [0,0])
    espacio_posicion_ranking_jugador = 0
    eje_y_jugador_posicion = 200

    for elemento in lista_tupla_datos_juego:
        nombre_jugador = elemento[0]
        score_jugador = elemento[1]
        if type(nombre_jugador) == type(None):
            nombre_jugador = "" 
        fuente_texto_score = pygame.font.SysFont("gamer",50)
        texto_score = fuente_texto_score.render(score_jugador, True, ROJO)
        
        fuente_texto_nombre = pygame.font.SysFont("gamer", 50)
        texto_nombre = fuente_texto_nombre.render(nombre_jugador+":", True, ROJO)
        
        pantalla.blit(texto_score, [550, eje_y_jugador_posicion + espacio_posicion_ranking_jugador])
        pantalla.blit(texto_nombre, [200, eje_y_jugador_posicion + espacio_posicion_ranking_jugador])
        espacio_posicion_ranking_jugador += 30

    correr_juego = True

    while correr_juego:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr_juego = False
             
        pygame.display.flip()
    pygame.quit()

nombre = menu()
juego(nombre)
ranking_final()
     