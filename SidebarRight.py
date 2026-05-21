from PySide6.QtWidgets import (
    QFrame, QLineEdit, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtGui import QPixmap, Qt

import Recursos

class SidebarRight(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recursos = Recursos.Recursos()
        #dados selecionados para mostrar na interface 
        self.expanded = True
        self.setup_ui()     # Monta layout e widgets da sidebar da direita
        #self.apply_styles()        # QSS separado
        #self.setup_animations()   # QPropertyAnimation para largura
        #self.setup_connections()


    def setup_ui(self):
        # 1. Container principal (QFrame semi-transparente)
        self.painel_direito = QFrame(self)
        self.painel_direito.setObjectName("painel_direito")
        self.painel_direito.setStyleSheet(self.recursos.style_qframe_2)
        self.painel_direito.setContentsMargins(7, -5, 0, 0)


        self.layout_principal = QVBoxLayout() #conteiner vertical pra agrupar os elementos textuais
        #self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.background = QLabel()# Painel lateral (background da sidebar)
        self.background.setStyleSheet(self.recursos.card_board_gradient_vertical)
        self.background.setPixmap(QPixmap("imagens/logo_seia_sidebar.png").scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) 
        self.background.setFixedWidth(235) #fixando manualmente a largura pra caber na interface
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        #self.background.move(self.background.x() + 150, self.background.y())
        #self.layout_principal.setContentsMargins(20,0,0,0)
        #self.background.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # permite que outros widgets fiquem por cima  

        #atributos da classe - apenas informações técnicas - informações sobre torres estará na outra sidebar
        self.nome = QLineEdit("...")
        self.regiao = QLineEdit("...")
        self.obrigacoes_unifique = QLineEdit("...")
        self.ddd = QLineEdit("...")
        self.area = QLineEdit("...")
        self.populacao = QLineEdit("...")
        self.localidades_sem_conexao = QLineEdit("...")

        #inserção dos elementos
        self.layout_principal.addWidget(self.background)
        self.layout_principal.addWidget(self.nome)
        self.layout_principal.addWidget(self.regiao)
        self.layout_principal.addWidget(self.obrigacoes_unifique)
        self.layout_principal.addWidget(self.ddd)
        self.layout_principal.addWidget(self.area)
        self.layout_principal.addWidget(self.populacao)
        self.layout_principal.addWidget(self.localidades_sem_conexao)

        # Layout final da janela
        self.painel_direito.setLayout(self.layout_principal)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.painel_direito)
        main_layout.setContentsMargins(10, 10, 10, 10)  # margem da janela
        self.layout_principal.addStretch()

        # Configurações adicionais
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
        if nome_atributo == self.recursos.nome_atributos[0]: self.nome.setText(valor)
        if nome_atributo == self.recursos.nome_atributos[1]: self.regiao.setText(valor)
        if nome_atributo == self.recursos.nome_atributos[6]: self.obrigacoes_unifique.setText(valor)
        if nome_atributo == self.recursos.nome_atributos[7]: self.ddd.setText(valor)
        if nome_atributo == self.recursos.nome_atributos[8]: self.area.setText(valor)
        if nome_atributo == self.recursos.nome_atributos[9]: self.populacao.setText(valor)
        if nome_atributo == self.recursos.nome_atributos[10]: self.localidades_sem_conexao.setText(valor)

    
    def calculoProporcaoAreasConectadas(self):
        total_areas_desconectadas = self.localidades_sem_conexao.displayText()
        #total_areas = ...

        percentual = (total_areas_desconectadas / total_areas) * 100
        self.localidades_sem_conexao.setText(str(percentual)+"%")

