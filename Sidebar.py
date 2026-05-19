from PySide6.QtWidgets import (
    QApplication, QLineEdit, QTextEdit, QWidget, QVBoxLayout, QGraphicsView, 
    QGraphicsScene, QGraphicsPathItem, QLabel, QHBoxLayout
)


class Sidebar():
    def __init__(self):
        super().__init__()

        # Painel lateral
        self.info_label = QLabel("Clique em um município...")
        self.info_label.setStyleSheet("padding: 10px; background: #2a2a2a;")

        
        conteiner = QVBoxLayout()#conteiner pra agrupar os elementos

        #atributos da classe
        self.nome = QLineEdit()
        self.mesoregiao = QLineEdit()
        self.torres_totais = QLineEdit()
        self.torres_vivo = QLineEdit()
        self.torres_claro = QLineEdit()
        self.torres_tim = QLineEdit()
        self.obrigacoes_unifique = QLineEdit()
        self.ddd = QLineEdit()
        self.area = QLineEdit()
        self.populacao = QLineEdit()
        self.localidades_sem_conexao = QLineEdit()


        #inserção dos elementos
        conteiner.addWidget(self.nome, stretch=1)





    def setNomeMunicipio(self, nome): # modifica nome do municipio
        self.nome.setText(nome)

    
    def calculoProporcaoAreasConectadas(self):
        total_areas_desconectadas = self.localidades_sem_conexao.displayText()
        total_areas = ...

        percentual = (total_areas_desconectadas / total_areas) * 100
        self.localidades_sem_conexao.setText(str(percentual)+"%")

