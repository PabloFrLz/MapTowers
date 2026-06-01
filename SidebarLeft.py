from PySide6.QtWidgets import (
    QFrame, QLineEdit, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtGui import QColor, QImage, QPixmap, Qt
from PySide6.QtCore import QPointF

import Recursos, Ripple

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
        self.torres_totais = QLabel()
        self.torres_vivo = QLabel()
        self.torres_claro = QLabel()
        self.torres_tim = QLabel()
        self.torres_ligga = QLabel()
        self.lista_torres = [self.torres_tim, self.torres_claro, self.torres_vivo, self.torres_ligga] # menos torres_totais

        #inserção dos elementos
        self.layout_principal.addWidget(self.background)
        self.layout_principal.addWidget(self.torres_totais)
        self.layout_principal.addWidget(self.torres_vivo)
        self.layout_principal.addWidget(self.torres_claro)
        self.layout_principal.addWidget(self.torres_tim)
        self.layout_principal.addWidget(self.torres_ligga)

        
        #  __________________________
        # |    ANIMAÇÃO DAS TORRES   |
        # |__________________________|

        self.ondas = Ripple.RippleWidget(self, self.width(), self.height()+300)
        self.ondas.setStyleSheet("background-color: transparent;")
        #self.layout_principal.addWidget(self.ondas)

        # configurações finais
        self.painel_esquerdo.setLayout(self.layout_principal)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.painel_esquerdo)
        main_layout.setContentsMargins(10, 10, 10, 10)  # margem da janela
        self.layout_principal.addStretch()


    def apply_styles(self):
        # estilo do QFrame
        self.painel_esquerdo.setStyleSheet(self.recursos.style_theme_1_aux)

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
        # normalizar: se o dado for None, usar '0' para evitar strings 'None'
        valor = '0' if val is None else str(val)
        if nome_atributo == self.recursos.indice_dados[15]: self.torres_claro.setText(valor)
        if nome_atributo == self.recursos.indice_dados[16]: self.torres_vivo.setText(valor)
        if nome_atributo == self.recursos.indice_dados[17]: self.torres_tim.setText(valor)
        if nome_atributo == self.recursos.indice_dados[18]: 
            for i, torre in enumerate(self.lista_torres):
                if torre.text() == "" or torre.text() == "None": # para os campos vazios na lista de dados.xlsx (json)
                    self.lista_torres[i].setText('0') # substitui o valor de None para 0 (string) pra evitar erros na hora do calculo abaixo
            #[NOTA] quando chegar aqui os atributos já terão os dados necessarios pra calcular o total de torres
            soma = int(self.torres_claro.text()) + int(self.torres_tim.text()) + int(self.torres_vivo.text()) + int(self.torres_ligga.text())
            self.torres_totais.setText(str(soma))
        
        #trecho adequado para iniciar animação
        self.play()

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

    
    def play(self):
        #obtendo as coordenadas absolutas dos objetos que contém a imagem das operadoras
        pos1 = self.torres_totais.mapTo(self.painel_esquerdo, self.torres_totais.rect().center())
        pos2 = self.torres_claro.mapTo(self.painel_esquerdo, self.torres_claro.rect().center())
        pos3 = self.torres_vivo.mapTo(self.painel_esquerdo, self.torres_vivo.rect().center())
        pos4 = self.torres_tim.mapTo(self.painel_esquerdo, self.torres_tim.rect().center())
        pos5 = self.torres_ligga.mapTo(self.painel_esquerdo, self.torres_ligga.rect().center())

        # aplicando a animação que tem foco apartir da coordenada obtida
        '''self.ondas.create_ripple(QPointF(pos1.x()+10, pos1.y()+10), False)
        self.ondas.create_ripple(QPointF(pos2.x()+10, pos2.y()+10), False)
        self.ondas.create_ripple(QPointF(pos3.x()+10, pos3.y()+10), False)
        self.ondas.create_ripple(QPointF(pos4.x()+10, pos4.y()+10), False)
        self.ondas.create_ripple(QPointF(pos5.x()+10, pos5.y()+10), False)'''

        self.ondas.create_ripple(QPointF(pos1.x()+10, pos1.y()+10))
        self.ondas.create_ripple(QPointF(pos2.x()+10, pos2.y()+10))
        self.ondas.create_ripple(QPointF(pos3.x()+10, pos3.y()+10))
        self.ondas.create_ripple(QPointF(pos4.x()+10, pos4.y()+10))
        self.ondas.create_ripple(QPointF(pos5.x()+10, pos5.y()+10))
    