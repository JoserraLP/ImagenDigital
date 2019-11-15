import Mundo as m
import sys
import json_loader as jl

import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Main:
	def __init__(self):
		self.mundo = None

	def display(self):
		self.mundo.display()

	def onMenu(self, opcion):
		self.mundo.onMenu(opcion)

	def onMotion(self, x, y):
		self.mundo.onMotion(x,y)

	

	def onMouse(self, button, state, x, y):
		self.mundo.onMouse(button,state,x,y)

	# Funcion que crea las distintas opciones que se pueden activar en los menus.
	def creacionMenu(self):
		menuFondo, menuDibujo, menuForma, menuCamara, menuPrincipal = 0,0,0,0,0

		menuFondo = glutCreateMenu(self.mundo.onMenu)
		glutAddMenuEntry("Negro", self.mundo.opcionesMenu['FONDO_1'])
		glutAddMenuEntry("Verde oscuro", self.mundo.opcionesMenu['FONDO_2'])
		glutAddMenuEntry("Azul oscuro", self.mundo.opcionesMenu['FONDO_3'])

		menuDibujo = glutCreateMenu(self.mundo.onMenu)
		glutAddMenuEntry("Blanco", self.mundo.opcionesMenu['DIBUJO_1'])
		glutAddMenuEntry("Verde claro", self.mundo.opcionesMenu['DIBUJO_2'])
		glutAddMenuEntry("Azul claro", self.mundo.opcionesMenu['DIBUJO_3'])
		
		menuForma = glutCreateMenu(self.mundo.onMenu)
		glutAddMenuEntry("Wired", self.mundo.opcionesMenu['FORMA_1'])
		glutAddMenuEntry("Solid", self.mundo.opcionesMenu['FORMA_2'])
		glutAddMenuEntry("Flat", self.mundo.opcionesMenu['FORMA_3'])
		glutAddMenuEntry("Smooth", self.mundo.opcionesMenu['FORMA_4'])

		menuCamara = glutCreateMenu(self.mundo.onMenu)
		glutAddMenuEntry("Camara 1", self.mundo.opcionesMenu['CAMARA_1'])
		glutAddMenuEntry("Camara 2", self.mundo.opcionesMenu['CAMARA_2'])
		glutAddMenuEntry("Camara 3", self.mundo.opcionesMenu['CAMARA_3'])
		glutAddMenuEntry("Camara aleatoria", self.mundo.opcionesMenu['CAMARA_4'])
		
		menuPrincipal = glutCreateMenu(self.mundo.onMenu)

		glutAddSubMenu("Color de fondo", menuFondo)
		glutAddSubMenu("Color del dibujo", menuDibujo)
		glutAddSubMenu("Forma del dibujo", menuForma)
		glutAddSubMenu("Camaras", menuCamara)
		
		# Carga el menú con el boton derecho.
		glutAttachMenu(GLUT_RIGHT_BUTTON)

	def keyPressed(self, key, x, y):
		self.mundo.keyPressed(key,x,y)

	def InitGL(self):

		# Activamos los bufferes
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_RGBA | GLUT_DEPTH | GLUT_ALPHA)	
		# Establece el tamaño de la ventana.
		glutInitWindowSize(self.mundo.getWidth(), self.mundo.getHeight())	
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
	main = Main()

	modelo_dict = jl.JsonLoader.load(sys.argv[1])
	
	if (len(modelo_dict) < 0):
		exit(status=1, message="El fichero "+sys.argv[1]+" no ha sido cargado correctamente")

	main.mundo = m.Mundo(modelo_dict)

	main.mundo.loadModel(sys.argv[2])

	glutInit(sys.argv)
	
	# Declaraciones Globales
	main.InitGL()

	# Gestion de los botones del raton
	glutMouseFunc(main.onMouse)
	# Gestion de los movimientos del raton	
	glutMotionFunc(main.onMotion)	
	# Dibujo e Idle
	glutDisplayFunc(main.display)
	glutIdleFunc(main.display)
	# Menús
	main.creacionMenu()
	# Pulsaciones del teclado
	glutKeyboardFunc(main.keyPressed)	
		
	#Repeat.
	glutMainLoop()	
