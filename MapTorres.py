import sys
from pathlib import Path
from typing import List, Dict, Any

import qdarktheme
import svgwrite
import json
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QByteArray


def carregar_municipios(arquivo: str = "municipios.json") -> List[Dict[str, Any]]:
    caminho = Path(arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo {arquivo} não encontrado!")
    
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    return dados["municipios"]


def create_map_svg(municipios, width=900, height=700):
    dwg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"), profile='full')
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='#1e1e1e'))
    
    for mun in municipios:
        path = dwg.path(
            d=mun['pathD'],
            fill="#3388ff" if mun.get('fundo') != "Não" else "#555555",
            stroke="#222222",
            stroke_width=1.5,
            opacity=0.9
        )
        
        # Tooltip
        path.set_desc(title=mun['nome'])
        
        # Atributos customizados (data-*) - forma correta no svgwrite
        path.attrib['data-nome'] = mun['nome']
        if mun.get('regiao'):
            path.attrib['data-regiao'] = mun.get('regiao')

        dwg.add(path)
    
    return dwg.tostring().encode('utf-8')


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Torres DRI - v1.0.0.00")
        self.resize(900, 700)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Carrega os dados
        municipios = carregar_municipios()
        
        # Cria o SVG
        svg_data = create_map_svg(municipios)
        
        # Cria o widget SVG
        self.svg_widget = QSvgWidget()
        self.svg_widget.load(QByteArray(svg_data))
        self.svg_widget.setMinimumSize(900, 700)
        
        layout.addWidget(self.svg_widget)


# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    window = MapWindow()
    window.show()
    sys.exit(app.exec())