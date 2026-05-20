
"""  
    Subject:    Mapa interativo do estado do Paraná, desenvolvido para o programa 
                Vale das Araucárias, projeto conduzido pelo núcleo de Diretoria em 
                Inovação (DIN), vinculado à Secretaria de Estado da Inovação em Inteligência 
                Artificial (SEIA), do Estado do Paraná.
    Tools: SVG, JSON, Python3, PySide6
    Author: Pablo Franco Luz (pablo-tr1@hotmail.com - https://github.com/PabloFrLz)
    Supervisor: André Luis Costa Batistela 
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
    QApplication, QGraphicsProxyWidget, QWidget, QVBoxLayout, QGraphicsView, 
    QGraphicsScene, QGraphicsPathItem, QLabel, QHBoxLayout
)
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF
from PySide6.QtCore import Qt, QPointF, QRectF

import Sidebar


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MapTorres - DRI - v1.0.0.00")
        self.resize(1600, 850)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # criando a sidebar
        self.sidebar = Sidebar.Sidebar()
        
        # Mapa
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.view, stretch=4)
        self.main_layout.addWidget(self.sidebar, stretch=1) # insere a sidebar no conteiner horizontal 
        
        layout.addLayout(self.main_layout)
        
        municipios = self.carregar_municipios() 
        self.desenhar_mapa(municipios) # desenha os mapas

        # insere a sidebar no cenário
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.sidebar)
        self.scene.addItem(proxy) 

    def carregar_municipios(self, arquivo: str = "mun.json") -> List[Dict]: # carrega os dados do arquivo JSON e retorna a lista de municípios
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados["municipios"] # retorna a lista de municípios contida no JSON

    def desenhar_mapa(self, municipios):
        # Cores
        fill_normal = QColor("#3388ff")
        fill_inativo = QColor("#555555")
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
            path_item.setBrush(QBrush(fill_normal if mun.get('fundo') != "Não" else fill_inativo)) # pinta com a cor normal caso o municipio tenha registrado fundos
            path_item.setPen(pen)
            path_item.setOpacity(0.92)
            # Dados customizados
            #dados = ['nome', 'vivo', 'tim', 'claro', 'total_torres', 'area_total', 'populacao', 'regiao']
            #dados = ['nome','conselho','conselho_link','fundo','fundo_link','regiao','x','y','pathD']
            '''
            dados = ["fid","CD_MUN","NM_MUN","UF","Latitude","Longitude","AREA_KM2", "Dados_fid",
                     "Dados_NM_MUN","Dados_AREA_KM2","Dados_areaqgis","Dados_dados conec pr_NM_MUN_2",
                     "Dados_dados conec pr_AREA_KM2_2","Dados_dados conec pr_areaconec",
                     "Dados_dados conec pr_percentualconec","Dados_Torres_claro","Dados_Torres_vivo",
                     "Dados_Torres_tim","Dados_rede_estadual_ensino","Dados_rede_mun_ensino",
                     "Dados_locs_sem_conec","Dados_obgs_unifique","Dados_DDD","area_urbana_areaurbana",
                     "area_rural_arearural","pop_total_mun"]
            '''
            for i, dado in enumerate(self.sidebar.nome_atributos):
                #path_item.setData(0, mun['nome'])
                path_item.setData(i, mun[dado])
            
            
            #path_item.setData(1, mun.get('codigo', '')) # Código se tiver
            # Habilitar eventos
            path_item.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable) # permite que o item (municipio) seja selecionado no cenário
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
        #nome = item.data(0)
        #print(f"✅ Clicou em: {nome}")

        for i, nome_atributo in enumerate(self.sidebar.nome_atributos): # atualiza valores dos dados
            self.sidebar.setAtributo(nome_atributo, item.data(i))

        """
        background: qlineargradient(
            x1:0, y1:0,
            x2:0, y2:1,
            stop:0 #111,
            stop:1 #222
        );
        """


        """
        background: qlineargradient(
            x1:0, y1:0,
            x2:1, y2:0,
            stop:0 #0b0b0b,
            stop:0.5 #1b1b1b,
            stop:1 #2a2a2a
        );
        """
        # criando o conteiner pra agrupar os elementos da sidebar
        '''glow = QWidget(self)
        glow.setStyleSheet("""
            background: rgba(255,255,255,15);
            border-radius: 20px;
        """)
        self.info_label.setText(f"<h3>{nome}</h3><p>Clique registrado!</p>")
        self.main_layout.addWidget(glow)'''
        
        # Exemplo: destacar município clicado
        for it in self.scene.items():
            if isinstance(it, QGraphicsPathItem):
                it.setBrush(QBrush(QColor("#3f4e54") if it != item else QColor("#008b3b")))
            #elif isinstance(it, QWidget):
            #    it.setBrush(QBrush(QColor("#3f4e54") if it != item else QColor("#0069b4")))

# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    window = MapWindow()
    window.show()
    sys.exit(app.exec())