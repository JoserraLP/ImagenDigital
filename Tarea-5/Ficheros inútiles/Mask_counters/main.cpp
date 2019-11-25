/* Proy_1.
Gestión de la ventana principal de un proyecto QT
  de Imagen Digital que utiliza una cámara, un visor
  para la imagen capturada y dos visores para las
  imágenes procesadas con operaciones básicas en OpenCV,
  en este caso paso a gris y un gaussiano seguido de un
  extractor de bordes Canny */

#include <QApplication>
#include "mainwindow.h"

int main(int argc, char *argv[])
{
    QApplication guau(argc, argv);
    MainWindow w;
    w.show();
    return guau.exec();
}
