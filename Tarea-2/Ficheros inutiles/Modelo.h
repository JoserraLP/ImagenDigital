#ifndef MODELO_H_
#define MODELO_H_

#include "Cara.h"
#include "Punto3D.h"
#include <cstdio>
#include <cstring>
#include <GL/glut.h>
#include <GL/glu.h>
#include <GL/gl.h>
#include <iostream>
#include <math.h>
#include <vector>

using namespace std;

typedef vector<Cara> ListaFace;
typedef vector<Punto3D> ListaVertex;

 enum tipoVista {wired};


class Modelo {

private:
	float alpha;
	float beta;

	ListaVertex ListaPuntos3D;
	ListaFace ListaCaras;

	int _NumCaras;
	int _NumVertices;

	void setVector4(GLfloat *v, GLfloat v0, GLfloat v1, GLfloat v2, GLfloat v3);

public:
	Modelo();
	~Modelo();
	Modelo(const int ncaras, const int nvertices);
	void inicializarParametros();
	int getNCaras();
	void setNCaras(const int val);
	int getNVertices();
	void setNVertices(const int val);
	void Load_Model(char fileName[50]);
	void Draw_Model(tipoVista iForma,float scale_from_editor, float zoom);

};

#endif /* MODELO_H_ */
