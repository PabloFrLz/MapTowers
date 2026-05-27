
"""  
    Subject:    Mapa interativo das torres de telecomunicação presentes no estado do Paraná - 
                mapa desenvolvido para o programa {nome_do_programa}. Projeto conduzido pela Diretoria
                de Inovação (DIN) a pedido da Diretoria de Relações Institucionais (DRI), diretorias
                vinculadas à Secretaria de Estado da Inovação em Inteligência Artificial (SEIA), do 
                Estado do Paraná.
    Tools: Python3, PySide6, JSON, qdarktheme, photoshop CC 2015/2019
    Author: Pablo Franco Luz (pablo-tr1@hotmail.com - https://github.com/PabloFrLz)
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
    QApplication, QCheckBox, QGraphicsEllipseItem, QGraphicsProxyWidget, QGraphicsTextItem, QPushButton, QScrollArea, QWidget, QVBoxLayout, QGraphicsView, 
    QGraphicsScene, QGraphicsPathItem, QLabel, QHBoxLayout
)
from PySide6.QtGui import QFont, QIcon, QPainter, QPen, QBrush, QColor, QPolygonF
from PySide6.QtCore import Qt, QPointF, QRectF

import SidebarRight, SidebarLeft, Recursos

WIDTH = 1600
HEIGHT = 900
NOME_SOFT = "GeoTorres Connect Paraná"
VER = "1.0.0.01"
PATH_DADOS = "dados.json" # dados da DRI
PATH_MUNICIPIOS = "municipios.json" # dados próprios usados pra desenhar os mapas - possui todos os vertices dos municipios do paraná
COR_PADRAO = QColor("#555555")
COR_PADRAO_2 = QColor("#3f4e54")
AZUL_PARANA = QColor("#3388ff")
VERDE_PARANA = QColor("#008b3b")
COR_TORRES = QColor("#d80000")

#CORES PARA REGIÕES:
COR_REGIAO_CURITIBA = QColor("#555555")
COR_REGIAO_CASCAVEL = QColor("#474747")
COR_REGIAO_PONTAGROSSA = QColor("#383838")
COR_REGIAO_LONDRINA = QColor("#252525")
COR_REGIAO_MARINGA = QColor("#1D1D1D")
COR_REGIAO_GUARAPUAVA = QColor("#141414")


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(NOME_SOFT+" - v."+VER)
        self.setFixedSize(WIDTH, HEIGHT)
        
        self.recursos = Recursos.Recursos()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        #  __________________________
        # |     CRIANDO SIDEBARS     |
        # |__________________________|
        self.sidebar_right = SidebarRight.SidebarRight()
        self.sidebar_left = SidebarLeft.SidebarLeft()
        
        # Mapa
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) # comentar caso queira remover a mãozinha do mapa - só que ai perde a função de clicar fora do mapa e arrastar ele pros lados
        #self.view.addScrollBarWidget(scroll, Qt.AlignmentFlag.AlignCenter)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.sidebar_left, stretch=0.3) # insere a sidebar da esquerda com uma proporção bem pequena (0.3)

        self.map_container = QWidget()# Container que agrupa o mapa (self.view) e os botões de zoom centralizados
        map_layout = QVBoxLayout(self.map_container)
        map_layout.setContentsMargins(0, 0, 0, 0)
        map_layout.addWidget(self.view, stretch=1)
        # os botões serão adicionados a este container mais abaixo
        self.main_layout.addWidget(self.map_container, stretch=4)
        self.main_layout.addWidget(self.sidebar_right, stretch=1) # insere a sidebar da direita
        layout.addLayout(self.main_layout)

        #  __________________________
        # |     GERANDO O MAPA       |
        # |__________________________|
        municipios = self.carregar_municipios() 
        self.desenhar_mapa(municipios) # desenha os mapas
        self.desenhar_torres() # desenha as torres


        # insere as sidebars no cenário
        """
        proxy_right = QGraphicsProxyWidget()
        proxy_right.setWidget(self.sidebar_right)
        self.scene.addItem(proxy_right) 

        proxy_left = QGraphicsProxyWidget()
        proxy_left.setWidget(self.sidebar_left)
        self.scene.addItem(proxy_left)
        """

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

        copyright = QLabel("   © SEIA 2026 — "+NOME_SOFT+" "+VER+". Todos os direitos reservados.\nSoftware institucional desenvolvido para a Diretoria de Relações Institucionais (DRI).")
        #copyright.setFont(QFont("Arial", 8))
        #copyright.setDefaultTextColor(QColor("white"))
        #copyright.setPos(WIDTH-200, HEIGHT-30)
        layout.addWidget(copyright, alignment=Qt.AlignmentFlag.AlignCenter)
        copyright.setContentsMargins(0,0,200,0)
        #self.scene.addItem(copyright)

        '''proxy_button = QGraphicsProxyWidget()
        proxy_button.setWidget(conteiner_buttons)
        proxy_button.setPos(100, 100)
        proxy_button.

        self.scene.addItem(proxy_button)
        #layout.addLayout(conteiner_zoom_buttons)'''


        


    def carregar_municipios(self, arquivo: str = PATH_MUNICIPIOS) -> List[Dict]: # carrega os dados do arquivo JSON e retorna a lista de municípios
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
            path_item.setBrush(QBrush(COR_PADRAO)) # cor inicial do mapa
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
        # Exemplo: destacar município clicado
        for it in self.scene.items():
            if isinstance(it, QGraphicsPathItem):
                it.setBrush(QBrush(COR_PADRAO_2 if it != item else VERDE_PARANA))
                if it != item:
                    # atualiza o nome da cidade na sidebar esquerda
                    self.sidebar_left.set_brasao_municipio(self.municipio, "Parana.png")

            #elif isinstance(it, QWidget):
            #    it.setBrush(QBrush(QColor("#3f4e54") if it != item else QColor("#0069b4")))

    def getDataFromJSON(self, municipio):
        lista_mun = self.carregar_municipios(PATH_DADOS) 

        for mun in lista_mun:
            nome_municipio = mun.get('NM_MUN')
            if nome_municipio == municipio:
                print(f"Dados do municipio '{nome_municipio}' encontrado.")
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
        lista_mun = self.carregar_municipios("dados.json") 

        for mun in lista_mun:
            coord_x = float(mun.get('Longitude')) # extrai as coordenadas
            coord_y = float(mun.get('Latitude'))
            ellipse = QGraphicsEllipseItem(coord_x, coord_y, 0.02, 0.02) # cria uma elipse/circulo pra representar as torres
            ellipse.setBrush(QBrush(COR_TORRES)) # cor interna dos circulos
            ellipse.setPen(QPen(QColor("#000000"), 0.005)) # cor das bordas dos circulos
            self.scene.addItem(ellipse) # insere no cenario

    #evento ativado automaticamente quando passar o mouse sobre um municipio              
    def hoverEnterEvent(self):
        #tooltip com informações básicas
        self.setToolTip(f"""
            Município: <b>{self.municipio}</b><br>
            Região: {self.regiao}<br>
        """)
        self.setStyleSheet(self.recursos.tooltips)
    
    
    def setTheme(self):
        if self.enable_theme:
            self.btn_theme.setIcon(self.icon_btn_on) # altera imagem do ícone para on
            self.sidebar_left.painel_esquerdo.setStyleSheet(self.recursos.style_theme_2_aux)
            self.sidebar_right.painel_direito.setStyleSheet(self.recursos.style_theme_2)
            
        else:
            self.btn_theme.setIcon(self.icon_btn_off) # altera imagem do ícone para off
            self.sidebar_left.painel_esquerdo.setStyleSheet(self.recursos.style_theme_1_aux)
            self.sidebar_right.painel_direito.setStyleSheet(self.recursos.style_theme_1)
        
        self.enable_theme = not self.enable_theme # inverte

        

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