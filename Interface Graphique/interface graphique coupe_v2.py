#-------------------------------------------------------------------------------
# Name:        Interface Graphique coupe_v2
# Purpose:     Interface graphique pour gérer et voir en temps réel les déplacements du robot
#
# Author:      aymeric
#
# Created:     12/09/2022
# Copyright:   (c) aymeric 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QPushButton,QLineEdit
from PyQt5 import QtGui, QtWidgets,QtCore 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPointF,QThread,QRectF  #Qthreead devra à terme gérer les déplacements du robots 
from numpy import *
import threading 
import Serial_comm

from classe_robot import * #classe qui gère l'entitée robot et tous les fonctions de mouvement qui lui sont associées 


class GraphicView(QGraphicsView):

    _angle=0

    def __init__(self,X,Y):
        
        super().__init__()
        self.img = QPixmap("table_2023_2.png") #On crée un élément Pixmap
        pixmap_resized = self.img.scaled(1200,800)  #on le met à la taille de notre scene
        self.scene = QGraphicsScene()  #On crée un élément scene sur lequel on ajoute nos objets dynamique     


        #◙elf.scene.addItem(self.carre)
        
        self.setScene(self.scene) #affiche la scene 
        self.setSceneRect(0, 0, 1300,1000) #met la scene sous forme de rectangle
        
        self.scene.addPixmap(pixmap_resized) #on ajoute notre pixamp a la scene
        self.rect=QRectF(X,Y,100,120)

        self.moveObject = Robot(X, Y, 100, 120) 
        #self.moveObject.setTransformOriginPoint(0,0)
        self.scene.addItem(self.moveObject) #ajoute l'objet 1 sur la scène
        #argument pour tester la fonction moveTo


        """
        Dans cette partie nous regroupons les widgets qui sont utiles pout les phases de test ou pour le logiciel de simulation
        ceux-ci peuvent et seront commentés quand le programme passera dans la carte de gestion de l'interface graphique. 

        """

        argx=0
        argy=0
        self.Moveto =QPushButton(self)
        self.Moveto.setText("Move to")          #text


        #le 1er label sert à gérer la position en temps réel du robot, le second le point d'arrivée 

        self.label = QtWidgets.QLabel(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))
        self.scene.addWidget(self.label)
        self.label.setGeometry(300,0,300,10)

        #Second label qui sert à gérer la position en temps réel du robot. 

        self.label_target = QtWidgets.QLabel(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))
        self.scene.addWidget(self.label_target)
        self.label_target.setGeometry(300,15,300,10)



        self.moveTox = QLineEdit(self)     
        self.moveTox.move(5,20)
        self.scene.addWidget(self.moveTox) #commande pour ajouter le widget Qline edit sur la scene, sans cette commande il ne sera pas affiché sur la scène.

        self.moveToy = QLineEdit(self)
        self.moveToy.move(5,40)
        self.scene.addWidget(self.moveToy)
        self.Moveto.clicked.connect(self.avancer_vers_pos1_tampon) 
        self.Moveto.move(5,5)

        """
        fin des widgets à commenter 
        """
        #widget pour la communication : 
            #widget bouton pour les phases de tests 
        self.read_comm =QPushButton(self)
        self.read_comm.setText("read_comm")
        self.scene.addWidget(self.read_comm)
        self.read_comm.move(800,5)
        self.read_comm.clicked.connect(self.readString)

            #widget pour l'affichage des coordonnées renvoyé par la carte de direction. 

        self.label_comm = QtWidgets.QLabel(str(0))
        self.scene.addWidget(self.label_comm)
        self.label_comm.setGeometry(800,25,50,10)

    def readString(self):
        CoordX=Serial_comm.serial_comm()
        self.label_comm.setText(CoordX)

    """
    fonction pour avancer avec un angle 
    elle sera stocké dans un fichier txt en attendant de réusssir à la faire fonctionner. 
    
    """
    def avancer_vers_pos1_tampon(self):
        xp,yp= int(self.moveTox.text()),int(self.moveToy.text())
        self.avancer_vers_pos1(xp,yp)

    def avancer_vers_pos1(self,xp,yp):

        x,y=self.moveObject.get_pos()
        #xp,yp= int(self.moveTox.text()),int(self.moveToy.text()) #récupère les infos dans les zone de text
        self.scene.addLine(x+100+50,y+300+60,xp+100+50,yp+300+60)
        self.label_target.setText(str([xp,yp,self.moveObject.calc_ang_dep(x,xp,y,yp)]))
        angle=self.moveObject.get_angle()
        print("l'angle de départ est:",angle)
        self.moveTox.clear()
        self.moveToy.clear()

        print("je tourne au début")
        self.rotation_canvas(xp,yp)
        self.moveObject.move(xp,yp,10)
        #dans un premier temps on va simplement déplacer le robot en x
        print("deplacement en x")
        
        if x!=xp:
            print("1er déplacement")
            while xp-x>0:
              
                self.moveObject.move(x,y,2)
                x,y=int(self.moveObject.get_pos()[0]),int(self.moveObject.get_pos()[1])
                self.label.setText(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))
                app.processEvents()
                sleep(0.01)
                #self.moveObject.setPos(xp,y)

            while xp-x<0:  
                    print("déplacement")
                    self.moveObject.move(x,y,-2)
                    x,y=int(self.moveObject.get_pos()[0]),int(self.moveObject.get_pos()[1])
                    self.label.setText(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))
                    app.processEvents()
                    sleep(0.01)
                    #self.moveObject.setPos(xp,y)

        #ensuite on tourne 
        self.angle_f=int(self.moveObject.calc_ang_dep(x,xp,y,yp))
        print("l'angle avant de tourner est: ",self.angle_f)
        
    def rotation_canvas(self,xp,yp):

        x,y=self.moveObject.get_pos()
        self.angle_f=int(self.moveObject.calc_ang_dep(x,xp,y,yp))
        print("angle dep:",self.moveObject.get_angle())
        print("angle arrivée:",self.angle_f)
        if self.moveObject.get_angle() != self.angle_f:
            while self.angle_f-self.moveObject.get_angle() !=0:
                if self.angle_f<90:
                    print("j'augmente mon angle")
                    self.moveObject.setAngle(self.moveObject.get_angle()+1)
                    self.label.setText(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))
                    app.processEvents()   #Pour que l'application ne freeze pas on appel cette fonction afin qu'à chaque tick le robot bouge quand même
                    sleep(0.01)
                if self.angle_f>=90:
                    print("je réduis mon angle")
                    self.moveObject.setAngle(self.moveObject.get_angle()-1)
                    self.label.setText(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))
                    app.processEvents()   #Pour que l'application ne freeze pas on appel cette fonction afin qu'à chaque tick le robot bouge quand même
                    sleep(0.01)
                else:
                    print("angle final:",self.moveObject.get_angle())
                    pass
        print("angle final:",self.moveObject.get_angle())
        return

#gestion des événement de mouvement au clavier 

    def keyPressEvent(self, event):
        
        if event.key() == Qt.Key_Left:
            print("rotation left")
            x,y=self.moveObject.get_pos()
            angle=self.moveObject.get_angle()
            self.moveObject.setAngle(angle-10)
            self.label.setText(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))

        elif event.key()==Qt.Key_Right:

            angle=self.moveObject.get_angle()
            self.moveObject.setAngle(angle+10)
            self.label.setText(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))

        elif event.key()==Qt.Key_Down:
            print("move back")
            x,y=self.moveObject.get_pos()
            self.moveObject.move(x,y,-10) 
            self.label.setText(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))

        elif event.key()==Qt.Key_Up:
            print("move forward")
            x,y=self.moveObject.get_pos()
            self.moveObject.move(x,y,10)
            self.label.setText(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))

        elif event.key()==Qt.Key_R:
            self.reset()
            self.label.setText(str([self.moveObject.get_pos(),self.moveObject.get_angle()]))
        
        elif event.key()==Qt.Key_A:
            print(self.moveObject.rect())
        
        elif event.key()==Qt.Key_Space:
            print('x: {0}, y: {1}'.format(self.moveObject.pos().x(), self.pos().y()))
            self.label.setText(str(self.moveObject.get_pos()))

    
    #reset de la position du robot
    def reset(self):
        print("reset")
        self.moveObject.setPos(QPointF(0, 0))
        self.moveObject.setAngle(0)


         
class main_window(object):
    def __init_(self,dialog):
        app = QApplication(sys.argv)
        win = QWidget()
        #win.setMinimumSize(300, 300)
        self.label = QtWidgets.QLabel(dialog)
        vbox = QVBoxLayout()
        self.label = QLabel(win)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self;vbox.addWidget(self.label)
        win.setLayout(vbox)
        win.setWindowTitle("QLabel Demo")
        win.show()      
        sys.exit(app.exec_())
    


app = QApplication(sys.argv)
view = GraphicView(100,300)
view.show()
sys.exit(app.exec_())
