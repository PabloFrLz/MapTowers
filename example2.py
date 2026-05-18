import sys
from pathlib import Path
from typing import List, Dict, Any

import qdarktheme
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGraphicsView, 
    QGraphicsScene, QGraphicsPathItem, QLabel, QHBoxLayout
)
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF
from PySide6.QtCore import Qt, QPointF, QRectF


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MapTorres - DRI - v1.0.0.00")
        self.resize(1600, 850)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Painel lateral (opcional)
        self.info_label = QLabel("Clique em um município...")
        self.info_label.setStyleSheet("padding: 10px; background: #2a2a2a;")

        # Mapa
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.view, stretch=4)
        main_layout.addWidget(self.info_label, stretch=1)
        
        layout.addLayout(main_layout)
        
        municipios = self.carregar_municipios()
        self.desenhar_mapa(municipios)

    def carregar_municipios(self, arquivo: str = "municipios.json") -> List[Dict]:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados["municipios"]

    def desenhar_mapa(self, municipios):
        # Cores
        fill_normal = QColor("#3388ff")
        fill_inativo = QColor("#555555")
        pen = QPen(QColor("#1a1a1a"), 0.003)
        
        for mun in municipios:
            path_d = mun.get('pathD')
            if not path_d:
                continue
                
            # Converter pathD (string) para QPolygonF
            polygon = self.path_d_to_polygon(path_d)
            
            if polygon.isEmpty():
                continue
                
            path_item = QGraphicsPathItem()
            path = path_item.path()
            path.addPolygon(polygon)
            path_item.setPath(path)
            
            # Configurações visuais
            path_item.setBrush(QBrush(fill_normal if mun.get('fundo') != "Não" else fill_inativo))
            path_item.setPen(pen)
            path_item.setOpacity(0.92)
            
            # Dados customizados
            path_item.setData(0, mun['nome'])           # Nome
            path_item.setData(1, mun.get('codigo', '')) # Código se tiver
            
            # Habilitar eventos
            path_item.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
            path_item.setAcceptHoverEvents(True)
            
            # Conectar eventos
            path_item.mousePressEvent = lambda event, item=path_item: self.municipio_clicado(item)
            
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

    def municipio_clicado(self, item: QGraphicsPathItem):
        nome = item.data(0)
        print(f"✅ Clicou em: {nome}")
        self.info_label.setText(f"<h3>{nome}</h3><p>Clique registrado!</p>")
        
        # Exemplo: destacar município clicado
        for it in self.scene.items():
            if isinstance(it, QGraphicsPathItem):
                it.setBrush(QBrush(QColor("#3388ff") if it != item else QColor("#ffcc00")))

# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    window = MapWindow()
    window.show()
    sys.exit(app.exec())