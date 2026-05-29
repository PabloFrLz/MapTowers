from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
import sys


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        
        # === Configuração de transparência ===
        fig.patch.set_facecolor('none')      # Fundo da figura transparente
        fig.patch.set_alpha(0.0)
        
        self.axes = fig.add_subplot(111)
        self.axes.patch.set_facecolor('none')  # Fundo dos eixos transparente
        self.axes.patch.set_alpha(0.0)
        
        super().__init__(fig)
        self.setParent(parent)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráfico com Fundo Transparente")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Opcional: deixar o fundo da janela com cor para ver o efeito
        central_widget.setStyleSheet("background-color: #2b2b2b;")  # fundo escuro

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.canvas = MplCanvas(self, width=9, height=6, dpi=100)

        # Exemplo de gráfico
        self.canvas.axes.plot([0, 1, 2, 3, 4], [10, 5, 15, 8, 12], 'c-o', linewidth=2)
        self.canvas.axes.set_title('Gráfico com Fundo Transparente', color='white')
        self.canvas.axes.set_xlabel('Eixo X', color='white')
        self.canvas.axes.set_ylabel('Eixo Y', color='white')
        self.canvas.axes.grid(True, color='gray', alpha=0.3)
        
        # Deixar os textos dos ticks brancos
        self.canvas.axes.tick_params(colors='white')

        layout.addWidget(self.canvas)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 600)
    window.show()
    sys.exit(app.exec())