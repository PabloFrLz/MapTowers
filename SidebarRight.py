from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLineEdit, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtGui import QPixmap, Qt



class SidebarRight(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #dados selecionados para mostrar na interface 
        self.nome_atributos = ["nome","regiao","total_torres","vivo","claro","tim","obrigacoes_unifique","ddd","area_total","populacao","localidades_sem_conecao"]
        self.expanded = True
        self.setup_ui()     # Monta layout e widgets da sidebar da direita
        #self.apply_styles()        # QSS separado
        #self.setup_animations()   # QPropertyAnimation para largura
        #self.setup_connections()

        self.style_1 = """
            QFrame#panel {
                background: rgba(20, 20, 30, 0.65);     /* semi-transparente */
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);            /* se Qt suportar */
            }
        """

        self.card_board_gradient = """
            background: qlineargradient(
                x1:0, y1:0,
                x2:0, y2:1,
                stop:0 #111,
                stop:1 #222
            );
        """
    



    def setup_ui(self):
        # 1. Container principal (QFrame semi-transparente)
        self.painel_direita = QFrame(self)
        self.painel_direita.setObjectName("painel_direita")
        self.painel_direita.setStyleSheet(self.style_1)
        
        self.layout_principal = QVBoxLayout() #conteiner vertical pra agrupar os elementos textuais
        #self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.background = QLabel()# Painel lateral (background da sidebar)
        self.background.setStyleSheet(self.card_board_gradient)
        self.background.setPixmap(QPixmap("imagens/logo_seia_sidebar.png").scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) 
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter) 
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
        self.painel_direita.setLayout(self.layout_principal)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.painel_direita)
        main_layout.setContentsMargins(10, 10, 10, 10)  # margem da janela
        self.layout_principal.addStretch()
        '''self.setLayout(self.layout_principal)
        self.layout_principal.addStretch()''' #joga pra cima


    def toggle(self):
        # Animação de largura + mudança de texto/ícones
        pass


    def setAtributo(self, nome_atributo, val): # atualiza valores dos dados
        valor = str(val)
        if nome_atributo == self.nome_atributos[0]: self.nome.setText(valor)
        if nome_atributo == self.nome_atributos[1]: self.regiao.setText(valor)
        if nome_atributo == self.nome_atributos[2]: self.obrigacoes_unifique.setText(valor)
        if nome_atributo == self.nome_atributos[3]: self.ddd.setText(valor)
        if nome_atributo == self.nome_atributos[4]: self.area.setText(valor)
        if nome_atributo == self.nome_atributos[5]: self.populacao.setText(valor)
        if nome_atributo == self.nome_atributos[6]: self.localidades_sem_conexao.setText(valor)

    
    def calculoProporcaoAreasConectadas(self):
        total_areas_desconectadas = self.localidades_sem_conexao.displayText()
        #total_areas = ...

        percentual = (total_areas_desconectadas / total_areas) * 100
        self.localidades_sem_conexao.setText(str(percentual)+"%")

