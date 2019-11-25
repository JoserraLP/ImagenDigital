#-------------------------------------------------
#
# Project created by QtCreator 2013-02-27T12:38:09
#
#-------------------------------------------------

QT       += core gui opengl xml 

TARGET = Counters_Match
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp\
rcdraw.cpp

HEADERS  += mainwindow.h\
               rcdraw.h

LIBS += -L/usr/local/lib  -lopencv_core -lopencv_imgproc -lopencv_highgui  -lopencv_video -lopencv_features2d -lopencv_calib3d -lopencv_objdetect -lopencv_videoio -lopencv_imgcodecs -lglut

INCLUDEPATH += -I/usr/local/include
FORMS    += mainwindow.ui

#-lqglviewer-qt4
