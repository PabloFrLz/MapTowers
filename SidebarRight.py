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
        self.apply_styles()        # QSS separado
        #self.setup_animations()   # QPropertyAnimation para largura
        #self.setup_connections()


    def setup_ui(self):
        # 1. Container principal (QFrame semi-transparente)
        self.painel_direito = QFrame(self)
        self.painel_direito.setObjectName("painel_direito")
        self.painel_direito.setContentsMargins(10, -5, 0, 0)

        #conteiner vertical pra agrupar os elementos textuais
        self.layout_principal = QVBoxLayout() 
        self.background = QLabel()# background de topo da sidebar da esquerda
        self.background.setPixmap(QPixmap("imagens/logo_seia_sidebar_full.png").scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) 
        self.background.setFixedWidth(235) #fixando manualmente a largura pra caber na interface
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter) # alinhar ao centro
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

        

    def apply_styles(self):
        # estilo do QFrame
        self.painel_direito.setStyleSheet(self.recursos.style_qframe_2)

        #estilo de gradient do background superior onde vai a logo do estado do paraná
        self.background.setStyleSheet(self.recursos.card_board_gradient_vertical)
        
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
        if nome_atributo == self.recursos.indice_dados[2]: self.nome.setText(valor)
        if nome_atributo == self.recursos.indice_dados[1]: self.regiao.setText("...")
        if nome_atributo == self.recursos.indice_dados[21]: self.obrigacoes_unifique.setText(valor)
        if nome_atributo == self.recursos.indice_dados[22]: self.ddd.setText(valor)
        if nome_atributo == self.recursos.indice_dados[23]: self.area.setText(valor)
        if nome_atributo == self.recursos.indice_dados[25]: self.populacao.setText(valor)
        if nome_atributo == self.recursos.indice_dados[20]: self.localidades_sem_conexao.setText(valor)

    
    def calculoProporcaoAreasConectadas(self):
        total_areas_desconectadas = self.localidades_sem_conexao.displayText()
        #total_areas = ...

        percentual = (total_areas_desconectadas / total_areas) * 100
        self.localidades_sem_conexao.setText(str(percentual)+"%")

