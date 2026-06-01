from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLayout, QLineEdit, QPushButton, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtCore import QPoint, QPropertyAnimation, QSize
from shiboken6 import isValid

import Recursos, MplCanvas 

class SidebarRight(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # atributos da classe
        self.parent_main = parent
        self.recursos = Recursos.Recursos()
        self.enable_graphs = True
        self.enable_animation = True
        self.expanded = True

        #conteiners adicionais
        self.widget_graphs = QWidget()
        self.conteiner_graphs = None # conteiner que será usado pra armazenar os gráficos
        self.widget_graphs.setFixedHeight(Recursos.HEIGHT / 1.5)
        self.widget_graphs.setStyleSheet(self.recursos.graphs_background)
        self.widget_graphs.setVisible(False) # inicialmente eles nao aparecem na interface - aparecem apenas quando estiver deslocando 
        self.conteiner_graphs = QVBoxLayout(self.widget_graphs) # conteiner que será usado pra armazenar os gráficos
        

        # init da aplicação
        self.widget_main = QWidget()
        self.setup_ui()     # Monta layout e widgets da sidebar da direita
        self.apply_styles()        # QSS separado
        #self.setup_animations()   # QPropertyAnimation para largura
        #self.setup_connections()


    def setup_ui(self):
        # 1. Container principal (QFrame semi-transparente)
        self.painel_direito = QFrame(self)
        self.painel_direito.setObjectName("painel_direito")
        #self.painel_direito.setFixedWidth(310)
        self.painel_direito.setContentsMargins(0, -6, 0, 0)

        #conteiner vertical pra agrupar os elementos textuais
        self.layout_principal = QVBoxLayout() 
        self.background = QLabel()# background de topo da sidebar da esquerda
        self.background.setPixmap(QPixmap("imagens/logo_seia_sidebar_full.png").scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) 
        self.background.setFixedWidth(280) #fixando manualmente a largura pra caber na interface
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter) # alinhar ao centro
        #self.background.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # permite que outros widgets fiquem por cima  

        #atributos da classe - apenas informações técnicas - informações sobre torres estará na outra sidebar
        '''
        self.fid = QLineEdit("...")
        self.cd_mun = QLineEdit("...")
        self.nm_mun = QLineEdit("...")
        self.latitude = QLineEdit("...")
        self.longitude = QLineEdit("...")
        '''

         #  _________________________________________
         # |         GERANDO AS INFORMAÇÕES          |
         # |_________________________________________|
         
        #dados do municipio
        self.municipio = QLineEdit("...")
        self.fid = QLineEdit("...")
        self.cd_mun = QLineEdit("...")
        self.regiao = QLineEdit("...")
        self.ddd = QLineEdit("...")
        self.populacao = QLineEdit("...")
        # dados relevantes sobre torres
        self.area_total = QLineEdit("...")
        self.area_conectada = QLineEdit("...")
        self.area_desconectada = QLineEdit("...")
        self.percentual_area_conectada = QLineEdit("...")
        self.percentual_area_desconectada = QLineEdit("...")
        self.obrigacoes_unifique = QLineEdit("...")
        self.localidades_sem_conexao = QLineEdit("...")
        #dados relevantes sobre redes de ensino do estado do paraná
        self.rede_municipal_ensino = QLineEdit("...")
        self.rede_estadual_ensino = QLineEdit("...")

        # conteiner + Qlabel + QLineEdit pra gerar o campo de informações da sidebar da direita
        self.municipio_conteiner = self.gerarCampoDeInformacao("MUNICÍPIO:", self.municipio)
        self.fid_conteiner = self.gerarCampoDeInformacao("FID:", self.fid)
        self.cd_mun_conteiner = self.gerarCampoDeInformacao("CD_MUN:", self.cd_mun)
        self.regiao_conteiner = self.gerarCampoDeInformacao("REGIÃO:", self.regiao)
        self.ddd_conteiner = self.gerarCampoDeInformacao("DDD:", self.ddd)
        self.populacao_conteiner = self.gerarCampoDeInformacao("Nº HABITANTES:", self.populacao)
        self.area_total_conteiner = self.gerarCampoDeInformacao("AREA TOTAL:", self.area_total)
        self.area_conectada_conteiner = self.gerarCampoDeInformacao("AREA CONECTADA:", self.area_conectada)
        self.area_desconectada_conteiner = self.gerarCampoDeInformacao("AREA DESCONECTADA:", self.area_desconectada)
        self.percentual_area_conectada_conteiner = self.gerarCampoDeInformacao("% AREA CONECTADA:", self.percentual_area_conectada)
        self.percentual_area_desconectada_conteiner = self.gerarCampoDeInformacao("% AREA DESCONECTADA:", self.percentual_area_desconectada)
        self.obrigacoes_unifique_conteiner = self.gerarCampoDeInformacao("OBRIGAÇÕES UNIFIQUE:", self.obrigacoes_unifique)
        self.localidades_sem_conexao_conteiner = self.gerarCampoDeInformacao("LOCALIDADES SEM CONEXÃO:", self.localidades_sem_conexao)
        self.rede_municipal_ensino_conteiner = self.gerarCampoDeInformacao("ESCOLAS MUNICIPAIS:", self.rede_municipal_ensino)
        self.rede_estadual_ensino_conteiner = self.gerarCampoDeInformacao("ESCOLAS ESTADUAIS:", self.rede_estadual_ensino)

         #  __________________________
         # |         GRUPO 1          |
         # |__________________________|
         # cria o 1º grupo que conterá dados do municipio
        # colocar informações especificas uma ao lado da outra pra economiza espaço da sidebar da direita
        self.conteiner_comprimido_1 = self.agrupandoInfos(self.cd_mun_conteiner, self.fid_conteiner)
        self.conteiner_comprimido_2 = self.agrupandoInfos(self.regiao_conteiner, self.ddd_conteiner)
        self.titulo1 = QLabel("MUNICÍPIO")
        self.titulo1.setStyleSheet(self.recursos.titulos)
        self.group_1 = QVBoxLayout()
        self.group_1.addWidget(self.titulo1)
        self.group_1.addItem(self.municipio_conteiner)
        self.group_1.addItem(self.conteiner_comprimido_1)
        self.group_1.addItem(self.conteiner_comprimido_2)
        self.group_1.addItem(self.populacao_conteiner)
        # Envolver o grupo em um QFrame para aplicar stylesheet pra inserir um fundo escuro com opacidade
        self.grupo_com_background_1 = QFrame()
        self.grupo_com_background_1.setLayout(self.group_1)
        self.grupo_com_background_1.setStyleSheet(self.recursos.style_qframe_1) # aplica efeito de fundo escuro transparente e bordas

         #  __________________________
         # |         GRUPO 2          |
         # |__________________________|
         # cria o 2º grupo que conterá dados de area e conexões
        # para o grupo 2 não será possível agrupar informações uma do lado da outra pois isso ocultaria algumas informações dado o tamanho da area da sidebar
        self.titulo2 = QLabel("AREA E CONEXÃO")
        self.titulo2.setStyleSheet(self.recursos.titulos)
        self.group_2 = QVBoxLayout()
        self.group_2.addWidget(self.titulo2)
        self.group_2.addItem(self.area_total_conteiner)
        self.group_2.addItem(self.area_conectada_conteiner)
        self.group_2.addItem(self.area_desconectada_conteiner)
        self.group_2.addItem(self.percentual_area_conectada_conteiner)
        self.group_2.addItem(self.percentual_area_desconectada_conteiner)
        self.group_2.addItem(self.obrigacoes_unifique_conteiner)
        self.group_2.addItem(self.localidades_sem_conexao_conteiner)

        self.grupo_com_background_2 = QFrame()
        self.grupo_com_background_2.setLayout(self.group_2)
        self.grupo_com_background_2.setStyleSheet(self.recursos.style_qframe_1)

         #  __________________________
         # |         GRUPO 3          |
         # |__________________________|
         # cria o 3º grupo que conterá dados da rede de ensino dos municipios
        self.titulo3 = QLabel("REDE DE ENSINO")
        self.titulo3.setStyleSheet(self.recursos.titulos)
        self.group_3 = QVBoxLayout()
        self.group_3.addWidget(self.titulo3)
        self.group_3.addItem(self.rede_municipal_ensino_conteiner)
        self.group_3.addItem(self.rede_estadual_ensino_conteiner)

        self.grupo_com_background_3 = QFrame()
        self.grupo_com_background_3.setLayout(self.group_3)
        self.grupo_com_background_3.setStyleSheet(self.recursos.style_qframe_1)

        #inserindo os QFrames no grupo pra facilitar a animação 
        self.array_widget_grupos = [self.grupo_com_background_1, self.grupo_com_background_2, self.grupo_com_background_3]

        #inserção dos conteiners no layout principal
        self.layout_principal.addWidget(self.background) # plano de fundo é inserido como widget e nao como item
        
        self.layout_principal.addWidget(self.grupo_com_background_1) # adiciona o grupo 1 com fundo escuro no layout principal
        self.layout_principal.addWidget(self.grupo_com_background_2) # adiciona o grupo 2 com fundo escuro no layout principal
        self.layout_principal.addWidget(self.grupo_com_background_3) # adiciona o grupo 3 com fundo escuro no layout principal

        #  ______________________________
        # |     BUTTON PARA GRÁFICOS     |
        # |______________________________|

        # Botão para transicionar para a seção de gráficos
        self.btn_graficos = QPushButton()
        self.btn_graficos_icon_hide =  QIcon(self.recursos.path_button_graphics_hide)
        self.btn_graficos_icon_show =  QIcon(self.recursos.path_button_graphics_show)
        self.btn_graficos.setIcon(self.btn_graficos_icon_hide) #inicialmente mostra o icone de retraído/escondido
        self.btn_graficos.clicked.connect(self.geraGraficos) # se conecta a função que tratará de gerar os gráficos.

        # Botão para habilitar/desabilitar as animações
        self.btn_animation = QPushButton()
        self.btn_animation_icon_off = QIcon(self.recursos.path_animation_off)
        self.btn_animation_icon_on = QIcon(self.recursos.path_animation_on)
        self.btn_animation.setIcon(self.btn_animation_icon_off) # icone de animação desativada irá destoar dos demais em cor pra dar maior destaque pro usuario saber quando um recurso gráfico relevante foi desativado
        self.btn_animation.clicked.connect(self.activateAnimation)

        # insere os Botoes no layout
        self.conteiner_buttons_sidebar_right = QHBoxLayout() #conteiner lateral pros buttons ficarem um do lado do outro
        self.conteiner_buttons_sidebar_right.addWidget(self.btn_graficos)
        self.conteiner_buttons_sidebar_right.addWidget(self.btn_animation)
        self.btn_graficos.setIconSize(QSize(100, 20)) # alterar tamanho dos buttons pra imagem ficar melhor renderizada
        self.btn_animation.setIconSize(QSize(100, 20))
        self.layout_principal.insertLayout(1, self.conteiner_buttons_sidebar_right) # insere o widget na segunda posição do conteiner, abaixo da logo principal da secretaria ou diretoria (depende do tema)
        
        #self.btn_graficos.setParent(self.painel_direito)
        #self.btn_graficos.setGeometry(Recursos.WIDTH - 50, Recursos.HEIGHT-600, 50, 50)
        # ou
        #self.btn_graficos.move(Recursos.WIDTH - 50, Recursos.HEIGHT-600)

        #  _______________________________________
        # |     ANIMAÇÃO DE TRANSIÇÃO DE TELA     |
        # |_______________________________________|

        # animação da largura para rolar a sidebar para a direita
        self.animacoes = []
        for grupo in self.array_widget_grupos: # cria uma animação pra cada grupo que contém as informações dos municipios
            animacao = QPropertyAnimation(grupo, b"pos")
            animacao.setDuration(Recursos.DURATION_ANIMATION_SLIDE)
            self.animacoes.append(animacao)
        
        # animação do deslizamento do gráfico
        self.animacao_graph = QPropertyAnimation(self.widget_graphs, b"pos")
        self.animacao_graph.setDuration(Recursos.DURATION_ANIMATION_SLIDE)


        #  ________________________________
        # |     CONFIGURAÇÕES PONTUAIS     |
        # |________________________________|
        self.painel_direito.setLayout(self.layout_principal)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.painel_direito)
        self.main_layout.setContentsMargins(10, 10, 10, 10)  # margem da janela
        self.layout_principal.addStretch()

        
    #  ______________________________
    # |           ESTILOS            |
    # |______________________________|

    def apply_styles(self):
        # estilo do QFrame
        self.painel_direito.setStyleSheet(self.recursos.style_theme_1)
        #estilo de gradient do background superior onde vai a logo do estado do paraná
        self.background.setStyleSheet(self.recursos.card_board_gradient_vertical)
        # Configurações adicionais
        self.setStyleSheet("""
            QLineEdit {
                background: transparent;
            }
        """)

    '''
    def toggle(self):
        # Animação de largura + mudança de texto/ícones
        pass
    '''
    
    #  ______________________________________
    # |     INFORMAÇÕES DA SIDEBAR RIGHT     |
    # |______________________________________|

    def gerarCampoDeInformacao(self, descricao, info):
        conteiner = QHBoxLayout()
        descricao = QLabel(descricao)
        conteiner.addWidget(descricao)
        conteiner.addWidget(info)
        info.setReadOnly(True) # pra nao permitir escrita nem copia dos valores
        return conteiner
    
    def agrupandoInfos(self, info1, info2): 
        conteiner_comprimido_1 = QHBoxLayout()
        conteiner_comprimido_1.addItem(info1)
        conteiner_comprimido_1.addItem(info2)
        conteiner_comprimido_1.addStretch() # comprime mais à esquerda pra reduzir mais ainda o espaço
        return conteiner_comprimido_1

    #  ______________________________
    # |     TRATAMENTO DOS DADOS     |
    # |______________________________|

    def setAtributo(self, nome_atributo, val): # atualiza valores dos dados
        valor = str(val) 
        if nome_atributo == self.recursos.indice_dados[2]: self.municipio.setText(valor)
        if nome_atributo == self.recursos.indice_dados[0]: self.fid.setText(valor) 
        if nome_atributo == self.recursos.indice_dados[1]: self.cd_mun.setText(valor) 
        if nome_atributo == self.recursos.indice_dados[1]: self.regiao.setText("...")
        if nome_atributo == self.recursos.indice_dados[22]: self.ddd.setText(valor)
        if nome_atributo == self.recursos.indice_dados[25]: self.populacao.setText(f"{float(valor):.2f}")
        if nome_atributo == self.recursos.indice_dados[12]: self.area_total.setText(f"{float(valor):.2f}"+"km²") # area km²
        if nome_atributo == self.recursos.indice_dados[13]: 
            self.area_conectada.setText(f"{float(valor):.2f}"+"km²") 
            var = self.getAreaDesconectada()
            self.area_desconectada.setText(var+"km²") 
        if nome_atributo == self.recursos.indice_dados[14]: 
            self.percentual_area_conectada.setText(f"{float(valor):.2f}"+"%") 
            var = self.getPercentualAreaDesconectada()
            self.percentual_area_desconectada.setText(var+"%")
        if nome_atributo == self.recursos.indice_dados[21]: self.obrigacoes_unifique.setText(valor)
        if nome_atributo == self.recursos.indice_dados[20]: self.localidades_sem_conexao.setText(valor)

        if nome_atributo == self.recursos.indice_dados[19]: self.rede_municipal_ensino.setText(valor)
        if nome_atributo == self.recursos.indice_dados[18]: self.rede_estadual_ensino.setText(valor) 



    def getAreaDesconectada(self):
        area_tot = self.area_total.displayText().split("k") # removendo a string 'km²' do numero float em string pra nao dar erro na hora da conversao em float()
        area_conect = self.area_conectada.displayText().split("k")
        areaDesconectada = float(area_tot[0]) - float(area_conect[0])
        return f"{areaDesconectada:.2f}" #retorna já formatado pra mostra só duas casas após a vírgula

    
    def getPercentualAreaDesconectada(self):
        perc_conectado_string = self.percentual_area_conectada.displayText().split("%") # removendo a string '%'
        perc_conectado = float(perc_conectado_string[0])
        perc_desconectado = 100 - perc_conectado
        return f"{perc_desconectado:.2f}" #retorna já formatado pra mostra só duas casas após a vírgula


    #  ______________________________________
    # |     AÇÃO DOS BOTÕES DA APLICAÇÃO     |
    # |______________________________________|

    def geraGraficos(self):
        if self.enable_graphs:
            self.btn_graficos.setIcon(self.btn_graficos_icon_show) # altera imagem do ícone para retratar que foi expandido
            # gera gráfico...
            # self.conteiner_graphs = QVBoxLayout(self.widget_graphs) # conteiner que será usado pra armazenar os gráficos
            for i in range(3): # cria 3 novos graficos e empilha um abaixo do outro
                graph = MplCanvas.MplCanvas(self)
                graph.createGraphs() # monta o gráfico
                self.conteiner_graphs.addWidget(graph)
                
            
            self.layout_principal.insertWidget(2, self.widget_graphs) # insere o widget do grafico na GUI na posição posterior a posição dos botoes de grafico e de desabilitar animações
            #self.main_layout.addWidget(self.widget_graphs)
            self.transitToGraphs() # empurra os dados pro lado direito com uma animação de deslocação no eixo x
        else:
            self.btn_graficos.setIcon(self.btn_graficos_icon_hide) # altera imagem do ícone para escondido 'hide'
            # ocultar gráficos...
            self.transitToGraphs() # logica de destruição dos objetos esta dentro do metodo
            
        self.enable_graphs = not self.enable_graphs # inverte

    def activateAnimation(self):
        if self.enable_animation: # desabilita animações da aplicação
            self.btn_animation.setIcon(self.btn_animation_icon_on)
            #implementar logica de desativação das animações
        else:
            self.btn_animation.setIcon(self.btn_animation_icon_off)
            #implementar lógica de habilitação das animações
        self.enable_animation = not self.enable_animation


    def transitToGraphs(self):
        if self.expanded: 
            # [ANIMAÇÃO 1]: empurra os elementos da sidebar pra direita (ocultando-os)
            for i, animacao in enumerate(self.animacoes):
                animacao.setStartValue(QPoint(0, self.array_widget_grupos[i].y()))
                animacao.setEndValue(QPoint(400, self.array_widget_grupos[i].y()))
                animacao.start() #inicia a animação
                    
            # [ANIMAÇÃO 2]: empurra os graficos para a esquerda
            print(f"x({self.widget_graphs.x()}) y({self.widget_graphs.y()})") # a coordenada de self.widget_graphs está mudando de alguma forma que desconheço
            self.animacao_graph.setStartValue(QPoint(400, 150))
            self.animacao_graph.setEndValue(QPoint(10, 150))
            self.animacao_graph.start()
            self.widget_graphs.setVisible(True) # torna visivel os graficos na interface pra ver a animação
        else: 
            # [ANIMAÇÃO 3]: puxa os elementos da sidebar pra esquerda (mostrando-os de volta)
            for i, animacao in enumerate(self.animacoes):
                animacao.setStartValue(QPoint(400, self.array_widget_grupos[i].y()))
                animacao.setEndValue(QPoint(0, self.array_widget_grupos[i].y()))  
                animacao.start() #inicia a animação

            # [ANIMAÇÃO 4]: empurra os gráficos pra direita e os destroem em seguida
            self.animacao_graph.setStartValue(QPoint(0, 150))
            self.animacao_graph.setEndValue(QPoint(400, 150))
            self.animacao_graph.start()
            self.animacao_graph.finished.connect(self.destroyGraphs) # destroi os gráficos quando a animação terminar
            
        self.expanded = not self.expanded # alterna pra retroceder da proxima vez

    def destroyGraphs(self):
        self.widget_graphs.setVisible(False) # deixa o widget invisível novamente
        self.layout_principal.removeWidget(self.widget_graphs) # remove o widget do layout_principal pra nao dar bug quando tentar adicionar de novo.
        self.widget_graphs.setParent(None)

        # deleta os widgets do conteiner
        while self.conteiner_graphs.count() > 0:
            item = self.conteiner_graphs.takeAt(0)  # remove o item do layout
            widget = item.widget() # obtem o widget
            if widget is not None and isValid(widget):
                widget.deleteLater()        # deleta o widget
        
        try:
            self.animacao_graph.finished.disconnect(self.destroyGraphs) # desconecta o sinal pra evitar de chamar esse metodo na prmeira interação quando os graficos aparecem
        except:
            pass
        






