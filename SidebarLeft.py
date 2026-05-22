from PySide6.QtWidgets import (
    QFrame, QLineEdit, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtGui import QColor, QImage, QPixmap, Qt

import Recursos

class SidebarLeft(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recursos = Recursos.Recursos()
        #dados selecionados para mostrar na interface 
        self.expanded = True
        self.setup_ui()     # Monta o layout e widgets da sidebar da direita
        self.apply_styles()        # QSS separado
        #self.setup_animations()   # QPropertyAnimation para largura
        #self.setup_connections()


    '''def setup_ui(self):  
        # 1. Container principal (QFrame semi-transparente)
        self.painel_esquerdo = QFrame(self)
        self.painel_esquerdo.setObjectName("painel_esquerdo")
        self.painel_esquerdo.setStyleSheet(self.recursos.style_qframe_3)
        self.painel_esquerdo.setFixedWidth(100)
        self.painel_esquerdo.setContentsMargins(4, -6, 0, 0)
        
        
        self.layout_principal = QVBoxLayout() #conteiner vertical pra agrupar os elementos textuais

        self.background = QLabel()# background de topo da sidebar da esquerda
        self.background.setStyleSheet(self.recursos.card_board_gradient_vertical)
        #self.background.setPixmap(QPixmap("brasoes/Parana.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)) 
        #self.brasao_municipio()
        self.background.setText(self.recursos.getHTML("Curitiba - PR", "Parana.png"))
        self.background.setFixedSize(78, 100)
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        #atributos da classe - apenas torres pois essa sidebar terá mais destaque que a outra (SidebarRight)
        self.torres_totais = QLabel("...")
        self.torres_vivo = QLabel("...")
        self.torres_claro = QLabel("...")
        self.torres_tim = QLabel("...")
        self.torres_ligga = QLabel("...")
        
        # lendo o estilo e a imagem definida em Recursos()
        self.torres_totais.setStyleSheet(self.recursos.torres_totais_config_style)
        self.torres_vivo.setStyleSheet(self.recursos.vivo_config_style)
        self.torres_claro.setStyleSheet(self.recursos.claro_config_style)
        self.torres_tim.setStyleSheet(self.recursos.tim_config_style)
        self.torres_ligga.setStyleSheet(self.recursos.ligga_config_style)

        #inserção dos elementos
        self.layout_principal.addWidget(self.background)
        self.layout_principal.addWidget(self.torres_totais)
        self.layout_principal.addWidget(self.torres_vivo)
        self.layout_principal.addWidget(self.torres_claro)
        self.layout_principal.addWidget(self.torres_tim)
        self.layout_principal.addWidget(self.torres_ligga)
        
        # Layout final da janela
        self.painel_esquerdo.setLayout(self.layout_principal)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.painel_esquerdo)
        main_layout.setContentsMargins(10, 10, 10, 10)  # margem da janela
        #self.layout_principal.addStretch()
    '''
    def setup_ui(self):  
        # 1. Container principal (QFrame semi-transparente)
        self.painel_esquerdo = QFrame(self)
        self.painel_esquerdo.setObjectName("painel_esquerdo")
        self.painel_esquerdo.setFixedWidth(100)
        self.painel_esquerdo.setContentsMargins(4, -6, 0, 0)

        #conteiner vertical pra agrupar os elementos textuais
        self.layout_principal = QVBoxLayout() 
        
        # background de topo da sidebar da esquerda
        self.background = QLabel()
        self.background.setText(self.recursos.getHTML("Curitiba - PR", "Parana.png"))
        self.background.setFixedSize(78, 100)
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        #atributos da classe - apenas torres pois essa sidebar terá mais destaque que a outra (SidebarRight)
        self.torres_totais = QLabel("...")
        self.torres_vivo = QLabel("...")
        self.torres_claro = QLabel("...")
        self.torres_tim = QLabel("...")
        self.torres_ligga = QLabel("...")

        #inserção dos elementos
        self.layout_principal.addWidget(self.background)
        self.layout_principal.addWidget(self.torres_totais)
        self.layout_principal.addWidget(self.torres_vivo)
        self.layout_principal.addWidget(self.torres_claro)
        self.layout_principal.addWidget(self.torres_tim)
        self.layout_principal.addWidget(self.torres_ligga)
        
        # Layout final da janela
        self.painel_esquerdo.setLayout(self.layout_principal)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.painel_esquerdo)
        main_layout.setContentsMargins(10, 10, 10, 10)  # margem da janela


    def apply_styles(self):
        # estilo do QFrame
        self.painel_esquerdo.setStyleSheet(self.recursos.style_qframe_3)

        # estilo do background onde lê o nome do municipio e brasão
        self.background.setStyleSheet(self.recursos.card_board_gradient_vertical) 

         # Estilo dos Qlabels que contem a logo das operadoras e o numero total de torres
        self.torres_totais.setStyleSheet(self.recursos.torres_totais_config_style)
        self.torres_vivo.setStyleSheet(self.recursos.vivo_config_style)
        self.torres_claro.setStyleSheet(self.recursos.claro_config_style)
        self.torres_tim.setStyleSheet(self.recursos.tim_config_style)
        self.torres_ligga.setStyleSheet(self.recursos.ligga_config_style)



            

    def toggle(self):
        # Animação de largura + mudança de texto/ícones
        pass


    def setAtributo(self, nome_atributo, val): # atualiza valores dos dados
        valor = str(val)
        if nome_atributo == self.recursos.indice_dados[15]: self.torres_claro.setText(valor)
        if nome_atributo == self.recursos.indice_dados[16]: self.torres_vivo.setText(valor)
        if nome_atributo == self.recursos.indice_dados[17]: self.torres_tim.setText(valor)
        if nome_atributo == self.recursos.indice_dados[18]: 
            self.torres_ligga.setText(str(0))
            #[NOTA] quando chegar aqui os atributos já terão os dados necessarios pra calcular o total de torres
            soma = int(self.torres_claro.text()) + int(self.torres_tim.text()) + int(self.torres_vivo.text()) + int(self.torres_ligga.text())
            self.torres_totais.setText(str(soma))

    def set_brasao_municipio(self, nome, arquivo_nome):
        '''pixmap = QPixmap("brasoes/Parana.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap_gray = self.pixmap_to_grayscale_keep_alpha(pixmap)
        self.background.setPixmap(pixmap_gray)
        self.background.setContentsMargins(0,-20,0,0)'''
        self.background.setText(self.recursos.getHTML(nome, arquivo_nome))


    # reaproveitando esse metodo do projeto SEIAParkingManagement que transforma imagens em preto e branco
    def pixmap_to_grayscale_keep_alpha(self, pixmap):
        image = pixmap.toImage().convertToFormat(QImage.Format_ARGB32)

        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor.fromRgba(image.pixel(x, y))

                gray = int(
                    color.red() * 0.299 +
                    color.green() * 0.587 +
                    color.blue() * 0.114
                )

                color.setRed(gray)
                color.setGreen(gray)
                color.setBlue(gray)
                # alpha fica intacto
                image.setPixelColor(x, y, color)

        return QPixmap.fromImage(image)

