import sys
from pathlib import Path
from typing import List, Dict, Any

import qdarktheme
import svgwrite
import json
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QByteArray


WIDTH=1600
HEIGHT=850
WIDTH_MAP=980
HEIGHT_MAP=630
ver = "v1.0.0.00"

class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MapTorres - DRI - "+ver)
        self.resize(WIDTH, HEIGHT)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Carrega os dados
        municipios = self.carregar_municipios()
        
        # Cria o SVG
        svg_data = self.create_map_svg(municipios)
        
        # Cria o widget SVG
        self.svg_widget = QSvgWidget()
        self.svg_widget.load(QByteArray(svg_data))
        self.svg_widget.setFixedSize(WIDTH_MAP, HEIGHT_MAP)
        layout.addWidget(self.svg_widget)

        self.svg_widget.mousePressEvent = self.clickEvent

        self.setLayout(layout)

    def carregar_municipios(self, arquivo: str = "municipios.json") -> List[Dict[str, Any]]:
        caminho = Path(arquivo)
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo {arquivo} não encontrado!")
        
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        municipios = dados["municipios"]
        
        print(f"✅ Total de municípios carregados: {len(municipios)}")
        
        # Debug dos primeiros 3
        '''
        for i, mun in enumerate(municipios[:3]):
            path = mun.get('pathD', '')
            print(f"Município {i+1}: {mun.get('nome')} | pathD existe: {bool(path)} | Tamanho pathD: {len(path)} caracteres")
            if len(path) > 50:
                print(f"   Primeiros 80 chars: {path[:80]}...")
        '''
        return municipios


    def create_map_svg(self, municipios):
        dwg = svgwrite.Drawing(size=(f"{WIDTH_MAP}px", f"{HEIGHT_MAP}px"), profile='full')
        dwg.viewbox(-55.00, -24.60, 7.28, 5.5)   # ajuste da viewbox pra pegar a região do mapa que é minuscula (dados IBGE)
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='#1e1e1e'))
        
        print(f"Criando SVG com {len(municipios)} municípios...")
        
        for mun in municipios:
            path_d = mun.get('pathD')
            if not path_d:
                print(f"⚠️  {mun.get('nome')} não tem 'pathD'!")
                continue
                
            try:
                path = dwg.path(
                    d=path_d,
                    fill="#3388ff" if mun.get('fundo') != "Não" else "#555555",
                    #stroke="#222222",
                    #stroke_width=1.5,
                    opacity=0.9,
                    transform="scale(1, -1) translate(0, 46.6)", #trecho necessario pra inverter o mapa e deixá-lo na posição correta (dados IBGE)
                    onclick=f"python://click?nome=${mun.get('nome')}"
                )
                path.set_desc(title=mun['nome'])
                dwg.add(path)
            except Exception as e:
                print(f"❌ Erro ao criar path para {mun.get('nome')}: {e}")
                
        svg_string = dwg.tostring()
        print(f"✅ SVG gerado com {svg_string.count('<path')} elementos <path>")
        
        #gerando arquivo.svg para debug posterior caso necessário
        name_map_svg = "mapa_debug.svg"
        with open(name_map_svg, "w", encoding="utf-8") as f:
            f.write(dwg.tostring())
        print(f"SVG salvo como {name_map_svg}")
        
        return svg_string.encode('utf-8')
    
    def clickEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        print(f"Clique em: {x}, {y}")
        # Aqui você converte para coordenadas do SVG e identifica o município

    
        


# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    window = MapWindow()
    window.show()
    sys.exit(app.exec())