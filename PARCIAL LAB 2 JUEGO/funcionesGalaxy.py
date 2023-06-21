import pygame
import sqlite3
ROJO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)

def mostrar_score(pantalla, mensaje, tamaño, x, y):
        fuente = pygame.font.SysFont("gamer", tamaño)
        mensaje_superficie = fuente.render(mensaje, True, ROJO)
        mensaje_rect = mensaje_superficie.get_rect()
        mensaje_rect.midtop = (x, y)
        pantalla.blit(mensaje_superficie, mensaje_rect)

def dibujar_barra_salud(pantalla, x, y, salud):
        largo_barra = 100
        altura_barra = 20
        llenar_barra = (salud / 100) * largo_barra
        borde_barra = pygame.Rect(x, y, largo_barra, altura_barra)
        llenar_barra = pygame.Rect(x, y, llenar_barra, altura_barra)
        pygame.draw.rect(pantalla, VERDE, llenar_barra)
        pygame.draw.rect(pantalla, AZUL, borde_barra,2) 

def crear_base_datos(path):
    with sqlite3.connect(path) as conexion:
        try:
            sentencia = ''' create table jugadores
                            (
                            id integer primary key autoincrement,
                            nombre text,
                            score integer
                            )
                        '''
            conexion.execute(sentencia)
            print("Se creo la tabla jugadores")
        except sqlite3.OperationalError:
            print("La tabla jugadores ya existe")

def agregar_dato_a_bd(path,nombre,score):
    with sqlite3.connect(path) as conexion:
        try:
            conexion.execute("insert into jugadores(nombre,score) values (?,?)", (nombre, score))
            conexion.commit()
        except:
            print("Error")

def obtener_dato_de_bd(path):
    with sqlite3.connect(path) as conexion:
        datos = conexion.execute("SELECT * FROM jugadores order by score desc")
        lista_datos = []
        for fila in datos:
            nombre = fila[1]          
            score = str(fila[2])         
            lista_datos.append((nombre,score))
        return lista_datos
#obtener_dato_de_bd("baseDatosGalaxy.db")