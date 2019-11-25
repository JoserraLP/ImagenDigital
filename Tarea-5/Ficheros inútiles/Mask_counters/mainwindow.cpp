/*
  Mainwindow gestiona el proceso global de adquirir una imagen
  de una caja browser, extraer las subimágenes de los contadores
  y lanzar un OCR para leer los números.
*/

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <qdebug.h>
#include <iostream>   // std::cout
#include <string>
#include <QFileDialog>

RNG rng(12345);

vector<vector<Point> > contours;
vector<Vec4i> hierarchy;

using namespace std;
// Constructor member
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);


    // Original Image and sub-images
    this->Image_Source = new QImage(720,540, QImage::Format_RGB888);
    this->image_counter = new QImage(304,130, QImage:: QImage::Format_Indexed8);
    this->image_counter2 = new QImage(304,130, QImage:: QImage::Format_Indexed8);
    this->image_counter3 = new QImage(304,130, QImage:: QImage::Format_Indexed8);

    // viewers
    viewer_original = new RCDraw(720,540, Image_Source, ui->viewer_original);
    viewer_counter1 = new RCDraw(304,130, image_counter, ui->viewer_counter1);
    viewer_counter2 = new RCDraw(304,130, image_counter2, ui->viewer_counter2);
    viewer_counter3 = new RCDraw(304,130, image_counter3, ui->viewer_counter3);




    // connect to button
    connect ( ui->Load_button, SIGNAL (clicked()), this, SLOT( Load_Image() ) );



}
// Destructor member
MainWindow::~MainWindow()
{
    delete ui;

    delete Image_Source;
    delete image_counter;
    delete image_counter2;
    delete image_counter3;
    delete viewer_original;
    delete viewer_counter1;
    delete viewer_counter2;
    delete viewer_counter3;
 }





void MainWindow::Load_Image()
{
     // Looking for a image name in a directory with browsing box
    QString Directory="capturas";
    QString fn = QFileDialog::getOpenFileName(this,"Choose a frame to download",Directory, "Images (*.png *.xpm *.jpg)");

    Original_Image= imread(fn.toStdString(), CV_LOAD_IMAGE_COLOR);
    cv::resize(Original_Image, mat_original, Size(720, 540), 0, 0, cv::INTER_CUBIC);
    memcpy(Image_Source->bits(),mat_original.data,mat_original.rows*mat_original.cols*sizeof(uchar)*3);
    viewer_original->update();
    }

