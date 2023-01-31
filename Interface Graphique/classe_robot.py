# -*- coding: utf-8 -*-
"""
Created on Mon May  2 17:50:48 2022

@author: rirpo
"""
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QPushButton,QLineEdit
from PyQt5 import QtGui, QtWidgets,QtCore 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPointF,QVariantAnimation
from numpy import *
from time import *

class Robot(QGraphicsRectItem):

    _angle=0

    def __init__(self,x,y,w,l,parents=None):
        
        super(Robot, self).__init__(parents)
        self.setRect(x, y,w,l)
        self.setBrush(Qt.red) #couleur 
        #self.setTransformOriginPoint(QPointF(x+w,y+l))

        # mouse hover event

    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))



    """
        Les fonctions suivantes regroupent les divers fonctions de caclul, de positionnement et de déplacement du robot 
    """
        
    def get_pos(self):
        #→print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))
        return int(self.pos().x()),int(self.pos().y())
    #cette fonction nous renvoie la position actuel du robot 

    def get_angle(self):
        print(self._angle)
        return self._angle

    def calc_ang_dep(self,x1,x2,y1,y2):
        angle=self.get_angle()

        if x1==x2:
            print("case x1=x2")
        #les coordonnées angulaires peuvent paraitres bizarres, cela est du à la manière dont Qt effectue la rotation autour d'un point, les angles sont donc dans le sens horaires 
        #270° permet d'aller de se tourner en haut et 90° en bas 
            if y2-y1>0:
                print("case 1")
                angle_final=270

            elif y2-y1<0:
                print("case 2")
                angle_final=90

            else:
                print("case 3")
                angle_final=0

        if y1==y2:
            print("case y1=y2")

            if x2-x1>0:
                print("case 1")
                angle_final=0
            elif x2-x1<0:
                print("case 2")
                angle_final=180

            #cette condition est peut être redondante, tester si elle est nécessaire      
            else:
                print("case 3")
                angle_final=0

        if x1!=x2 and y1!=y2:
            print("case normal")
            angle_final=arctan2((y2-y1),(x2-x1))*180/pi+360
            angle_final%=360
            print("angle final = ",angle_final)
            angle_final=angle_final-angle
            print(angle,angle_final)

        return angle_final

    def move(self,x,y,dep):
        cosang,sinang=self.calcul_dep()
        self.setPos(x+dep*cosang, y+dep*sinang)
        self.get_pos()          

    def setAngle(self, angle):
        x,y=self.get_pos()
        #self.rotation_center(x,y,0,0)
        angle %= 360
        if angle == self._angle:
            return
        self._angle = angle
        #self.setTransform(QtGui.QTransform().rotate(-angle))
        self.setTransformOriginPoint(self.mapFromScene(QtCore.QPointF(x+150 , y+360)))
        self.setRotation(angle)
        #self.adjustSize()

    def calcul_dep(self):
        angle=self.get_angle()
        #print(cos(angle*pi/180),sin(angle*pi/180))
        return cos(angle*pi/180),sin(angle*pi/180)



#print(arctan2((0-100),(200-100))*180/pi)
#print(arctan2((0-100),(200-100))*180/pi)