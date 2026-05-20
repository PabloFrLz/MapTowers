from PySide6.QtWidgets import (
    QHBoxLayout, QLineEdit, QWidget, QVBoxLayout, QLabel
)


class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #dados selecionados para mostrar na interface 
        self.nome_atributos = ["nome","regiao","total_torres","vivo","claro","tim","obrigacoes_unifique","ddd","area_total","populacao","localidades_sem_conecao"]
        self.expanded = True
        self.setup_ui()            # Monta layout e widgets
        #self.apply_styles()        # QSS separado
        #self.setup_animations()   # QPropertyAnimation para largura
        #self.setup_connections()
    
    def setup_ui(self):
        #widget principal que vai conter todos os demais conteineres ou elementos
        main_widget = QWidget(self)
        #conteiner vertical pra agrupar os elementos textuais
        self.conteiner_1 = QVBoxLayout(main_widget) 
        self.conteiner_1.setContentsMargins(0, 0, 0, 0)

        # Painel lateral (background da sidebar)
        self.background_sidebar = QLabel(main_widget)
        self.background_sidebar.setStyleSheet(
            """
            background: qlineargradient(
                x1:0, y1:0,
                x2:0, y2:1,
                stop:0 #111,
                stop:1 #222
            );
            """
        )
        '''
        self.background_sidebar.setPixmap(QPixmap("sua_imagem.jpg"))  # ou :/resources/imagem.png
        self.background_sidebar.setScaledContents(True)   # ajusta a imagem ao tamanho
        self.background_sidebar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Importante: permitir que outros widgets fiquem por cima
        self.background_sidebar.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        # Adiciona o background no layout
        main_layout.addWidget(self.background_sidebar)
        '''

        #inserir background abaixo do conteiner


        #atributos da classe
        self.nome = QLineEdit("...")
        self.regiao = QLineEdit("...")
        self.torres_totais = QLineEdit("...")
        self.torres_vivo = QLineEdit("...")
        self.torres_claro = QLineEdit("...")
        self.torres_tim = QLineEdit("...")
        self.obrigacoes_unifique = QLineEdit("...")
        self.ddd = QLineEdit("...")
        self.area = QLineEdit("...")
        self.populacao = QLineEdit("...")
        self.localidades_sem_conexao = QLineEdit("...")


        #inserção dos elementos
        self.conteiner_1.addWidget(self.nome)
        self.conteiner_1.addWidget(self.regiao)
        self.conteiner_1.addWidget(self.torres_totais)
        self.conteiner_1.addWidget(self.torres_vivo)
        self.conteiner_1.addWidget(self.torres_claro)
        self.conteiner_1.addWidget(self.torres_tim)
        self.conteiner_1.addWidget(self.obrigacoes_unifique)
        self.conteiner_1.addWidget(self.ddd)
        self.conteiner_1.addWidget(self.area)
        self.conteiner_1.addWidget(self.populacao)
        self.conteiner_1.addWidget(self.localidades_sem_conexao)

        #self.main_layout.addLayout(self.conteiner_1)
        #self.setLayout(self.main_layout)
        self.setLayout(self.conteiner_1)
        self.conteiner_1.addStretch() #joga pra cima
        #main_widget.setLayout(self.conteiner_1)
        

    def toggle(self):
        # Animação de largura + mudança de texto/ícones
        pass


    def setAtributo(self, nome_atributo, valor): # atualiza valores dos dados
        if nome_atributo == self.nome_atributos[0]: self.nome.setText(valor)
        if nome_atributo == self.nome_atributos[1]: self.regiao.setText(valor)
        if nome_atributo == self.nome_atributos[2]: self.torres_totais.setText(valor)
        if nome_atributo == self.nome_atributos[3]: self.torres_vivo.setText(valor)
        if nome_atributo == self.nome_atributos[4]: self.torres_claro.setText(valor)
        if nome_atributo == self.nome_atributos[5]: self.torres_tim.setText(valor)
        if nome_atributo == self.nome_atributos[6]: self.obrigacoes_unifique.setText(valor)
        if nome_atributo == self.nome_atributos[7]: self.ddd.setText(valor)
        if nome_atributo == self.nome_atributos[8]: self.area.setText(valor)
        if nome_atributo == self.nome_atributos[9]: self.populacao.setText(valor)
        if nome_atributo == self.nome_atributos[10]: self.localidades_sem_conexao.setText(valor)

    
    def calculoProporcaoAreasConectadas(self):
        total_areas_desconectadas = self.localidades_sem_conexao.displayText()
        #total_areas = ...

        percentual = (total_areas_desconectadas / total_areas) * 100
        self.localidades_sem_conexao.setText(str(percentual)+"%")

