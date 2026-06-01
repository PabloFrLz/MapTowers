from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPen
import math
import sys

# Classe com animação de ondas circulares, similar as ondas de uma gota caindo na agua.
# basicamente é um circulo que tem seu raio aumentado gradativamente


class Ripple:
    def __init__(self, x, y, radius=2.0, max_radius=60.0, opacity=1.0, speed=1.8, diametro_linha_circulo=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.max_radius = max_radius
        self.opacity = opacity
        self.speed = speed    # quanto cresce por frame
        self.diametro_linha_circulo = diametro_linha_circulo


class RippleWidget(QWidget):
    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.setMinimumSize(width, height)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # ← importante
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background: transparent;")  # fundo transparente
        
        self.ripples = []
        # Timer para animação suave
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

        # Timer para criar novas ondas (efeito contínuo)
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.create_ripple)
        self.spawn_timer.start(800)  # nova onda a cada 800ms

    
    def create_ripple(self, pos=None):
        '''
        if pos is None:
            # Cria no centro por padrão
            pos = QPointF(self.width() / 2, self.height() / 2)
        '''
        if pos is not None:
            self.ripples.append(Ripple(pos.x(), pos.y()))
            print(f"x:{pos.x()} y:{pos.y()}")
        #print("im execute that")
    
    '''
    def create_ripple(self, pos=None, isTorres=None):
        #if pos is not None:
        if isTorres:
            self.ripples.append(Ripple(pos.x(), pos.y(), 0.2, 8.0, 0.1, 0.18, 0.1)) # animação das torres no mapa
        else:
            self.ripples.append(Ripple(pos.x(), pos.y())) # animação das torres na sidebar left
        
        self.update() # forma correta de chamar o paintEvent() - diz ao pyqt que o widget precisa ser redesenhado.
    '''
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.transparent) # fundo transparente

        for ripple in self.ripples[:]:
            # Calcula cor com opacidade
            alpha = int(ripple.opacity * 180)
            color = QColor(0, 180, 255, alpha)
            
            pen = QPen(color, ripple.diametro_linha_circulo)
            painter.setPen(pen)
            painter.drawEllipse(QPointF(ripple.x, ripple.y), ripple.radius, ripple.radius)

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

