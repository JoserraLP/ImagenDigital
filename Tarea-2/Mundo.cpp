#include "Mundo.h"

Mundo::Mundo() {

	// Inicializamos todo:

	width=800;
	height=800;
	aspect = width/height;
	angulo = 0;
	window=0;

	// Factor para el tamaño del modelo.
	escalaGeneral = 0.005;

	// Rotacion de los modelos.
	alpha=0; 
	beta=0;

	// Variables para la gestion del ratón.
	xold=0;
	yold=0;
	zoom=1.0;

	iDibujo=4;
	iFondo=0;
}


void Mundo::drawAxis(void) {
	
	// Inicializamos
	glDisable(GL_LIGHTING);
	glBegin(GL_LINES);
	glClearColor(0.f, 0.f, 0.0f, 0.f);
	
	// Eje X Rojo
	glColor3f(1.f, 0.f, 0.f);
	glVertex3f(0.0f, 0.0f, 0.0f);
	glVertex3f((float) tamanio, 0.0f, 0.0f);

	// Eje Y Verde
	glColor3f(0.f, 1.f, 0.f);
	glVertex3f(0.0f, 0.0f, 0.0f);
	glVertex3f(0.0f, (float) tamanio, 0.0f);

	// Eje Z Azul
	glColor3f(0.f, 0.f, 1.f);
	glVertex3f(0.0f, 0.0f, 0.0f);
	glVertex3f(0.0f, 0.0f, (float) tamanio);

	glClearColor(0.f, 0.f, 0.0f, 0.f);

	glEnd();
	glEnable(GL_LIGHTING);
}


void Mundo::drawModel(Modelo modelo,float escala) {
			glDisable(GL_LIGHTING);
			modelo.Draw_Model(wired,escala,zoom);
			glEnable(GL_LIGHTING);

}

void Mundo::display(void) {
	glClearDepth(1.0);
	glClearColor(colores[getIFondo()][0], colores[getIFondo()][1], colores[getIFondo()][2], 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	glRotatef(alpha, 1.0f, 0.0f, 0.0f);
	glRotatef(beta, 0.0f, 1.0f, 0.0f);

	// Establecemos el color del Modelo.
	glColor3f(colores[getIDibujo()][0], colores[getIDibujo()][1], colores[getIDibujo()][2]);
		
	// Pintamos el modelo.
	drawModel(Sol,escalaGeneral);

	glFlush(); 
	glutSwapBuffers();
}


////////////////////////////////////////////////////////////////////////////////
// Funcion para gestionar los movimientos del raton.
void Mundo::onMouse(int button, int state, int x, int y) {
	if ((button == 3) || (button == 4)){
		if (state == GLUT_UP)
			return;
		if(button==3)
                    {zoom=zoom-0.1;cout<<"Zoom negativo...."<<zoom<<endl;}
		else
                    {zoom=zoom+0.1;cout<<"Zoom poditivo...."<<zoom<<endl;}
	} else {
		// Actualizamos los valores de x, y.
		xold = x;
		yold = y; 
	}

}


////////////////////////////////////////////////////////////////////////////////
// Funcion que actualiza la posicion de los modelos en la pantalla segun los movimientos del raton.
void Mundo::onMotion(int x, int y) {
	alpha = (alpha + (y - yold));
	beta = (beta + (x - xold));
	xold = x;
	yold = y;
	glutPostRedisplay();
}

// Funcion que gestiona las pulsaciones en el teclado.
void Mundo::keyPressed(unsigned char key, int x, int y) {
	switch (key) {
		// Tecla Esc.
		case 27:	
			// Cerramos la ventana y salimos.
			glutDestroyWindow(window);
			exit(0);
			break;
        }               
/*
		// Tecla espacio	
		case 32:	
			
			break;

		default:
			// Numeros del 0 al 7
			if(key>=48 && key<=55)	
                        {};
			break;
	}
	*/
}


////////////////////////////////////////////////////////////////////////////////
void Mundo::setVector4(GLfloat *v, GLfloat v0, GLfloat v1, GLfloat v2, GLfloat v3) {
	v[0] = v0;
	v[1] = v1;
	v[2] = v2;
	v[3] = v3;
}

////////////////////////////////////////////////////////////////////////////////
// Funcion para activar las distintas opciones que permite el menu.
void Mundo::onMenu(int opcion) {
switch (opcion) {
	case FONDO_1:
		setIFondo(0);
		break;
	case FONDO_2:
		setIFondo(1);
		break;
	case FONDO_3:
		setIFondo(2);
		break;
	case DIBUJO_1:
		setIDibujo(3);
		break;
	case DIBUJO_2:
		setIDibujo(4);
		break;
	case DIBUJO_3:
		setIDibujo(5);
		break;
	}
	glutPostRedisplay();
}


////////////////////////////////////////////////////////////////////////////////
void Mundo::cargarModelo(char *nombre){ 
	Sol.Load_Model(nombre);
}


////////////////////////////////////////////////////////////////////////////////
int Mundo::getWidth() {
	return width;
}


////////////////////////////////////////////////////////////////////////////////
int Mundo::getHeight() {
	return height;
}

////////////////////////////////////////////////////////////////////////////////
void Mundo::setIFondo(int iFondo) {
	this->iFondo = iFondo;
}


////////////////////////////////////////////////////////////////////////////////
int Mundo::getIFondo() {
	return iFondo;
}


////////////////////////////////////////////////////////////////////////////////
void Mundo::setIDibujo(int iDibujo) {
	this->iDibujo = iDibujo;
}


////////////////////////////////////////////////////////////////////////////////
int Mundo::getIDibujo() {
	return iDibujo;
}

Mundo::~Mundo() {
}
