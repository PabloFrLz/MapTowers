
"""  
    Subject:    Mapa interativo das torres de telecomunicação presentes no estado do Paraná - 
                mapa desenvolvido para o programa ... Projeto conduzido pela Diretoria
                de Inovação (DIN) a pedido da Diretoria de Relações Institucionais (DRI), diretorias
                vinculadas à Secretaria de Estado da Inovação em Inteligência Artificial (SEIA), do 
                Estado do Paraná.
    Tools: Python3, PySide6, JSON, qdarktheme, photoshop CC 2015/2019
    Author: Pablo Franco Luz (pablo-tr1@hotmail.com - https://github.com/PabloFrLz - 66 992002440)
    Supervisor: André Luis Costa Batistela 
    Director: Thiago Rodrigo da Silva
    Department: Diretoria de Inovação (DIN) 
    Version: 1.0.0.00
    Start: 18/05/2026 - 07:00AM
    Finish: ...
    Modified: ...
    Notes:
        1. 
        2. 
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

import qdarktheme
import json
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QFrame, QGraphicsEllipseItem, QGraphicsOpacityEffect, QGraphicsProxyWidget, QGraphicsRectItem, QGraphicsTextItem, QPushButton, QScrollArea, QStackedLayout, QWidget, QVBoxLayout, QGraphicsView, 
    QGraphicsScene, QGraphicsPathItem, QLabel, QHBoxLayout
)
from PySide6.QtGui import QFont, QIcon, QPainter, QPen, QBrush, QColor, QPolygonF, QTransform
from PySide6.QtCore import QTimer, Qt, QPointF, QRectF
from functools import partial

import SidebarRight, SidebarLeft, Recursos, Ripple, RippleItem

class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(Recursos.NOME_SOFT+" - v."+Recursos.VER)
        self.setFixedSize(Recursos.WIDTH, Recursos.HEIGHT)
        
        self.recursos = Recursos.Recursos()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QHBoxLayout()
        
        #  __________________________
        # |     CRIANDO SIDEBARS     |
        # |__________________________|
        self.sidebar_right = SidebarRight.SidebarRight()
        self.sidebar_left = SidebarLeft.SidebarLeft()

        
        #  ____________________
        # |        MAPA        |
        # |____________________|
        #
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) # comentar caso queira remover a mãozinha do mapa - só que ai perde a função de clicar fora do mapa e arrastar ele pros lados
        #self.view.addScrollBarWidget(scroll, Qt.AlignmentFlag.AlignCenter)

       

        #  __________________________________________________
        # |        ADICIONANDO SIDEBARS E MAPA NA GUI        |
        # |__________________________________________________|
        #
        self.main_layout.addWidget(self.sidebar_left, stretch=0.3) # insere a sidebar da esquerda com uma proporção bem pequena (0.3)

        self.map_container = QWidget()# Container que agrupa o mapa (self.view) e os botões de zoom centralizados
        self.map_layout = QVBoxLayout(self.map_container)
        self.map_layout.setContentsMargins(0, 0, 0, 0)
        self.map_layout.addWidget(self.view, stretch=1)
        # os botões serão adicionados a este container mais abaixo
        self.main_layout.addWidget(self.map_container, stretch=4)
        self.main_layout.addWidget(self.sidebar_right, stretch=1) # insere a sidebar da direita
        layout.addLayout(self.main_layout)
        

        #  _____________________________________________
        # |        OBJETO DE ANIMAÇÃO DAS ONDAS         |
        # |_____________________________________________|
        #self.ondas = Ripple.RippleWidget(self.view, self.width(), self.height()+300)
        #self.ondas.setStyleSheet("background-color: transparent;")
        self.lista_coord_torres = [] # lista de tuplas para armazenar a coordenada das torres de todos os municipios e seu respectivo nome
        self.lista_coord_mun = [] # lista de coordenadas de um municipio especifico que serão animadas
        self.temporizador_ondas = None # timer da animação das ondas
        #self.map_layout.addWidget(self.ondas)
        #self.map_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        

        #  __________________________
        # |     GERANDO O MAPA       |
        # |__________________________|
        municipios = self.carregar_municipios() 
        self.desenhar_mapa(municipios) # desenha os mapas
        self.desenhar_torres() # desenha as torres

        
        

        #  __________________________
        # |       BOTÕES ZOOM        |
        # |__________________________|
        conteiner_buttons = QWidget()
        layout_buttons = QHBoxLayout(conteiner_buttons) #horizontal pois ficaram um do lado do outro
        #button zoom in
        self.btn_zoom_in = QPushButton(self)
        self.icon_btn_zoom_in = QIcon(self.recursos.path_zoom_in)
        self.btn_zoom_in.setIcon(self.icon_btn_zoom_in)
        self.btn_zoom_in.clicked.connect(self.zoom_in)
        # button zoom out
        self.btn_zoom_out = QPushButton(self)
        self.icon_btn_zoom_out = QIcon(self.recursos.path_zoom_out)
        self.btn_zoom_out.setIcon(self.icon_btn_zoom_out)
        self.btn_zoom_out.clicked.connect(self.zoom_out)
        # button pra trocar de thema
        self.btn_theme = QPushButton(self)
        self.icon_btn_off = QIcon(self.recursos.path_button_off)
        self.icon_btn_on = QIcon(self.recursos.path_button_on)
        self.btn_theme.setIcon(self.icon_btn_off)
        self.btn_theme.clicked.connect(self.setTheme)
        self.enable_theme = True # variavel de controle do tema

        # insere os buttons no conteiner e centraliza
        layout_buttons.addWidget(self.btn_zoom_in) 
        layout_buttons.addWidget(self.btn_zoom_out)
        layout_buttons.addWidget(self.btn_theme)
        layout_buttons.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Insere os botões dentro do container do mapa e centraliza horizontalmente
        self.map_container.layout().addWidget(conteiner_buttons, alignment=Qt.AlignmentFlag.AlignHCenter)
        #layout.addLayout(layout_buttons)


        #  ___________________________
        # |       TOGGLE SWITCH       |
        # |___________________________|

        # Toggle Switch customizado via stylesheet para o botão que irá transicionar entre themas da aplicação
        '''
        self.toggle = QCheckBox()
        self.toggle.setCheckable(True)
        self.toggle.setStyleSheet(self.recursos.checkbox_button_edition)
        layout_buttons.addWidget(self.toggle) # vou inserir no layout dos botoes de zoom pra que fique na região própria para botões da interface
        layout_buttons.addStretch() # espreme pra ficar um do lado do outro
        self.toggle.toggled.connect(self.setTheme)
        '''



        #  __________________________
        # |        COPYRIGHT         |
        # |__________________________|

        copyright = QLabel("   © SEIA 2026 — "+Recursos.NOME_SOFT+" "+Recursos.VER+". Todos os direitos reservados.\nSoftware institucional desenvolvido para a Diretoria de Relações Institucionais (DRI).")
        layout.addWidget(copyright, alignment=Qt.AlignmentFlag.AlignCenter)
        copyright.setContentsMargins(0,0,200,0)
        #self.scene.addItem(copyright)

        #  _______________________________
        # |        LEGENDA DO MAPA        |
        # |_______________________________|
        self.widget_legendas =  QFrame(self.view.viewport()) # insere o widget dentro da area do mapa pra ficar por cima dele e não ser afetada pelo zoom
        self.conteiner_legenda = QVBoxLayout(self.widget_legendas) # conteiner lateral pra agrupar um em baixo do outro
        self.conteiner_legenda = self.generateLegenda() # gera a legenda das torres e demais itens futuros do mapa
        #self.map_container.layout().addWidget(self.widget_legendas, alignment=Qt.AlignmentFlag.AlignLeft) # insere a legenda no container do mapa e alinha à esquerda
        self.widget_legendas.move(900, 700)
        self.widget_legendas.setStyleSheet(self.recursos.style_qframe_1)


        #  _______________________________
        # |        TEMPORIZADORES         |
        # |_______________________________|
        # temporizador para criar as ondas de animação no mapa
        self.temporizador_ondas = QTimer(self)
        self.temporizador_ondas.timeout.connect(self.create_another_onda)
        # temporizador das animações de transição suave entre as imagens de fundo das sidebars
        self.temporizador_transicao = QTimer(self)
        self.temporizador_transicao.timeout.connect(self.transitionAnimation)

        # define os efeitos pra possibilitar a animação de transição
        self.efeito = QGraphicsOpacityEffect() # infelizmente nao pode usar o mesmo objeto pra dois objetos ao mesmo tempo
        self.efeito2 = QGraphicsOpacityEffect()
        self.efeito.setOpacity(1.0) # define a opacidade padrão
        self.efeito2.setOpacity(1.0) # define a opacidade padrão
        self.sidebar_right.painel_direito.setGraphicsEffect(self.efeito) # aplica o efeito de opacidade no painel direito da sidebar
        self.sidebar_left.painel_esquerdo.setGraphicsEffect(self.efeito2) # aplica o efeito de opacidade no painel esquerdo da sidebar
        


    def carregar_municipios(self, arquivo: str = Recursos.PATH_MUNICIPIOS) -> List[Dict]: # carrega os dados do arquivo JSON e retorna a lista de municípios
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados["municipios"] # retorna a lista de municípios contida no JSON


    def desenhar_mapa(self, municipios):
        # Cores
        #fill_normal = QColor("#3388ff")
        #fill_inativo = QColor("#555555")
        pen = QPen(QColor("#1a1a1a"), 0.003)
        
        for mun in municipios:
            path_d = mun.get('pathD')
            if not path_d:
                continue
                
            polygon = self.path_d_to_polygon(path_d) # Converter pathD (string) para QPolygonF - converte a string path_d (ex: "M -50.002 -25.004 L -51.009 -23.456 ...") em um QPolygonF — uma lista de pontos (QPointF)
            if polygon.isEmpty(): # caso polígono não tenha pontos válidos
                continue
                
            path_item = QGraphicsPathItem() # Criar item gráfico para o município - necessário se quiser colocar eventos de clique e outras interações - SVGwriter é bem limitado pra esse fim
            path = path_item.path()
            path.addPolygon(polygon)
            path_item.setPath(path)
            # Configurações visuais
            #path_item.setBrush(QBrush(AZUL_PARANA if mun.get('fundo') != "Não" else COR_PADRAO)) # pinta com a cor normal caso o municipio tenha registrado fundos
            path_item.setBrush(QBrush(Recursos.COR_PADRAO)) # cor inicial do mapa
            '''
            # descomentar caso queira implementar cores diferentes dado região do paraná
            if mun.get('regiao') == "curitiba": path_item.setBrush(QBrush(COR_REGIAO_CURITIBA))
            elif mun.get('regiao') == "cascavel": path_item.setBrush(QBrush(COR_REGIAO_CASCAVEL))
            elif mun.get('regiao') == "londrina": path_item.setBrush(QBrush(COR_REGIAO_LONDRINA))
            elif mun.get('regiao') == "ponta-grossa": path_item.setBrush(QBrush(COR_REGIAO_PONTAGROSSA))
            elif mun.get('regiao') == "maringa": path_item.setBrush(QBrush(COR_REGIAO_MARINGA))
            elif mun.get('regiao') == "guarapuava": path_item.setBrush(QBrush(COR_REGIAO_GUARAPUAVA))
            '''
            
            path_item.setPen(pen)
            path_item.setOpacity(0.92)
            # Dados customizados
            dados = ['nome','conselho','conselho_link','fundo','fundo_link','regiao','x','y','pathD']
            for i, dado in enumerate(dados):
                path_item.setData(i, mun[dado])
            
            # Habilitar eventos
            #path_item.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable) # permite que o item (municipio) seja selecionado no cenário
            path_item.setAcceptHoverEvents(True) # para eventos de hover - implementação futura
            # Conectar eventos
            path_item.mousePressEvent = lambda event, item=path_item: self.show_sidebar(item) # ao clicar no município o metodo 'municipio_clicado()' será chamado
            self.scene.addItem(path_item)
        
        # Ajusta a visualização
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        # Inverte Y (porque os dados do IBGE vêm invertidos)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.view.scale(1, -1)   # Inverte verticalmente

    def path_d_to_polygon(self, path_d: str) -> QPolygonF:
        """Converte string 'M x y L x y ...' para QPolygonF"""
        polygon = QPolygonF()
        numbers = [float(n) for n in path_d.replace('M', '').replace('L', '').replace('Z', '').split()]
        
        for i in range(0, len(numbers), 2):
            if i + 1 < len(numbers):
                polygon.append(QPointF(numbers[i], numbers[i + 1]))
        return polygon

    
    def show_sidebar(self, item: QGraphicsPathItem): 
        if self.temporizador_ondas is not None:
            self.temporizador_ondas.stop() # interrompe o timer parando o loop das animações atuais
            self.lista_coord_mun.clear() # limpa a lista 

        if not self.sidebar_right.enable_graphs: # para corrigir um bug onde ao clicar no mapa com a barra escondida ela retrocedia pra uma posição incorreta
            self.sidebar_right.btn_graficos.setIcon(self.sidebar_right.btn_graficos_icon_hide) # altera imagem do ícone para escondido 'hide'
            self.sidebar_right.transitToGraphs()
            self.sidebar_right.enable_graphs = not self.sidebar_right.enable_graphs # inverte
        
        # ideentifica o municipio
        self.municipio = item.data(0)
        self.regiao = item.data(5) # desnecessário pra logica desse método mas necessário pra tooltip que surgirá no mapa
        dados_municipio = self.getDataFromJSON(self.municipio) # busca os dados do municipio
        # atualiza valores dos dados nas sidebars 
        for i, indice_dados in enumerate(self.recursos.indice_dados): 
            self.sidebar_right.setAtributo(indice_dados, dados_municipio.get(indice_dados))
            self.sidebar_left.setAtributo(indice_dados, dados_municipio.get(indice_dados))
            # stay here!
        
        self.hoverEnterEvent() # mostra o tooltip do municipio

        # trecho de destaque ao município clicado
        for it in self.scene.items():
            if isinstance(it, QGraphicsPathItem):
                it.setBrush(QBrush(Recursos.COR_PADRAO_2 if it != item else Recursos.AZUL_PARANA))
                if it != item:
                    # atualiza o nome da cidade na sidebar esquerda
                    self.sidebar_left.set_brasao_municipio(self.municipio, "Parana.png")

            #elif isinstance(it, QWidget):
            #    it.setBrush(QBrush(QColor("#3f4e54") if it != item else QColor("#0069b4")))
        
        # trecho relativo as animações de ondas na tela
        for torre in self.lista_coord_torres:
            if (torre[0] == self.municipio): # só vai animar as torres do municipio selecionado no mapa
                self.lista_coord_mun.append(QPointF(torre[1].x(), torre[1].y())) # insere as coord. das torres do municipio para serem animadas
        
        #cria um timer pra ficar colocando a animação em loop
        self.temporizador_ondas.start(800)  # nova onda a cada 800ms
        

    def getDataFromJSON(self, municipio):
        lista_mun = self.carregar_municipios(Recursos.PATH_DADOS) 

        for mun in lista_mun:
            nome_municipio = mun.get('NM_MUN')
            if nome_municipio == municipio:
                print(f"[MapTorres.py]: Dados do municipio '{nome_municipio}' encontrado.")
                return mun
    
    def wheelEvent(self, event):
        # Zoom com roda do mouse
        fator = 1.15 if event.angleDelta().y() > 0 else 0.85
        self.view.scale(fator, fator)

    def zoom_in(self): # ação do icone zoom_in para dar zoom no mapa
        fator = 1.15
        self.view.scale(fator, fator)

    def zoom_out(self): # ação do icone zoom_out para retroceder o zoom no mapa
        fator = 0.85
        self.view.scale(fator, fator)

    def desenhar_torres(self): 
        #obtem os dados das torres via arquivo.json informado
        lista_mun = self.carregar_municipios("torres_location.json") 
        for mun in lista_mun:
            #print(mun.get('Longitude'))
            coord_x = float(mun.get('Longitude')) # extrai as coordenadas
            coord_y = float(mun.get('Latitude'))
            ellipse = QGraphicsEllipseItem(0, 0, Recursos.TAM_CIRCLE_TORRE, Recursos.TAM_CIRCLE_TORRE) # cria uma elipse/circulo pra representar as torres
            ellipse.setPos(coord_x, coord_y) # posiciona a torre na interface

            status = mun.get('Status') # vê qual o status da torre atual pra pintá-la de acordo no mapa
            if(status == "Em Andamento"):
                cor = Recursos.COR_TORRE_ANDAMENTO
            elif(status == "ATIVO"):
                cor = Recursos.COR_TORRE_ATIVA
            else:
                cor = Recursos.COR_TORRE_NORMAL
            ellipse.setBrush(QBrush(cor)) # cor interna dos circulos
            ellipse.setPen(QPen(QColor("#000000"), Recursos.BORDAS_CIRCLE_TORRE)) # cor das bordas dos circulos
            self.scene.addItem(ellipse) # insere no cenario

            self.lista_coord_torres.append([mun.get('Município'), QPointF(coord_x, coord_y)]) # salva uma tupla com o nome do municipio e as coordenadas xy da torre inserida na GUI        

    #evento ativado automaticamente quando passar o mouse sobre um municipio              
    def hoverEnterEvent(self):
        #tooltip com informações básicas
        self.setToolTip(f"""
            Município: <b>{self.municipio}</b><br>
            Região: {self.regiao}<br>
        """)
        self.setStyleSheet(self.recursos.tooltips)
        

    # metodo para debug via click de mouse kkk
    def mousePressEvent(self, event):

        
        return super().mousePressEvent(event)
    
    def create_another_onda(self):
        for coord in self.lista_coord_mun:
            ripple = RippleItem.RippleItem(coord.x(), coord.y(), max_radius=0.5, speed=0.02)
            self.scene.addItem(ripple)
    

    def setTheme(self):
        if self.enable_theme:
            self.btn_theme.setIcon(self.icon_btn_on) # altera imagem do ícone para on
            self.sidebar_left.painel_esquerdo.setStyleSheet(self.recursos.style_theme_2_aux)
            self.sidebar_right.painel_direito.setStyleSheet(self.recursos.style_theme_2)
            self.sidebar_right.background.setPixmap(self.sidebar_right.image_2) # define a 2ª imagem como padrão
            #self.sidebar_right.btn_graficos.setStyleSheet(self.recursos.buttons_style)
            #self.sidebar_right.btn_animation.setStyleSheet(self.recursos.buttons_style)
            
            # inicia a animação de transição suave
            self.efeito.setOpacity(Recursos.CONST_OPACITY_SPEED) #define a opacidade inicial em preparação pra animação de transição suave
            self.efeito2.setOpacity(Recursos.CONST_OPACITY_SPEED) 
            self.temporizador_transicao.start(Recursos.CONST_UPDATE_MS) # 30ms para criar um efeito de transição suave entre as imagens de fundo
            
        else:
            self.btn_theme.setIcon(self.icon_btn_off) # altera imagem do ícone para off
            self.sidebar_left.painel_esquerdo.setStyleSheet(self.recursos.style_theme_1_aux)
            self.sidebar_right.painel_direito.setStyleSheet(self.recursos.style_theme_1)
            self.sidebar_right.background.setPixmap(self.sidebar_right.image_1) # define a 1ª imagem como padrão
            #self.sidebar_right.btn_graficos.setStyleSheet(self.recursos.buttons_style)
            #self.sidebar_right.btn_animation.setStyleSheet(self.recursos.buttons_style)

            # inicia a animação de transição suave
            self.efeito.setOpacity(Recursos.CONST_OPACITY_SPEED) #define a opacidade inicial em preparação pra animação de transição suave
            self.efeito2.setOpacity(Recursos.CONST_OPACITY_SPEED) 
            self.temporizador_transicao.start(Recursos.CONST_UPDATE_MS) # 30ms para criar um efeito de transição suave entre as imagens de fundo

        self.enable_theme = not self.enable_theme # inverte

    # metodo reciclado do outro projeto SEIAParkingManagement
    def generateLegenda(self): # gera a legenda das cores pra se orientar melhor
        #self.legendas = QVBoxLayout() # conteiner lateral pra agrupar um em baixo do outro
        self.legendas = []
        descricao = ["Torres inativas - em andamento", 
                  "Torres ativas"]
        pen = [Recursos.COR_TORRE_ANDAMENTO, Recursos.COR_TORRE_ATIVA]
        brush = [Recursos.COR_TORRE_ANDAMENTO, Recursos.COR_TORRE_ATIVA]

        #conteiner = QVBoxLayout() # conteiner lateral pra agrupar um em baixo do outro

        for i in range(2):
            linha = QHBoxLayout()

            quadrado = QFrame()
            quadrado.setFixedSize(15, 10)
            quadrado.setStyleSheet(f"""
                background-color: {brush[i].name()};
                border: 1px solid black;
            """)
            texto = QLabel(descricao[i])
            linha.addWidget(quadrado)
            linha.addWidget(texto)
            self.conteiner_legenda.addLayout(linha)

    def transitionAnimation(self):
        opacidade_atual = self.efeito.opacity() # obtem a opacidade atual
        opacidade_atual_2 = self.efeito2.opacity() # obtem a opacidade atual do segundo efeito
        if opacidade_atual >= 1.0 and opacidade_atual_2 >= 1.0:
            self.temporizador_transicao.stop() # para o timer quando a opacidade atingir 1.0 (totalmente visível)
        else:
            if opacidade_atual < 1.0: # evita soma além de 1.0 que pode causar bug visual
                self.efeito.setOpacity(opacidade_atual + Recursos.CONST_OPACITY_SPEED) # soma a opacidade atual mais a constante de velocidade da animação que normalmente é um valor bem baixo (0.01)
            if opacidade_atual_2 < 1.0:
                self.efeito2.setOpacity(opacidade_atual_2 + Recursos.CONST_OPACITY_SPEED) # soma a opacidade atual mais a constante de velocidade da animação que normalmente é um valor bem baixo (0.01)


        '''
        opacidade_atual = self.sidebar_right.painel_direito.windowOpacity() # obtem a opacidade atual
        print(f"why am i not here ???? {opacidade_atual}")
        if opacidade_atual >= 1.0:
            self.temporizador_transicao.stop() # para o timer quando a opacidade atingir 1.0 (totalmente visível)
        else:
            self.sidebar_right.painel_direito.setWindowOpacity(opacidade_atual + Recursos.CONST_OPACITY_SPEED) # soma a opacidade atual mais a constante de velocidade da animação que normalmente é um valor bem baixo (0.01) 
        '''


            

# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    window = MapWindow()
    window.show()
    #adicionando uma scrollbar pra corrigir o problema de limitação da tela de 1600x900p
    '''
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(window)
    scroll.setFixedSize(WIDTH, HEIGHT)
    scroll.show() # mostra a janela da aplicação
    '''
    sys.exit(app.exec())