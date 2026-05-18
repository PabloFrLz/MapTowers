import sys
from pathlib import Path
from typing import List, Dict, Any

import qdarktheme
import svgwrite
import json
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QUrl, QByteArray


WIDTH = 1600
HEIGHT = 850
WIDTH_MAP = 980
HEIGHT_MAP = 630
ver = "v1.0.0.00"


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MapTorres - DRI - " + ver)
        self.resize(WIDTH, HEIGHT)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        municipios = self.carregar_municipios()
        html_content = self.create_interactive_map(municipios)
        
        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(WIDTH_MAP, HEIGHT_MAP)
        self.web_view.setHtml(html_content)
        
        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def carregar_municipios(self, arquivo: str = "municipios.json") -> List[Dict[str, Any]]:
        caminho = Path(arquivo)
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo {arquivo} não encontrado!")
        
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados["municipios"]

    def create_interactive_map(self, municipios):
        dwg = svgwrite.Drawing(size=(f"{WIDTH_MAP}px", f"{HEIGHT_MAP}px"), profile='full', debug=False)
        dwg.viewbox(-55.00, -24.60, 7.28, 5.5)
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='#1e1e1e'))
        
        for mun in municipios:
            path_d = mun.get('pathD')
            if not path_d:
                continue
                
            nome = mun['nome']
            
            path = dwg.path(
                d=path_d,
                fill="#3388ff" if mun.get('fundo') != "Não" else "#555555",
                opacity="0.9",
                transform="scale(1, -1) translate(0, 46.6)",
                data_nome=nome,
            )
            path.set_desc(title=nome)
            dwg.add(path)
        
        svg_string = dwg.tostring()
        
        # HTML completo com JavaScript
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ margin:0; padding:0; background:#1e1e1e; }}
                svg {{ width:100%; height:100%; }}
                path {{ cursor: pointer; transition: fill 0.2s; }}
                path:hover {{ fill: #ffcc00 !important; opacity: 1; }}
            </style>
        </head>
        <body>
            {svg_string}
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    document.querySelectorAll('path').forEach(path => {{
                        path.addEventListener('click', function() {{
                            const nome = this.getAttribute('nome');
                            
                            // Chama função Python
                            window.location.href = `python://click?nome=${{encodeURIComponent(nome)}}`;
                        }});
                    }});
                }});
            </script>
        </body>
        </html>
        """
        return html

    # Função que vai receber o clique (via QWebEngineView)
    def handle_click(self, nome: str, codigo: str = None):
        print(f"✅ Clicou em: {nome} (Código: {codigo})")
        # Aqui você pode abrir janela, mudar cor, etc.


# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    window = MapWindow()
    window.show()
    sys.exit(app.exec())