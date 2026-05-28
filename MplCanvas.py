from PySide6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys

class MplCanvas(FigureCanvas):
    """Classe wrapper para facilitar o uso"""
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)   # ou  fig.add_subplot(111) para um gráfico simples
        super().__init__(fig)
        self.setParent(parent)
    
    def createGraphs(self):
        self.axes.plot([0,1,2,3,4], [10,5,15,8,12], 'b-o')
        self.axes.set_title("Gráfico Teste")
        self.axes.set_xlabel("Eixo X")
        self.axes.set_ylabel("Eixo Y")
        self.axes.grid(True)
        
        
