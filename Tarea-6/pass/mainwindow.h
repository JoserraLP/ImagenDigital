#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/video/video.hpp>
#include <opencv2/videoio/videoio.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <opencv2/calib3d/calib3d.hpp>
#include <opencv2/video/tracking.hpp>
#include "opencv2/core/cuda.hpp"
#include "opencv2/video/background_segm.hpp"
#include "opencv2/imgcodecs.hpp"


#include <rcdraw.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

using namespace cv;
using namespace std;


#include <iostream>



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
    int raw1,raw2;

    Ui::MainWindow *ui;
    QTimer timer; // Slot Timer
    VideoCapture *cap; //

    RCDraw *viewer_original;
    QImage *Q_current_image;


    Mat  Current_Image;


public slots:
        void compute();

};

#endif // MAINWINDOW_H
