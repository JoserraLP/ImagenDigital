import Modelo as m
import Camera as c

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Mundo:
	"""Clase para representar Mundo"""

	# Número de vistas diferentes.
	numCamaras = 3

	# Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
	# Se encuentra distribuido en RGB
	colores = [(0.00, 0.00, 0.00),   # 0 - negro
		(0.06, 0.25, 0.13), # 1 - verde oscuro
		(0.10, 0.07, 0.33), # 2 - azul oscuro
		(1.00, 1.00, 1.00), # 3 - blanco
		(0.12, 0.50, 0.26), # 4 - verde claro
		(0.20, 0.14, 0.66)] # 5 - azul claro 

	width, height, window = 0, 0, 0 
	aspect, angulo = 0.0, 0.0
	sol = m.Modelo(0,0)
	
	# Tamaño de los ejes y del alejamiento de Z.
	tamanio, z0 = 0, 0

	# Factor para el tamaño del modelo.
	escalaGeneral = 0.0

	# Rotacion de los modelos.
	alpha, beta = 0.0, 0.0

	# Variables para la gestion del ratón.
	xold, yold = 0, 0
	zoom = 0.0


	# Vistas del Sistema Planetario.
	iFondo, iDibujo = 0, 0
	iForma = "wired"

	def __init__ (self):
		self.width, self.height, self.angulo, self.windows = 800, 800, 0, 0
		self.aspect = self.width/self.height

		# Factor para el tamaño del modelo.
		self.escalaGeneral = 0.005

		# Rotacion de los modelos.
		self.alpha, self.beta = 0, 0

		# Variables para la gestion del ratón.
		self.xold, self.yold = 0, 0
		self.zoom = 1.0

		self.iDibujo, self.iFondo = 3, 0
		self.iForma = "wired"

		# Distintas opciones del menu.
		self.opcionesMenu = {
			"FONDO_1":1,
			"FONDO_2":2,
			"FONDO_3":3,
			"FONDO_4":4,
			"DIBUJO_1":5,
			"DIBUJO_2":6,
			"DIBUJO_3":7,
			"DIBUJO_4":8,
			"FORMA_1":9,
			"FORMA_2":10,
			"FORMA_3":11,
			"FORMA_4":12
		}

		# Un dato de ejemplo
		self.camara = c.Camera(2.0, 2.0, 5.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
		self.camara.startCam()

	def getIFondo(self):
		return self.iFondo

	def getIDibujo(self):
		return self.iDibujo

	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width

	def drawAxis(self):
	
		# Inicializamos
		glDisable(GL_LIGHTING)
		glBegin(GL_LINES)
		glClearColor(0.0, 0.0, 0.0, 0.0)

		# Eje X Rojo
		glColor3f(1.0, 0.0, 0.0)
		glVertex3f(0.0, 0.0, 0.0)
		glVertex3f(self.tamanio, 0.0, 0.0)

		# Eje Y Verde
		glColor3f(0.0, 1.0, 0.0)
		glVertex3f(0.0, 0.0, 0.0)
		glVertex3f(0.0, self.tamanio, 0.0)

		# Eje Z Azul
		glColor3f(0.0, 0.0, 1.0)
		glVertex3f(0.0, 0.0, 0.0)
		glVertex3f(0.0, 0.0, self.tamanio)

		glClearColor(0.0, 0.0, 0.0, 0.0)

		glEnd()
		glEnable(GL_LIGHTING)

	def drawModel(self, modelo, escala):
		modelo.Draw_Model(escala,self.zoom,self.iForma)

	def display(self):
		glClearDepth(1.0)
		glClearColor(self.colores[self.getIFondo()][0], self.colores[self.getIFondo()][1], self.colores[self.getIFondo()][2], 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		self.camara.startCam()

		glRotatef(self.alpha, 1.0, 0.0, 0.0)
		glRotatef(self.beta, 0.0, 1.0, 0.0)

		# Establecemos el color del Modelo.
		glColor3f(self.colores[self.getIDibujo()][0], self.colores[self.getIDibujo()][1], self.colores[self.getIDibujo()][2])

		# Pasar a una nueva clase esto de la luz

		luzdifusa, luzambiente, luzspecular, posicion0 = [], [], [], []

		self.sol.setVector(luzdifusa, 1.0, 1.0, 1.0, 1.0)
		self.sol.setVector(luzambiente, 0.50, 0.50, 0.50, 1.0)
		self.sol.setVector(luzspecular, 0.20, 0.20, 0.20, 1.0)
		self.sol.setVector(posicion0, 5.0, 5.0, 6.0, 0.0)
		glLightfv(GL_LIGHT0, GL_DIFFUSE, luzdifusa)
		glLightfv(GL_LIGHT0, GL_AMBIENT, luzambiente)
		glLightfv(GL_LIGHT0, GL_SPECULAR, luzspecular)
		glLightfv(GL_LIGHT0, GL_POSITION, posicion0)

		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)

		# Pintamos el modelo.
		self.drawModel(self.sol, self.escalaGeneral)

		glFlush() 
		glutSwapBuffers()

	# Funcion para gestionar los movimientos del raton.
	def onMouse(self, button, state, x, y):
		if (button == 3) or (button == 4):
			if (state == GLUT_UP):
				pass
			if(button==3):
				self.zoom -= 0.1
				# print("Zoom negativo..." + self.zoom)
			else:
				self.zoom += 0.1
				# print("Zoom positivo..." + self.zoom)
		else:
			# Actualizamos los valores de x, y.
			self.xold = x
			self.yold = y 
	
	# Funcion que actualiza la posicion de los modelos en la pantalla segun los movimientos del raton.
	def onMotion(self, x, y):
		self.alpha = (self.alpha + (y - self.yold))
		self.beta = (self.beta + (x - self.xold))
		self.xold = x
		self.yold = y
		glutPostRedisplay()

	def keyPressed (self, key, x, y):
		if (key == chr(27).encode()): # Tecla ESC
			glutDestroyWindow(self.window)
		elif (key == chr(32).encode()):
			self.camara.randomCam()
	
	def onMenu (self, option):
		if option == self.opcionesMenu["FONDO_1"]:
			self.iFondo = 0
		elif option == self.opcionesMenu["FONDO_2"]:
			self.iFondo = 1
		elif option == self.opcionesMenu["FONDO_3"]:
			self.iFondo = 2
		elif option == self.opcionesMenu["DIBUJO_1"]:
			self.iDibujo = 3
		elif option == self.opcionesMenu["DIBUJO_2"]:
			self.iDibujo = 4
		elif option == self.opcionesMenu["DIBUJO_3"]:
			self.iDibujo = 5
		elif option == self.opcionesMenu["FORMA_1"]:
			self.iForma = "wired"
		elif option == self.opcionesMenu["FORMA_2"]:
			self.iForma = "solid"
		elif option == self.opcionesMenu["FORMA_3"]:
			self.iForma = "flat"
		elif option == self.opcionesMenu["FORMA_4"]:
	  		self.iForma = "smooth"
		glutPostRedisplay()
		return option

	def loadModel (self, nombre):
		_, vertices, faces = self.sol.load(nombre)
		self.sol.numCaras = len(faces)
		self.sol.numVertices = len(vertices)
		self.sol.ListaCaras = faces
		self.sol.ListaPuntos3D = vertices
		

