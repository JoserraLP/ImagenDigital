import random

from OpenGL.GL import *

class Material:

    def __init__(self, material):
        self.mat_ambient, self.mat_diffuse, self.mat_specular, self.brillo = material

    def randomMaterial(self):
        self.mat_ambient = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 0.0]
        self.mat_diffuse = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 0.0]
        self.mat_specular = [random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 0.0]
        self.brillo = random.uniform(0.0, 1.0)

    def startMaterial(self):
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.mat_specular)
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.mat_diffuse)
        glMaterialf(GL_FRONT, GL_SHININESS, self.brillo)
