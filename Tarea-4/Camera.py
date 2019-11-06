import random 

from OpenGL.GLU import *
from OpenGL.GL import *

class Camera:
    
    def __init__(self, axisX = 0.0, axisY = 0.0, axisZ = 0.0, centerX = 0.0, centerY = 0.0, centerZ = 0.0, upX = 0.0, upY = 0.0, upZ = 0.0, aspect = 1.0):
        self.axisX = axisX
        self.axisY = axisY
        self.axisZ = axisZ
        self.centerX = centerX
        self.centerY = centerY
        self.centerZ = centerZ
        self.upX = upX
        self.upY = upY
        self.upZ = upZ
        self.fovy = 30.0
        self.aspect = aspect
        self.zNear = 1.0
        self.zFar = 10.0

    def randomCam(self):
        self.axisX = random.uniform(0.0, 5.0)
        self.axisY = random.uniform(0.0, 5.0)
        self.axisZ = random.uniform(0.0, 5.0)
        self.centerX = random.uniform(0.0, 0.0)
        self.centerY = random.uniform(0.0, 0.0)
        self.centerZ = random.uniform(0.0, 0.0)
        self.upX = random.uniform(0.0, 1.0)
        self.upY = random.uniform(0.0, 1.0)
        self.upZ = random.uniform(0.0, 1.0)

    def selectPerspective(self, fovy, aspect, zNear, zFar):
        self.fovy = fovy
        self.aspect = aspect
        self.zNear = zNear
        self.zFar = zFar

    def randomPerspective(self):
        self.fovy = random.uniform(20.0, 50.0)
        self.zNear = random.uniform(0.0, 5.0)
        self.zFar = random.uniform(5.0, 15.0)


    def startCam(self):
        gluPerspective(self.fovy, self.aspect, self.zNear, self.zFar)
        gluLookAt(self.axisX, self.axisY, self.axisZ, self.centerX, self.centerY, self.centerZ, self.upX, self.upY, self.upZ)