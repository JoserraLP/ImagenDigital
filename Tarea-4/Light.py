import random

from OpenGL.GL import *

class Light:

	def __init__(self, luzdifusa, luzambiente, luzespecular, posicion0):
		self.luzdifusa = luzdifusa
		self.luzambiente = luzambiente
		self.luzspecular = luzespecular
		self.posicion0 = posicion0

	def randomLight(self):
		self.luzdifusa = [1.0, 1.0, 1.0, 1.0]
		self.luzambiente = [0.50, 0.50, 0.50, 1.0]
		self.luzspecular = [0.20, 0.20, 0.20, 1.0]
		self.posicion0 = [random.uniform(0.0, 10.0), random.uniform(0.0, 10.0), random.uniform(0.0, 10.0), random.uniform(0.0, 10.0)]

	def startLight(self):
		glLightfv(GL_LIGHT0, GL_DIFFUSE, self.luzdifusa)
		glLightfv(GL_LIGHT0, GL_AMBIENT, self.luzambiente)
		glLightfv(GL_LIGHT0, GL_SPECULAR, self.luzspecular)
		glLightfv(GL_LIGHT0, GL_POSITION, self.posicion0)

