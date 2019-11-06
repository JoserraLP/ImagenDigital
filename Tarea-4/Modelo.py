
import re
import Material as m

from point_face import Point3D, Face
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Modelo:
    alpha, beta, _numCaras, _numVertices = 0,0,0,0

    """
    # Planetas JSON
    radio, wRotAstro, wRotProp, tamanio = 0.0, 0.0, 0.0, 0.0 
    nombre, l = "", ""
    """

    #Lista de puntos 3D y Lista de caras
    ListaPuntos3D, ListaCaras = [], []

    def __init__(self, nCaras, nVertices):
        self._numCaras = nCaras
        self._numVertices = nVertices
        self.material = m.Material([0.0215, 0.1745, 0.0215, 0.0], [0.07568, 0.61424, 0.07568, 0.0], [0.633, 0.727811, 0.633, 0.0], 0.6)
        
    def setVector(self, vector, v0, v1, v2, v3):
        vector.clear()
        vector.append(v0)
        vector.append(v1)
        vector.append(v2)
        vector.append(v3)

    @property
    def numCaras(self):
        return self._numCaras

    @numCaras.setter
    def numCaras(self, value):
        self._numCaras = value

    @property
    def numVertices(self):
        return self._numVertices

    @numVertices.setter
    def numVertices(self, value):
        self._numVertices = value

    @staticmethod
    def load(path: str):
        """Loads a asc file as a 3D model

        Args:
            path (str): The path where the asc file can be found

        Returns:
            str: Name of the imported model
            list: List of vertices (Point3D)
            list: List of faces (Face)
        """

        vertices, faces = list(), list()
        name = ''

        def regex(types, regex, string):
            return [t(s) for t, s in zip(types, re.search(regex, string).groups())]

        with open(path) as file:
            for line in file:
                line = line.strip()
                if line[:5] == 'Named':
                    name = re.search('"(.*)"', line).groups()[0]
                    line = next(file)
                    _, _numVertices, _, _, _numCaras = regex((str, int, str, str, int), 
                    'Tri-mesh, Vertices:(\s+)(\d+)(\s+)Faces:(\s+)(\d+)', line)

                if line == 'Vertex list:':
                    for n in range(0, _numVertices):
                        line = next(file)

                        _, x = regex((str, float), 'X:(\s*)(-?\d*\.?\d*)', line)
                        _, y = regex((str, float), 'Y:(\s*)(-?\d*\.?\d*)', line)
                        _, z = regex((str, float), 'Z:(\s*)(-?\d*\.?\d*)', line)

                        vertices.append(Point3D(x, y, z))

                if line == 'Face list:':
                    for n in range(0, _numCaras):
                        line = next(file)
                        if line.strip() == '' or 'Page' in line or 'Smoothing:' in line:
                            continue

                        _, a = regex((str, int), 'A:(\s*)(\d+)', line)
                        _, b = regex((str, int), 'B:(\s*)(\d+)', line)
                        _, c = regex((str, int), 'C:(\s*)(\d+)', line)

                        ax = vertices[a].x - vertices[b].x  # X[A] - X[B]
                        ay = vertices[a].y - vertices[b].y  # Y[A] - Y[B]
                        az = vertices[a].z - vertices[b].z  # Z[A] - Z[B]
                        bx = vertices[b].x - vertices[c].x  # X[B] - X[C]
                        by = vertices[b].y - vertices[c].y  # Y[B] - Y[C]
                        bz = vertices[b].z - vertices[c].z  # Z[B] - Z[C]

                        normal = Point3D(
                            (ay * bz) - (az * by),
                            (az * bx) - (ax * bz),
                            (ax * by) - (ay * bx))

                        l = ((normal.x ** 2) + (normal.y ** 2) + (normal.z ** 2)) ** (1 / 2)

                        normal.x /= l
                        normal.y /= l
                        normal.z /= l

                        faces.append(Face(a, b, c, normal))
        return name, vertices, faces

    def Draw_Model(self, scale_from_editor, zoom, iForma):
        # print("Caras: ", self._numCaras)
        smooth = False
        for FaceNumber in range(self._numCaras):
            if (iForma == "solid"):
                glDisable(GL_LIGHTING)
                glBegin(GL_POLYGON)
            elif (iForma == "wired"):
                glDisable(GL_LIGHTING)
                glBegin(GL_LINES)
            elif (iForma == "flat"):
                glShadeModel(GL_FLAT)
                glBegin(GL_POLYGON)
                # Normal
                glNormal3f(self.ListaCaras[FaceNumber].getNormal().getX(), self.ListaCaras[FaceNumber].getNormal().getY(), self.ListaCaras[FaceNumber].getNormal().getZ())
            elif (iForma == "smooth"):
                glShadeModel(GL_SMOOTH)
                glBegin(GL_POLYGON)
                smooth = True
               
            # Normals
            if (smooth):
                glNormal3f(self.ListaPuntos3D[self.ListaCaras[FaceNumber].getA()].getX(), self.ListaPuntos3D[self.ListaCaras[FaceNumber].getA()].getY(), self.ListaPuntos3D[self.ListaCaras[FaceNumber].getA()].getZ())

            glVertex3f(self.ListaPuntos3D[self.ListaCaras[FaceNumber].getA()].getX()*scale_from_editor*zoom, 
            self.ListaPuntos3D[self.ListaCaras[FaceNumber].getA()].getY()*scale_from_editor*zoom, 
            self.ListaPuntos3D[self.ListaCaras[FaceNumber].getA()].getZ()*scale_from_editor*zoom)

            if (smooth):
                glNormal3f(self.ListaPuntos3D[self.ListaCaras[FaceNumber].getB()].getX(), self.ListaPuntos3D[self.ListaCaras[FaceNumber].getB()].getY(), self.ListaPuntos3D[self.ListaCaras[FaceNumber].getB()].getZ())

            glVertex3f(self.ListaPuntos3D[self.ListaCaras[FaceNumber].getB()].getX()*scale_from_editor*zoom, 
            self.ListaPuntos3D[self.ListaCaras[FaceNumber].getB()].getY()*scale_from_editor*zoom, 
            self.ListaPuntos3D[self.ListaCaras[FaceNumber].getB()].getZ()*scale_from_editor*zoom)

            if (smooth):
                glNormal3f(self.ListaPuntos3D[self.ListaCaras[FaceNumber].getC()].getX(), self.ListaPuntos3D[self.ListaCaras[FaceNumber].getC()].getY(), self.ListaPuntos3D[self.ListaCaras[FaceNumber].getC()].getZ())

            glVertex3f(self.ListaPuntos3D[self.ListaCaras[FaceNumber].getC()].getX()*scale_from_editor*zoom, 
            self.ListaPuntos3D[self.ListaCaras[FaceNumber].getC()].getY()*scale_from_editor*zoom, 
            self.ListaPuntos3D[self.ListaCaras[FaceNumber].getC()].getZ()*scale_from_editor*zoom)
            
            glVertex3f(self.ListaPuntos3D[self.ListaCaras[FaceNumber].getA()].getX()*scale_from_editor*zoom, 
            self.ListaPuntos3D[self.ListaCaras[FaceNumber].getA()].getY()*scale_from_editor*zoom,
            self.ListaPuntos3D[self.ListaCaras[FaceNumber].getA()].getZ()*scale_from_editor*zoom)                    
            
            glEnd()

    def chooseMaterial(self):
        self.material.randomMaterial()