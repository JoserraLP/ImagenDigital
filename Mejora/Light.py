import random

from OpenGL.GL import *

class Light:

	dict_lights = {
		0: GL_LIGHT0,
		1: GL_LIGHT1,
		2: GL_LIGHT2,
		3: GL_LIGHT3,
		4: GL_LIGHT4,
		5: GL_LIGHT5,
		6: GL_LIGHT6
	}

	def __init__(self, luzdifusa, luzambiente, luzespecular, posicion0, num = 0):
		self.luzdifusa = luzdifusa
		self.luzambiente = luzambiente
		self.luzspecular = luzespecular
		self.posicion0 = posicion0
		self.activa = True
		self.num = num

	def randomLight(self):
		self.luzdifusa = [1.0, 1.0, 1.0, 1.0]
		self.luzambiente = [0.50, 0.50, 0.50, 1.0]
		self.luzspecular = [0.20, 0.20, 0.20, 1.0]
		self.posicion0 = [random.uniform(0.0, 10.0), random.uniform(0.0, 10.0), random.uniform(0.0, 10.0), random.uniform(0.0, 10.0)]
		self.activa = True

	def startLight(self):
		glLightfv(self.dict_lights[self.num], GL_DIFFUSE, self.luzdifusa)
		glLightfv(self.dict_lights[self.num], GL_AMBIENT, self.luzambiente)
		glLightfv(self.dict_lights[self.num], GL_SPECULAR, self.luzspecular)
		glLightfv(self.dict_lights[self.num], GL_POSITION, self.posicion0)

	def disableLight(self):
		glDisable(self.dict_lights[self.num])

	def enableLight(self):
		glEnable(self.dict_lights[self.num])

	def setNum (self, num):
		self.num = num

	def changeStatus(self):
		if (self.activa is True):
			self.activa = False
		else:
			self.activa = True