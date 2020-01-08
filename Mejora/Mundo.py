import Modelo as m 
import Camera as c 
import Light as l 
import numpy as np 

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Mundo:
    """Clase para representar Mundo"""

    def __init__ (self, modelo_dict):
        self.width, self.height, self.angulo, self.window = 800, 800, 0, 0
        self.aspect = self.width/self.height
        # Número de vistas diferentes
        self.numCamaras = 3
        
        # Factor para el tamaño del modelo
        self.escalaGeneral = 0.025

        # Rotacion de los modelos
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
			"FORMA_4":12,
			"CAMARA_1":13,
			"CAMARA_2":14,
			"CAMARA_3":15,
			"CAMARA_4":16,
            "MATERIAL_1":17,
            "MATERIAL_2":18,
            "MATERIAL_3":19
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

        self.act_mat = 0

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

        self.modelo = m.Modelo(self.materials[0], 2)

    def getIFondo(self):
        return self.iFondo

    def getIDibujo(self):
        return self.iDibujo

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width
    
    def display(self):
        glClearDepth(1.0)
        glClearColor(self.colores[self.getIFondo()][0], self.colores[self.getIFondo()][1], self.colores[self.getIFondo()][2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
		
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()	
		
        self.camaras[self.act_cam].startCam(self.zoom)

        self.modelo.changeMaterial(self.materials[self.act_mat])

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(self.alpha, 1.0, 0.0, 0.0)
        glRotatef(self.beta, 0.0, 1.0, 0.0)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_DEPTH_TEST)
		# Establecemos el color del Modelo.
        glColor3f(self.colores[self.getIDibujo()][0], self.colores[self.getIDibujo()][1], self.colores[self.getIDibujo()][2])

		# Establecemos la luz
        for light in self.lights:
            light.startLight()
		
        glEnable(GL_LIGHTING)
        for light in self.lights:
            self.checkLight(light)
	
		# Pintamos el modelo
        self.modelo.Draw_Model(self.escalaGeneral, self.zoom, self.iForma)
			
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
            print (self.zoom)
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
        elif (key == chr(109).encode()):
            self.materials[3].randomMaterial()
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
        elif option == self.opcionesMenu["MATERIAL_1"]:
            self.act_mat = 0
        elif option == self.opcionesMenu["MATERIAL_2"]:
            self.act_mat = 1
        elif option == self.opcionesMenu["MATERIAL_3"]:
            self.act_mat = 2
        elif option == self.opcionesMenu["MATERIAL_4"]:
            self.act_mat = 3
        

        glutPostRedisplay()
        return option

    def loadModel(self, nombre):
        _, vertices, faces = self.modelo.load(nombre)
        self.modelo.numCaras = len(faces)
        self.modelo.numVertices = len(vertices)
        self.modelo.ListaCaras = faces
        self.modelo.ListaPuntos3D = vertices