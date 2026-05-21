from PySide6.QtWidgets import (
    QFrame, QLineEdit, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtGui import QPixmap, Qt

import Recursos

class SidebarLeft(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recursos = Recursos.Recursos()
        #dados selecionados para mostrar na interface 
        self.expanded = True
        self.setup_ui()     # Monta o layout e widgets da sidebar da direita
        #self.apply_styles()        # QSS separado
        #self.setup_animations()   # QPropertyAnimation para largura
        #self.setup_connections()


    def setup_ui(self):  
        # 1. Container principal (QFrame semi-transparente)
        self.painel_esquerdo = QFrame(self)
        self.painel_esquerdo.setObjectName("painel_esquerdo")
        self.painel_esquerdo.setStyleSheet(self.recursos.style_qframe_3)
        
        self.layout_principal = QVBoxLayout() #conteiner vertical pra agrupar os elementos textuais

        #atributos da classe - apenas torres pois essa sidebar terá mais destaque que a outra
        self.torres_totais = QLineEdit("...")
        self.torres_vivo = QLineEdit("...")
        self.torres_claro = QLineEdit("...")
        self.torres_tim = QLineEdit("...")

        #inserção dos elementos
        self.layout_principal.addWidget(self.torres_totais)
        self.layout_principal.addWidget(self.torres_vivo)
        self.layout_principal.addWidget(self.torres_claro)
        self.layout_principal.addWidget(self.torres_tim)
        
        # Layout final da janela
        self.painel_esquerdo.setLayout(self.layout_principal)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.painel_esquerdo)
        main_layout.setContentsMargins(10, 10, 10, 10)  # margem da janela
        #self.layout_principal.addStretch()

        #configurações adicionais:
        self.setStyleSheet("""
            QLineEdit {
                background: transparent;
            }
        """)
        

    def toggle(self):
        # Animação de largura + mudança de texto/ícones
        pass


    def setAtributo(self, nome_atributo, val): # atualiza valores dos dados
        valor = str(val)
        if nome_atributo == self.recursos.nome_atributos[2]: self.torres_totais.setText(valor)
        if nome_atributo == self.recursos.nome_atributos[3]: self.torres_vivo.setText(valor)
        if nome_atributo == self.recursos.nome_atributos[4]: self.torres_claro.setText(valor)
        if nome_atributo == self.recursos.nome_atributos[5]: self.torres_tim.setText(valor)




