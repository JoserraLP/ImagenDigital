/*
  Se trata básicamente de diseñar una aplicación que mediante una máquina de
  estados controle el tráfico de personas a través de la puerta de un aula
  tomando como base los datos adquiridos a través de las ímagenes de video
  de una cámara cenita.
  Se propone de entrada utilizar un aproximación centrada en determinar
  las diferencias entre una imagen base inicial neutra y las sucesivas imágenes del
  tren de video y a partir de ellas seguir el tracking del centroide considerando
  dos barreras virtuales para la contrucción de la máquina de estados.
  */

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <qdebug.h>
#include <iostream>   // std::cout
#include <string>

vector<vector<Point> > contours;
vector<Vec4i> hierarchy;

using namespace std;

// Constructor member
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // Object video creation
    cap= new VideoCapture();
    cap->open("video.wmv"); // original video
    // settings sizes
    cap->set(CV_CAP_PROP_FRAME_WIDTH,320); // fix width
    cap->set(CV_CAP_PROP_FRAME_HEIGHT,240); // fix heigth

    // Barriers positions
    raw1=128;raw2=200;


    // Qimages for viewers
    Q_current_image = new QImage(320,240, QImage::Format_RGB888);


    // Viewers
    viewer_original = new RCDraw(320,240, Q_current_image, ui->viewer_original);


    // Run connect and start timer
    connect(&timer,SIGNAL(timeout()),this,SLOT(compute()));
    timer.start(100);
}

// Destructor member
MainWindow::~MainWindow()
{
    delete ui;
    delete cap;
    delete Q_current_image;

 }


// Process loop implementation on SLOT
void MainWindow::compute()
{
   ////////////////// CAMERA  //////////////////////////
   if(!cap->isOpened())  // check if we succeeded
       exit(-1);
   // Get a image from video
   *cap >> Current_Image;

   // BGR2RGB
   cvtColor(Current_Image, Current_Image, CV_BGR2RGB,1);


   //Draw barrier lines and copy to current image viewer
   cv::line(Current_Image,Point(0,raw1),Point(Current_Image.cols-1,raw1),CV_RGB(0,255,255),1);
   cv::line(Current_Image,Point(0,raw2),Point(Current_Image.cols-1,raw2),CV_RGB(0,255,255),1);
   memcpy(Q_current_image->bits(),Current_Image.data, Current_Image.rows*Current_Image.cols*sizeof(uchar)*3 );
   viewer_original->update();

}
