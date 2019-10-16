import re

from point_face import Point3D, Face


class Modelo:
    alpha, beta, _numCaras, _numVertices

    #Lista de puntos 3D
    ListaPuntos3D = []

    #Lista de caras
	ListaCaras = []

    #include "Modelo.h"

def __init__:
	numCaras, numVertices, alpha, beta = 0, 0, 0, 0


def __init__(self, nCaras, nVertices):
    self._numCaras = nCaras
    self._numVertices = nVertices
    alpha, beta = 0, 0

def setVector(self, vector, v0, v1, v2, v3):
    vector[0] = v0
    vector[1] = v1
    vector[2] = v2
    vector[3] = v3

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


def Draw_Model(tipoVista iForma,float scale_from_editor, float zoom):
   // cout<<"Caras: "<<_NumCaras<<endl
    cout<<scale_from_editor<<endl
	for (int FaceNumber = 0 FaceNumber < _NumCaras FaceNumber++) {
                    glBegin(GL_LINES)
                        glVertex3f(ListaPuntos3D[ListaCaras[FaceNumber].getA()].getX()*scale_from_editor*zoom, ListaPuntos3D[ListaCaras[FaceNumber].getA()].getY()*scale_from_editor*zoom, ListaPuntos3D[ListaCaras[FaceNumber].getA()].getZ()*scale_from_editor*zoom)
                        glVertex3f(ListaPuntos3D[ListaCaras[FaceNumber].getB()].getX()*scale_from_editor*zoom, ListaPuntos3D[ListaCaras[FaceNumber].getB()].getY()*scale_from_editor*zoom, ListaPuntos3D[ListaCaras[FaceNumber].getB()].getZ()*scale_from_editor*zoom)
                        glVertex3f(ListaPuntos3D[ListaCaras[FaceNumber].getC()].getX()*scale_from_editor*zoom, ListaPuntos3D[ListaCaras[FaceNumber].getC()].getY()*scale_from_editor*zoom, ListaPuntos3D[ListaCaras[FaceNumber].getC()].getZ()*scale_from_editor*zoom)
			
			glVertex3f(ListaPuntos3D[ListaCaras[FaceNumber].getA()].getX()*scale_from_editor*zoom, ListaPuntos3D[ListaCaras[FaceNumber].getA()].getY()*scale_from_editor*zoom, ListaPuntos3D[ListaCaras[FaceNumber].getA()].getZ()*scale_from_editor*zoom)                    glEnd()	       glEnd()	
		}

