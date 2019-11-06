import random

from OpenGL.GL import *

class Material:

    def __init__(self, mat_ambient = None, mat_diffuse = None, mat_specular = None, brillo = 1.0):
        self.mat_ambient = mat_ambient
        self.mat_diffuse = mat_diffuse
        self.mat_specular = mat_specular
        self.brillo = brillo

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
