# Ripple.py (modifique ou crie novo)
from PySide6.QtWidgets import QGraphicsItem, QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import QRectF, QTimer, QPointF
import math

class RippleItem(QGraphicsItem, QWidget):
    def __init__(self, x, y, max_radius=0.5, speed=0.02, color=QColor(0, 180, 255)):
        super().__init__()
        self.setPos(x, y)
        self.current_radius = 0.05
        self.max_radius = max_radius
        self.speed = speed
        self.diametro_linha = 0.01
        self.opacity = 1.0
        self.color = color
        self.setZValue(10)  # acima das torres

        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advance)
        self.timer.start(16)  # ~60fps

    '''def create_another_ripple(self):
        print("im create")
        RippleItem(self.x(), self.y(), max_radius=1, speed=0.2)'''
            

        

    def boundingRect(self):
        return QRectF(-self.max_radius, -self.max_radius, 
                      self.max_radius*2, self.max_radius*2)
    

    def advance(self):
        self.current_radius += self.speed
        self.opacity = max(0.0, 1.0 - (self.current_radius / self.max_radius))
        
        if self.scene() is not None and self.opacity <= 0.01:
            self.scene().removeItem(self)  # se auto-remove
            #self.create_another_ripple() # cria outro ripple continuamente
            return
            
        self.update()  # força repaint

    def paint(self, painter, option, widget):
        if self.opacity <= 0:
            return
            
        alpha = int(self.opacity * 180)
        pen = QPen(QColor(self.color.red(), self.color.green(), self.color.blue(), alpha), self.diametro_linha)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawEllipse(QPointF(0, 0), self.current_radius, self.current_radius)