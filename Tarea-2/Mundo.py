import Modelo as m
import OpenGL.GL
import OpenGL.GLUT
import OpenGL.GLU

class Mundo:
	"""Clase para representar Mundo"""

	# Distintas opciones del menu.
	opcionesMenu = {
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

	tipoVista = {'wired'}

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

	def __init__ (self):
		width, height, angulo, windows = 800, 800, 0, 0
		aspect = width/height

		# Factor para el tamaño del modelo.
		escalaGeneral = 0.005

		# Rotacion de los modelos.
		alpha, beta = 0, 0

		# Variables para la gestion del ratón.
		xold, yold = 0, 0
		zoom = 1.0

		iDibujo, iFondo = 4, 0



	def drawAxis(self):
	
		# Inicializamos
		GL.glDisable(GL.GL_LIGHTING)
		GL.glBegin(GL.GL_LINES)
		GL.glClearColor(0.0, 0.0, 0.0, 0.0)

		# Eje X Rojo
		GL.glColor3f(1.0, 0.0, 0.0)
		GL.glVertex3f(0.0, 0.0, 0.0)
		GL.glVertex3f(self.tamanio, 0.0, 0.0)

		# Eje Y Verde
		GL.glColor3f(0.0, 1.0, 0.0)
		GL.glVertex3f(0.0, 0.0, 0.0)
		GL.glVertex3f(0.0, self.tamanio, 0.0)

		# Eje Z Azul
		GL.glColor3f(0.0, 0.0, 1.0)
		GL.glVertex3f(0.0, 0.0, 0.0)
		GL.glVertex3f(0.0, 0.0, self.tamanio)

		GL.glClearColor(0.0, 0.0, 0.0, 0.0)

		GL.glEnd()
		GL.glEnable(GL.GL_LIGHTING)

	def drawModel(self, modelo, escala):
		GL.glDisable(GL.GL_LIGHTING)
		modelo.Draw_Model(escala,self.zoom,self.tipoVista)
		GL.glEnable(GL.GL_LIGHTING)

	def display(self):
		GL.glClearDepth(1.0)
		GL.glClearColor(self.colores[self.getIFondo()][0], self.colores[self.getIFondo()][1], self.colores[self.getIFondo()][2], 1.0)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

		GL.glMatrixMode(GL.GL_PROJECTION)
		GL.glLoadIdentity()

		GL.glMatrixMode(GL.GL_MODELVIEW)
		GL.glLoadIdentity()

		GL.glRotatef(self.alpha, 1.0, 0.0, 0.0)
		GL.glRotatef(self.beta, 0.0, 1.0, 0.0)

		# Establecemos el color del Modelo.
		GL.glColor3f(self.colores[self.getIDibujo()][0], self.colores[self.getIDibujo()][1], self.colores[self.getIDibujo()][2])
		
		# Pintamos el modelo.
		drawModel(self.Sol, self.escalaGeneral)

		GL.glFlush() 
		GL.glutSwapBuffers()



	# Funcion para gestionar los movimientos del raton.
	def onMouse(self, button, state, x, y):
		if (button == 3) or (button == 4):
			if (state == GL.GLUT_UP):
				pass
			if(button==3):
				self.zoom -= 0.1
				print("Zoom negativo..." + self.zoom)
			else:
				self.zoom += 0.1
				print("Zoom positivo..." + self.zoom)
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
		GL.glutPostRedisplay()

	def keyPressed (self, key, x, y):
		if (key == 27): # Tecla ESC
			GL.glutDestroyWindow(window)
		elif (key == 32): # Tecla espacio
			pass
		elif (key >= 48 and key <= 55):
			pass

	
	def onMenu (self, option):
		if option == self.opcionesMenu["FONDO_1"]:
			iFondo = 0
		elif option == self.opcionesMenu["FONDO_2"]:
			iFondo = 1
		elif option == self.opcionesMenu["FONDO_3"]:
			iFondo = 2
		elif option == self.opcionesMenu["DIBUJO_1"]:
			iFondo = 3
		elif option == self.opcionesMenu["DIBUJO_2"]:
			iFondo = 4
		elif option == self.opcionesMenu["DIBUJO_3"]:
			iFondo = 5
		GL.glutPostRedisplay()

	def loadModel (self, nombre):
		self.sol.load(nombre)

