from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPen
import math
import sys

# Classe com animação de ondas circulares, similar as ondas de uma gota caindo na agua.
# basicamente é um circulo que tem seu raio aumentado gradativamente


class Ripple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 2.0
        self.max_radius = 80.0
        self.opacity = 1.0
        self.speed = 1.8    # quanto cresce por frame
        self.diametro_linha_circulo = 1


class RippleWidget(QWidget):
    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.setMinimumSize(width, height)
        self.ripples = []
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        # Timer para animação suave
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

        # Timer para criar novas ondas (efeito contínuo)
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.create_ripple)
        self.spawn_timer.start(800)  # nova onda a cada 800ms

    '''
    def create_ripple(self, pos=None):
        if pos is None:
            # Cria no centro por padrão
            pos = QPointF(self.width() / 2, self.height() / 2)
        
        self.ripples.append(Ripple(pos.x(), pos.y()))
    '''

    def create_ripple(self, pos=None):
        if pos is not None:
            self.ripples.append(Ripple(pos.x(), pos.y()))
            self.update() # forma correta de chamar o paintEvent() - diz ao pyqt que o widget precisa ser redesenhado.

    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for ripple in self.ripples[:]:
            # Calcula cor com opacidade
            alpha = int(ripple.opacity * 180)
            color = QColor(0, 180, 255, alpha)
            
            pen = QPen(color, ripple.diametro_linha_circulo)
            painter.setPen(pen)
            painter.drawEllipse(QPointF(ripple.x, ripple.y), 
                              ripple.radius, ripple.radius)

            # Atualiza ripple
            ripple.radius += ripple.speed
            ripple.opacity = max(0.0, 1.0 - (ripple.radius / ripple.max_radius))

            # Remove quando ficar invisível
            if ripple.opacity <= 0.01:
                self.ripples.remove(ripple)

    '''            
    def mousePressEvent(self, event):
        """Cria ripple onde o usuário clicar"""
        self.create_ripple(event.position())
        # Opcional: várias ondas ao clicar
        # QTimer.singleShot(80, lambda: self.create_ripple(event.position()))
        # QTimer.singleShot(160, lambda: self.create_ripple(event.position()))
    '''

