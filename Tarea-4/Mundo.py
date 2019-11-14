import Modelo as m
import Camera as c
import Light as l

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Mundo:
	"""Clase para representar Mundo"""

	def __init__ (self, modelo_dict):
		self.width, self.height, self.angulo, self.window = 800, 800, 0, 0
		self.aspect = self.width/self.height

		# Número de vistas diferentes.
		self.numCamaras = 3

		# Factor para el tamaño del modelo.
		self.escalaGeneral = 0.011

		# Rotacion de los modelos.
		self.alpha, self.beta = 0, 0

		# Variables para la gestion del ratón.
		self.xold, self.yold = 0, 0
		self.zoom = 1.0

		self.iDibujo, self.iFondo = 3, 0
		self.iForma = "wired"

		# Tamaño de los ejes y del alejamiento de Z.
		self.tamanio, self.z0 = 0, 0

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
			"FORMA_4":12,
			"CAMARA_1":13,
			"CAMARA_2":14,
			"CAMARA_3":15,
			"CAMARA_4":16
		}

		# Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
		# Se encuentra distribuido en RGB
		self.colores = [(0.00, 0.00, 0.00),   # 0 - negro
			(0.06, 0.25, 0.13), # 1 - verde oscuro
			(0.10, 0.07, 0.33), # 2 - azul oscuro
			(1.00, 1.00, 1.00), # 3 - blanco
			(0.12, 0.50, 0.26), # 4 - verde claro
			(0.20, 0.14, 0.66)] # 5 - azul claro 

		# Variables actuales

		self.act_cam = 0

		# Cargamos todos los datos y los almacenamos en distintos arrays

		self.lights = [l.Light(light['luzdifusa'], light['luzambiente'], light['luzspecular'], light['posicion']) for light in modelo_dict['focos']] 

		# Almacenar el número de la luz
		for i in range(len(self.lights)):
			self.lights[i].setNum(i)

		self.camaras = [c.Camera(cam['ejex'], cam['ejey'], cam['ejez'], cam['centrox'], cam['centroy'], cam['centroz'], 
		cam['upx'], cam['upy'], cam['upz']) for cam in modelo_dict['camaras']]
		
		# Añadimos la opción de una camara aleatoria
		self.camaras.append(c.Camera(10,10,10,0,0,0,1,0,1))
		
		self.camaras[0].startCam(self.zoom)

		self.materials = [[material['luzambiente'], material['luzdifusa'], material['luzspecular'], material['brillo']] for material in modelo_dict['materiales']]

		self.astros = []
		i=0
		for model in modelo_dict["planetas"]:
			self.astros.append(m.Modelo(self.materials[i], model['radio'], model['wRotAstro'], model['wRotProp'], model['tamanio'], model['nombre'], model['l']))
			i+=1

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
		modelo.Draw_Model(escala,self.iForma)

	def display(self):
		glClearDepth(1.0)
		glClearColor(self.colores[self.getIFondo()][0], self.colores[self.getIFondo()][1], self.colores[self.getIFondo()][2], 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		self.camaras[self.act_cam].startCam(self.zoom)

		glRotatef(self.alpha, 1.0, 0.0, 0.0)
		glRotatef(self.beta, 0.0, 1.0, 0.0)

		# Establecemos el color del Modelo.
		glColor3f(self.colores[self.getIDibujo()][0], self.colores[self.getIDibujo()][1], self.colores[self.getIDibujo()][2])

		# Establecemos la luz
		for light in self.lights:
			light.startLight()
		
		glEnable(GL_LIGHTING)
		for light in self.lights:
			self.checkLight(light)

		planetas = [planeta for planeta in self.astros if planeta.l == 'n']
		for planeta in planetas:
			print(planeta.nombre)
		print("...................")
		lunas = [luna for luna in self.astros if luna.l == 'l']
		for luna in lunas:
			print(luna.nombre)

		for model in self.astros:
			glPushMatrix()
			glTranslatef(model.radio*self.escalaGeneral, 0.0, 0.0)
			# Pintamos el modelo
			self.drawModel(model, self.escalaGeneral)
			glPopMatrix()

		# Radio de la luna tiene que se relativo al planeta

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

	def checkLight(self, light):
		if(light.activa is True):
			light.enableLight()
		else:
			light.disableLight()

	def keyPressed (self, key, x, y):
		if (key == chr(27).encode()): # Tecla ESC
			glutDestroyWindow(self.window)
			exit()
		elif (key == chr(32).encode()): # Tecla espacio
			self.camaras[3].randomCam()
		elif (key == chr(49).encode()): # Tecla 1
			self.lights[0].changeStatus()
			self.checkLight(self.lights[0])
		elif (key == chr(50).encode()): # Tecla 2
			self.lights[1].changeStatus()
			self.checkLight(self.lights[1])
		elif (key == chr(51).encode()): # Tecla 3
			self.lights[2].changeStatus()
			self.checkLight(self.lights[2])
		elif (key == chr(52).encode()): # Tecla 4
			self.lights[3].changeStatus()
			self.checkLight(self.lights[3])
		elif (key == chr(53).encode()): # Tecla 5
			self.lights[4].changeStatus()
			self.checkLight(self.lights[4])
		elif (key == chr(54).encode()): # Tecla 6
			self.lights[5].changeStatus()
			self.checkLight(self.lights[5])
		elif (key == chr(55).encode()): # Tecla 7
			self.lights[6].changeStatus()
			self.checkLight(self.lights[6])

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
		elif option == self.opcionesMenu["CAMARA_1"]:
			self.act_cam = 0
		elif option == self.opcionesMenu["CAMARA_2"]:
			self.act_cam = 1
		elif option == self.opcionesMenu["CAMARA_3"]:
			self.act_cam = 2
		elif option == self.opcionesMenu["CAMARA_4"]:
			self.act_cam = 3

		glutPostRedisplay()
		return option

	def loadModel (self, nombre):
		for model in self.astros:
			_, vertices, faces = model.load(nombre)
			model.numCaras = len(faces)
			model.numVertices = len(vertices)
			model.ListaCaras = faces
			model.ListaPuntos3D = vertices
		

