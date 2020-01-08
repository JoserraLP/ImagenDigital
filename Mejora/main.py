import Mundo as m 
import sys 
import json_loader as jl 
import numpy as np 

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


# Funcion que crea las distintas opciones que se pueden activar en los menus.
def creacionMenu():
    menuFondo, menuDibujo, menuForma, menuCamara, menuPrincipal = 0,0,0,0,0

    menuFondo = glutCreateMenu(mundo.onMenu)
    glutAddMenuEntry("Negro", mundo.opcionesMenu['FONDO_1'])
    glutAddMenuEntry("Verde oscuro", mundo.opcionesMenu['FONDO_2'])
    glutAddMenuEntry("Azul oscuro", mundo.opcionesMenu['FONDO_3'])

    menuDibujo = glutCreateMenu(mundo.onMenu)
    glutAddMenuEntry("Blanco", mundo.opcionesMenu['DIBUJO_1'])
    glutAddMenuEntry("Verde claro", mundo.opcionesMenu['DIBUJO_2'])
    glutAddMenuEntry("Azul claro", mundo.opcionesMenu['DIBUJO_3'])
    
    menuForma = glutCreateMenu(mundo.onMenu)
    glutAddMenuEntry("Wired", mundo.opcionesMenu['FORMA_1'])
    glutAddMenuEntry("Solid", mundo.opcionesMenu['FORMA_2'])
    glutAddMenuEntry("Flat", mundo.opcionesMenu['FORMA_3'])
    glutAddMenuEntry("Smooth", mundo.opcionesMenu['FORMA_4'])

    menuCamara = glutCreateMenu(mundo.onMenu)
    glutAddMenuEntry("Camara 1", mundo.opcionesMenu['CAMARA_1'])
    glutAddMenuEntry("Camara 2", mundo.opcionesMenu['CAMARA_2'])
    glutAddMenuEntry("Camara 3", mundo.opcionesMenu['CAMARA_3'])
    glutAddMenuEntry("Camara aleatoria", mundo.opcionesMenu['CAMARA_4'])

    menuMaterial = glutCreateMenu(mundo.onMenu)
    glutAddMenuEntry("Material 1", mundo.opcionesMenu['MATERIAL_1'])
    glutAddMenuEntry("Material 2", mundo.opcionesMenu['MATERIAL_2'])
    glutAddMenuEntry("Material 3", mundo.opcionesMenu['MATERIAL_3'])
    
    menuPrincipal = glutCreateMenu(mundo.onMenu)

    glutAddSubMenu("Color de fondo", menuFondo)
    glutAddSubMenu("Color del dibujo", menuDibujo)
    glutAddSubMenu("Forma del dibujo", menuForma)
    glutAddSubMenu("Camaras", menuCamara)
    glutAddSubMenu("Materiales", menuMaterial)
    
    # Carga el menú con el boton derecho.
    glutAttachMenu(GLUT_RIGHT_BUTTON)


def InitGL():
    # Activamos los bufferes
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_RGBA | GLUT_DEPTH | GLUT_ALPHA)	
    # Establece el tamaño de la ventana.
    glutInitWindowSize(mundo.getWidth(), mundo.getHeight())	
    # Establece la posicion inicial (esquina superior izquierda de la ventana).
    glutInitWindowPosition(100, 100)	
    glutCreateWindow(b"Mundo")
    glShadeModel(GL_SMOOTH) 
    glEnable(GL_LIGHTING) 
    glEnable(GL_NORMALIZE) 
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)

if __name__ == "__main__":
    modelo_dict = jl.JsonLoader.load(sys.argv[1])
	
    if (len(modelo_dict) < 0):
        exit(status=1, message="El fichero "+sys.argv[1]+" no ha sido cargado correctamente")

    mundo = m.Mundo(modelo_dict)

    mundo.loadModel(sys.argv[2])
    glutInit(sys.argv)
	
    # Declaraciones Globales
    InitGL()
	# Gestion de los botones del raton
    glutMouseFunc(mundo.onMouse)
	# Gestion de los movimientos del raton	
    glutMotionFunc(mundo.onMotion)	
	# Dibujo e Idle
    glutDisplayFunc(mundo.display)
    glutIdleFunc(mundo.display)
	# Menús
    creacionMenu()
	# Pulsaciones del teclado
    glutKeyboardFunc(mundo.keyPressed)	
		
	#Repeat.
    glutMainLoop()