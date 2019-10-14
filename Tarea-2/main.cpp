#include "Mundo.h"

Mundo mundo;

////////////////////////////////////////////////////////////////////////////////
void display(void){
	mundo.display();
}

////////////////////////////////////////////////////////////////////////////////
void onMenu(int opcion){
	mundo.onMenu(opcion);
}

////////////////////////////////////////////////////////////////////////////////
// Funcion que crea las distintas opciones que se pueden activar en los menus.
void creacionMenu(void) {
	int menuFondo, menuDibujo, menuPrincipal, menuForma;

	menuFondo = glutCreateMenu(onMenu);
	glutAddMenuEntry("Negro", FONDO_1);
	glutAddMenuEntry("Verde oscuro", FONDO_2);
	glutAddMenuEntry("Azul oscuro", FONDO_3);

	menuDibujo = glutCreateMenu(onMenu);
	glutAddMenuEntry("Blanco", DIBUJO_1);
	glutAddMenuEntry("Verde claro", DIBUJO_2);
	glutAddMenuEntry("Azul claro", DIBUJO_3);

        menuPrincipal = glutCreateMenu(onMenu);
	glutAddSubMenu("Color de fondo", menuFondo);
	glutAddSubMenu("Color del dibujo", menuDibujo);
	// Carga el menú con el boton derecho.
	glutAttachMenu(GLUT_RIGHT_BUTTON);
}

////////////////////////////////////////////////////////////////////////////////
void onMotion(int x,int y){
	mundo.onMotion(x,y);
}

////////////////////////////////////////////////////////////////////////////////
void onMouse(int button,int state,int x,int y){
	mundo.onMouse(button,state,x,y);
}

////////////////////////////////////////////////////////////////////////////////
void keyPressed(unsigned char key,int x,int y){
	mundo.keyPressed(key,x,y);
}

void InitGL()
{
    	// Activamos los bufferes
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_RGBA | GLUT_DEPTH | GLUT_ALPHA);	
	// Eestablece el tamaño de la ventana.
	glutInitWindowSize(mundo.getWidth(), mundo.getHeight());	
	//Establece la posicion inicial (esquina superior izquierda de la ventana).
	glutInitWindowPosition(100, 100);	
	glutCreateWindow("Mundo");
	glShadeModel(GL_SMOOTH); glEnable(GL_LIGHTING); glEnable(GL_NORMALIZE); glEnable(GL_CULL_FACE);
	glEnable(GL_DEPTH_TEST);
	glDepthMask(GL_TRUE);glDepthFunc(GL_LESS);
}

////////////////////////////////////////////////////////////////////////////////
int main(int argc, char **argv) {
        
	
	mundo.cargarModelo(argv[1]);


	glutInit(&argc, argv);
	
        // Declaraciones Globales
        InitGL();

	// Gestion de los botones del raton
	glutMouseFunc(&onMouse);
	// Gestion de los movimientos del raton	
	glutMotionFunc(&onMotion);	
        // Dibujo e Idle
	glutDisplayFunc(&display);
	glutIdleFunc(&display);
        // Menús
	creacionMenu();
	// Pulsaciones del teclado
	glutKeyboardFunc(&keyPressed);	
        
	//Repeat.
	glutMainLoop();	

	return 0;
}
