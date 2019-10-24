#include "Mundo.h"
import OpenGL.GL
import OpenGL.GLUT
import OpenGL.GLU
import Mundo as m
import sys

class Main:

	mundo = m.Mundo()

	def display(self):
		self.mundo.display()

	def onMenu(self, opcion):
		self.mundo.onMenu(opcion)

	# Funcion que crea las distintas opciones que se pueden activar en los menus.
	def creacionMenu(self):
		menuFondo, menuDibujo, menuPrincipal, menuForma

		menuFondo = GL.glutCreateMenu(onMenu)
		GL.glutAddMenuEntry("Negro", FONDO_1)
		GL.glutAddMenuEntry("Verde oscuro", FONDO_2)
		GL.glutAddMenuEntry("Azul oscuro", FONDO_3)

		menuDibujo = glutCreateMenu(onMenu)
		GL.glutAddMenuEntry("Blanco", DIBUJO_1)
		GL.glutAddMenuEntry("Verde claro", DIBUJO_2)
		GL.glutAddMenuEntry("Azul claro", DIBUJO_3)
		menuPrincipal = GL.glutCreateMenu(onMenu)
		GL.glutAddSubMenu("Color de fondo", menuFondo)
		GL.glutAddSubMenu("Color del dibujo", menuDibujo)
		# Carga el menú con el boton derecho.
		GL.glutAttachMenu(GL.GLUT_RIGHT_BUTTON)

	def onMotion(self, x, y):
		self.mundo.onMotion(x,y)

	def onMouse(self, button, state, x, y):
		self.mundo.onMouse(button,state,x,y)

	def keyPressed(self, key, x, y):
		self.mundo.keyPressed(key,x,y)

	def InitGL(self):

		# Activamos los bufferes
		GL.glutInitDisplayMode(GL.GLUT_DOUBLE | GL.GLUT_RGB | GL.GLUT_RGBA | GL.GLUT_DEPTH | GL.GLUT_ALPHA)	
		# Establece el tamaño de la ventana.
		GL.glutInitWindowSize(self.mundo.getWidth(), self.mundo.getHeight())	
		#	Establece la posicion inicial (esquina superior izquierda de la ventana).
		GL.glutInitWindowPosition(100, 100)	
		GL.glutCreateWindow("Mundo")
		GL.glShadeModel(GL.GL_SMOOTH) 
		GL.glEnable(GL.GL_LIGHTING) 
		GL.glEnable(GL.GL_NORMALIZE) 
		GL.glEnable(GL.GL_CULL_FACE)
		GL.glEnable(GL.GL_DEPTH_TEST)
		GL.glDepthMask(GL.GL_TRUE)
		GL.glDepthFunc(GL.GL_LESS)


if __name__ == "__main__":
	main = Main()

	mundo = m.Mundo()
	
	mundo.loadModel(sys.argv[1])

	GL.glutInit(argc, argv)
	
	# Declaraciones Globales
	main.InitGL()

	# Gestion de los botones del raton
	GL.glutMouseFunc(main.onMouse)
	# Gestion de los movimientos del raton	
	GL.glutMotionFunc(main.onMotion)	
	# Dibujo e Idle
	GL.glutDisplayFunc(main.display)
	GL.glutIdleFunc(main.display)
	# Menús
	main.creacionMenu()
	# Pulsaciones del teclado
	GL.glutKeyboardFunc(main.keyPressed)	
		
	#Repeat.
	GL.glutMainLoop()	
