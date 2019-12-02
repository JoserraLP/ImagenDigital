#-------------------------------------------------
#
# Project created by QtCreator 2013-02-27T12:38:09
#
#-------------------------------------------------

QT       += core gui opengl xml 

TARGET = proyID_1
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp\
rcdraw.cpp

HEADERS  += mainwindow.h\
               rcdraw.h

LIBS += -L/usr/local/lib  -lopencv_imgproc -lopencv_videoio -lopencv_imgcodecs -lopencv_core -lopencv_highgui -lopencv_features2d -lopencv_flann -lopencv_video -lopencv_calib3d

FORMS    += mainwindow.ui

#-lqglviewer-qt4
