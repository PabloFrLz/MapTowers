from PySide6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys

class MplCanvas(FigureCanvas):
    """Classe wrapper para facilitar o uso"""
    def __init__(self, parent=None, width=6, height=4, dpi=50): #dpi é a proporção geral das letras e das informações do mapa - quanto menor, menor será o gráfico desenhado
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('none')      # Fundo da figura transparente
        fig.patch.set_alpha(0.0)

        self.axes = fig.add_subplot(111)   # ou  fig.add_subplot(111) para um gráfico simples
        self.axes.patch.set_facecolor('none')  # Fundo dos eixos transparente
        self.axes.patch.set_alpha(0.0)

        super().__init__(fig)
        self.setParent(parent)
        #plt.style.use('ggplot') # aplica um thema diferente
        
    
    def createGraphs(self):
        self.axes.plot([0,1,2,3,4], [10,5,15,8,12], 'c-o', linewidth=2)
        self.axes.set_title("Gráfico Teste", color='white')
        self.axes.set_xlabel("Eixo X", color='white')
        self.axes.set_ylabel("Eixo Y", color='white')
        self.axes.grid(True, color = 'gray', alpha=0.1)
        self.axes.tick_params(colors='white')
        print("Gráfico gerado!")
        
        

