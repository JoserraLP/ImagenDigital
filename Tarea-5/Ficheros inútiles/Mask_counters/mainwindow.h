#ifndef MAINWINDOW_H
#define MAINWINDOW_H
#include <QMainWindow>
#include "GL/glut.h"


#include <rcdraw.h>


#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/videoio/videoio.hpp"
#include "opencv2/video/video.hpp"

#include "opencv2/core/core.hpp"
#include "opencv2/imgcodecs.hpp"


#include <iostream>
#include <stdio.h>
#include <stdlib.h>

#include <QCoreApplication>
using namespace cv;
using namespace std;



namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:

   explicit MainWindow(QWidget *parent = 0);

    ~MainWindow();

private:



    Ui::MainWindow *ui;

     // user viewers
    RCDraw *viewer_original;
    RCDraw *viewer_counter1;
    RCDraw *viewer_counter2;
    RCDraw *viewer_counter3;


//---------------------------------------------
    // Qimages associated to viewers
    QImage *Image_Source;
    QImage *image_counter;
    QImage *image_counter2;
    QImage *image_counter3;



     //---------------------------------------------



    Mat  Original_Image, mat_original, mat_processed, mat_counter, mat_counter2, mat_counter3;



public slots: // Connect to user buttons
        void Load_Image();

private slots:

};

#endif // MAINWINDOW_H
