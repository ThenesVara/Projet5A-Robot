
from json import load
from time import sleep
import sys
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QPushButton,QLineEdit
from PyQt5 import QtGui, QtWidgets,QtCore 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPointF,QRect
from numpy import *


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

    # def get_pos(self,event):

    #     pos_x,pos_y=event.scenePos()


    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))
    
    #fonction de mouvement au clavier pour commencer 

    def get_pos(self):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))
        return self.pos().x(),self.pos().y()
    #cette fonction nous renvoie la position actuel du robot 

    #def rotation_center(self,x,y,w,l):
     #   self.setTransformOriginPoint(0,0)
      #  return

    def get_angle(self):
        print(self._angle)
        return self._angle

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




class GraphicView(QGraphicsView):

    _angle=0

    def __init__(self,X,Y):
        
        super().__init__()
        self.img = QPixmap("D:/affichage dynamique/table_2023.png") #On crée un élément Pixmap
        pixmap_resized = self.img.scaled(1200,1000)  #on le met à la taille de notre scene
        self.scene = QGraphicsScene()  #On crée un élément scene sur lequel on ajoute nos objets dynamique
        
        self.setScene(self.scene) #affiche la scene 
        self.setSceneRect(0, 0, 1200, 1000) #met la scene sous forme de rectangle
        self.label = QtWidgets.QLabel()
        self.scene.addPixmap(pixmap_resized) #on ajoute notre pixamp a la scene

        self.moveObject = Robot(X, Y, 100, 120) 
        #self.moveObject.setTransformOriginPoint(0,0)
        self.scene.addItem(self.moveObject) #ajoute l'objet 1 sur la scène
        #argument pour tester la fonction moveTo
        argx=0
        argy=0
        self.Moveto =QPushButton(self)
        self.Moveto.setText("Move to")          #text
        #self.setupButton.setShortcut('Ctrl+D')  #shortcut key


        
        self.moveTox = QLineEdit(self)
        #self.moveTox.setGeometry(QRect(170,80,191,31))#Permet de rédéfinir la taille du widget Qline Edit 
     
        self.moveTox.move(5,20)
        self.scene.addWidget(self.moveTox) #commande pour ajouter le widget Qline edit sur la scene, sans cette commande il ne sera pas affiché sur la scène.

        self.moveToy = QLineEdit(self)

        self.moveToy.move(5,40)
        self.scene.addWidget(self.moveToy)
        self.Moveto.clicked.connect(self.avancer_vers_pos1) 
        self.Moveto.move(5,5)

    def avancer_vers_pos1(self):

        
        x,y=self.moveObject.get_pos()
        xp,yp= int(self.moveTox.text()),int(self.moveToy.text()) #ferme la fenetre
        angle=self.moveObject.get_angle()
        self.moveTox.clear()
        self.moveToy.clear()


        if x<xp:
            while x<xp:
                self.moveObject.move(x+10,y,0)
                x,y=self.moveObject.get_pos()
                sleep(1)
                #self.moveObject.setPos(xp,y)
                
        else:
            while x>xp:  
                self.moveObject.move(x-10,y,0)
                x,y=self.moveObject.get_pos()
                sleep(1)
                #self.moveObject.setPos(xp,y)

        
        if y<yp:
            while y<yp:
                self.moveObject.move(x,y+10,0)
                x,y=self.moveObject.get_pos()
                sleep(1)
                #self.moveObject.setPos(x,yp)

        else:
            while y>yp:
                self.moveObject.move(x,y-10,0)
                x,y=self.moveObject.get_pos()
                
                sleep(1)
                #self.moveObject.setPos(x,yp)


        return self.moveObject.get_pos()


        

#gestion des événement de mouvement au clavier 

    def keyPressEvent(self, event):
        
        if event.key() == Qt.Key_Left:
            print("rotation left")
            x,y=self.moveObject.get_pos()
            angle=self.moveObject.get_angle()
            self.moveObject.setAngle(angle+10)

        elif event.key()==Qt.Key_Right:

            angle=self.moveObject.get_angle()
            self.moveObject.setAngle(angle-10)


        elif event.key()==Qt.Key_Down:
            print("move back")
            x,y=self.moveObject.get_pos()
            self.moveObject.move(x,y,-10) 

        elif event.key()==Qt.Key_Up:
            print("move forward")
            x,y=self.moveObject.get_pos()
            self.moveObject.move(x,y,10)

        elif event.key()==Qt.Key_R:
            self.reset()
        
        elif event.key()==Qt.Key_A:
            print(self.moveObject.rect())
        
        elif event.key()==Qt.Key_Space:
            print('x: {0}, y: {1}'.format(self.moveObject.pos().x(), self.pos().y()))

    
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
        self.label.setPixmap(QtGui.QPixmap(self.img))
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