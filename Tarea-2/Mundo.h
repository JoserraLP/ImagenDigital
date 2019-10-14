#ifndef MUNDO_H_
#define MUNDO_H_

#include "Modelo.h"
#include <iostream>
#include <sys/time.h>
#include <time.h>

using namespace std;


// Distintas opciones del menu.
typedef enum { 	FONDO_1, FONDO_2, FONDO_3, FONDO_4,
				DIBUJO_1, DIBUJO_2, DIBUJO_3, DIBUJO_4,
				FORMA_1, FORMA_2, FORMA_3, FORMA_4
			} opcionesMenu;

// Número de vistas diferentes.
const int numCamaras = 3;

// Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
const float colores [6][3] = {
		{ 0.00f, 0.00f, 0.00f}, // 0 - negro
		{ 0.06f, 0.25f, 0.13f}, // 1 - verde oscuro
		{ 0.10f, 0.07f, 0.33f}, // 2 - azul oscuro
		{ 1.00f, 1.00f, 1.00f}, // 3 - blanco
		{ 0.12f, 0.50f, 0.26f}, // 4 - verde claro
		{ 0.20f, 0.14f, 0.66f}, // 5 - azul claro
};


class Mundo {

	int width;
	int height;
	float aspect;
	float angulo;
	int window;
	Modelo Sol;
        
	// Tamaño de los ejes y del alejamiento de Z.
	int tamanio;
	int z0;

	// Factor para el tamaño del modelo.
	float escalaGeneral;

	// Rotacion de los modelos.
	float alpha; 
	float beta;

	// Variables para la gestion del ratón.
	int xold;
	int yold;
	float zoom;


	// Vistas del Sistema Planetario.
	tipoVista iForma;
	int iFondo;
	int iDibujo;


public:
	Mundo();

        void drawAxis(void);
	void display(void);
	void onMouse(int button, int state, int x, int y);
	void onMotion(int x, int y);

	void keyPressed(unsigned char key, int x, int y);
	void onMenu(int opcion);
	void setVector4(GLfloat *v, GLfloat v0, GLfloat v1, GLfloat v2, GLfloat v3);
	void cargarModelo(char* nombreModelo);
	int getWidth();
	int getHeight();
;
	void setIFondo(int iFondo);
	int getIFondo();
	void setIDibujo(int iDibujo);
	int getIDibujo();
	void drawModel(Modelo modelo,float escala);


	~Mundo();
};

#endif /* MUNDO_H_ */
