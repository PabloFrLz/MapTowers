from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Imagem com campos por cima")
        self.resize(800, 600)

        # Widget principal que vai conter tudo
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 1. QLabel como fundo
        self.background = QLabel(main_widget)
        self.background.setPixmap(QPixmap("sua_imagem.jpg"))  # ou :/resources/imagem.png
        self.background.setScaledContents(True)   # ajusta a imagem ao tamanho
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Importante: permitir que outros widgets fiquem por cima
        self.background.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        # Adiciona o background no layout
        main_layout.addWidget(self.background)

        # 2. Cria os campos de texto e posiciona por cima
        self.create_text_fields()

        self.setLayout(main_layout)  # ou main_widget.setLayout...

    def create_text_fields(self):
        # Exemplo: vários QLineEdit sobrepostos na imagem
        campos = [
            ("Nome", 100, 150),
            ("Email", 100, 200),
            ("Telefone", 100, 250),
            ("Endereço", 100, 320),
        ]

        for texto, x, y in campos:
            edit = QLineEdit(self)
            edit.setPlaceholderText(texto)
            edit.setFixedWidth(300)
            # Posicionamento absoluto em relação à janela principal
            edit.move(x, y)
            edit.show()   # importante