from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLayout, QLineEdit, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtGui import QIcon, QPixmap, Qt

import Recursos

class SidebarRight(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recursos = Recursos.Recursos()
        #dados selecionados para mostrar na interface 
        self.expanded = True
        self.setup_ui()     # Monta layout e widgets da sidebar da direita
        self.apply_styles()        # QSS separado
        #self.setup_animations()   # QPropertyAnimation para largura
        #self.setup_connections()


    def setup_ui(self):
        # 1. Container principal (QFrame semi-transparente)
        self.painel_direito = QFrame(self)
        self.painel_direito.setObjectName("painel_direito")
        #self.painel_direito.setFixedWidth(310)
        self.painel_direito.setContentsMargins(0, -6, 0, 0)

        #conteiner vertical pra agrupar os elementos textuais
        self.layout_principal = QVBoxLayout() 
        self.background = QLabel()# background de topo da sidebar da esquerda
        self.background.setPixmap(QPixmap("imagens/logo_seia_sidebar_full.png").scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)) 
        self.background.setFixedWidth(280) #fixando manualmente a largura pra caber na interface
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter) # alinhar ao centro
        #self.background.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False) # permite que outros widgets fiquem por cima  

        #atributos da classe - apenas informações técnicas - informações sobre torres estará na outra sidebar
        '''
        self.fid = QLineEdit("...")
        self.cd_mun = QLineEdit("...")
        self.nm_mun = QLineEdit("...")
        self.latitude = QLineEdit("...")
        self.longitude = QLineEdit("...")
        '''

         #  _________________________________________
         # |         GERANDO AS INFORMAÇÕES          |
         # |_________________________________________|
         
        #dados do municipio
        self.municipio = QLineEdit("...")
        self.fid = QLineEdit("...")
        self.cd_mun = QLineEdit("...")
        self.regiao = QLineEdit("...")
        self.ddd = QLineEdit("...")
        self.populacao = QLineEdit("...")
        # dados relevantes sobre torres
        self.area_total = QLineEdit("...")
        self.area_conectada = QLineEdit("...")
        self.area_desconectada = QLineEdit("...")
        self.percentual_area_conectada = QLineEdit("...")
        self.percentual_area_desconectada = QLineEdit("...")
        self.obrigacoes_unifique = QLineEdit("...")
        self.localidades_sem_conexao = QLineEdit("...")
        #dados relevantes sobre redes de ensino do estado do paraná
        self.rede_municipal_ensino = QLineEdit("...")
        self.rede_estadual_ensino = QLineEdit("...")

        # conteiner + Qlabel + QLineEdit pra gerar o campo de informações da sidebar da direita
        self.municipio_conteiner = self.gerarCampoDeInformacao("MUNICÍPIO:", self.municipio)
        self.fid_conteiner = self.gerarCampoDeInformacao("FID:", self.fid)
        self.cd_mun_conteiner = self.gerarCampoDeInformacao("CD_MUN:", self.cd_mun)
        self.regiao_conteiner = self.gerarCampoDeInformacao("REGIÃO:", self.regiao)
        self.ddd_conteiner = self.gerarCampoDeInformacao("DDD:", self.ddd)
        self.populacao_conteiner = self.gerarCampoDeInformacao("Nº HABITANTES:", self.populacao)
        self.area_total_conteiner = self.gerarCampoDeInformacao("AREA TOTAL:", self.area_total)
        self.area_conectada_conteiner = self.gerarCampoDeInformacao("AREA CONECTADA:", self.area_conectada)
        self.area_desconectada_conteiner = self.gerarCampoDeInformacao("AREA DESCONECTADA:", self.area_desconectada)
        self.percentual_area_conectada_conteiner = self.gerarCampoDeInformacao("% AREA CONECTADA:", self.percentual_area_conectada)
        self.percentual_area_desconectada_conteiner = self.gerarCampoDeInformacao("% AREA DESCONECTADA:", self.percentual_area_desconectada)
        self.obrigacoes_unifique_conteiner = self.gerarCampoDeInformacao("OBRIGAÇÕES UNIFIQUE:", self.obrigacoes_unifique)
        self.localidades_sem_conexao_conteiner = self.gerarCampoDeInformacao("LOCALIDADES SEM CONEXÃO:", self.localidades_sem_conexao)
        self.rede_municipal_ensino_conteiner = self.gerarCampoDeInformacao("ESCOLAS MUNICIPAIS:", self.rede_municipal_ensino)
        self.rede_estadual_ensino_conteiner = self.gerarCampoDeInformacao("ESCOLAS ESTADUAIS:", self.rede_estadual_ensino)

         #  __________________________
         # |         GRUPO 1          |
         # |__________________________|
         # cria o 1º grupo que conterá dados do municipio
        # colocar informações especificas uma ao lado da outra pra economiza espaço da sidebar da direita
        self.conteiner_comprimido_1 = self.agrupandoInfos(self.cd_mun_conteiner, self.fid_conteiner)
        self.conteiner_comprimido_2 = self.agrupandoInfos(self.regiao_conteiner, self.ddd_conteiner)
        self.titulo1 = QLabel("MUNICÍPIO")
        self.titulo1.setStyleSheet(self.recursos.titulos)
        self.group_1 = QVBoxLayout()
        self.group_1.addWidget(self.titulo1)
        self.group_1.addItem(self.municipio_conteiner)
        self.group_1.addItem(self.conteiner_comprimido_1)
        self.group_1.addItem(self.conteiner_comprimido_2)
        self.group_1.addItem(self.populacao_conteiner)
        # Envolver o grupo em um QFrame para aplicar stylesheet pra inserir um fundo escuro com opacidade
        self.grupo_com_background_1 = QFrame()
        self.grupo_com_background_1.setLayout(self.group_1)
        self.grupo_com_background_1.setStyleSheet(self.recursos.style_qframe_1) # aplica efeito de fundo escuro transparente e bordas

         #  __________________________
         # |         GRUPO 2          |
         # |__________________________|
         # cria o 2º grupo que conterá dados de area e conexões
        # para o grupo 2 não será possível agrupar informações uma do lado da outra pois isso ocultaria algumas informações dado o tamanho da area da sidebar
        self.titulo2 = QLabel("AREA E CONEXÃO")
        self.titulo2.setStyleSheet(self.recursos.titulos)
        self.group_2 = QVBoxLayout()
        self.group_2.addWidget(self.titulo2)
        self.group_2.addItem(self.area_total_conteiner)
        self.group_2.addItem(self.area_conectada_conteiner)
        self.group_2.addItem(self.area_desconectada_conteiner)
        self.group_2.addItem(self.percentual_area_conectada_conteiner)
        self.group_2.addItem(self.percentual_area_desconectada_conteiner)
        self.group_2.addItem(self.obrigacoes_unifique_conteiner)
        self.group_2.addItem(self.localidades_sem_conexao_conteiner)

        self.grupo_com_background_2 = QFrame()
        self.grupo_com_background_2.setLayout(self.group_2)
        self.grupo_com_background_2.setStyleSheet(self.recursos.style_qframe_1)

         #  __________________________
         # |         GRUPO 3          |
         # |__________________________|
         # cria o 3º grupo que conterá dados da rede de ensino dos municipios
        self.titulo3 = QLabel("REDE DE ENSINO")
        self.titulo3.setStyleSheet(self.recursos.titulos)
        self.group_3 = QVBoxLayout()
        self.group_3.addWidget(self.titulo3)
        self.group_3.addItem(self.rede_municipal_ensino_conteiner)
        self.group_3.addItem(self.rede_estadual_ensino_conteiner)

        self.grupo_com_background_3 = QFrame()
        self.grupo_com_background_3.setLayout(self.group_3)
        self.grupo_com_background_3.setStyleSheet(self.recursos.style_qframe_1)


        #inserção dos conteiners no layout principal
        self.layout_principal.addWidget(self.background) # plano de fundo é inserido como widget e nao como item
        
        self.layout_principal.addWidget(self.grupo_com_background_1) # adiciona o grupo 1 com fundo escuro no layout principal
        self.layout_principal.addWidget(self.grupo_com_background_2) # adiciona o grupo 2 com fundo escuro no layout principal
        self.layout_principal.addWidget(self.grupo_com_background_3) # adiciona o grupo 3 com fundo escuro no layout principal

        # configurações finais
        self.painel_direito.setLayout(self.layout_principal)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.painel_direito)
        main_layout.setContentsMargins(10, 10, 10, 10)  # margem da janela
        self.layout_principal.addStretch()

        

    def apply_styles(self):
        # estilo do QFrame
        self.painel_direito.setStyleSheet(self.recursos.style_qframe_2)
        #estilo de gradient do background superior onde vai a logo do estado do paraná
        self.background.setStyleSheet(self.recursos.card_board_gradient_vertical)
        # Configurações adicionais
        self.setStyleSheet("""
            QLineEdit {
                background: transparent;
            }
        """)


    def toggle(self):
        # Animação de largura + mudança de texto/ícones
        pass
    
    def gerarCampoDeInformacao(self, descricao, info):
        conteiner = QHBoxLayout()
        descricao = QLabel(descricao)
        conteiner.addWidget(descricao)
        conteiner.addWidget(info)
        info.setReadOnly(True) # pra nao permitir escrita nem copia dos valores
        return conteiner
    
    def agrupandoInfos(self, info1, info2): 
        conteiner_comprimido_1 = QHBoxLayout()
        conteiner_comprimido_1.addItem(info1)
        conteiner_comprimido_1.addItem(info2)
        conteiner_comprimido_1.addStretch() # comprime mais à esquerda pra reduzir mais ainda o espaço
        return conteiner_comprimido_1


    def setAtributo(self, nome_atributo, val): # atualiza valores dos dados
        valor = str(val) 
        if nome_atributo == self.recursos.indice_dados[2]: self.municipio.setText(valor)
        if nome_atributo == self.recursos.indice_dados[0]: self.fid.setText(valor) 
        if nome_atributo == self.recursos.indice_dados[1]: self.cd_mun.setText(valor) 
        if nome_atributo == self.recursos.indice_dados[1]: self.regiao.setText("...")
        if nome_atributo == self.recursos.indice_dados[22]: self.ddd.setText(valor)
        if nome_atributo == self.recursos.indice_dados[25]: self.populacao.setText(f"{float(valor):.2f}")
        if nome_atributo == self.recursos.indice_dados[12]: self.area_total.setText(f"{float(valor):.2f}"+"km²") # area km²
        if nome_atributo == self.recursos.indice_dados[13]: 
            self.area_conectada.setText(f"{float(valor):.2f}"+"km²") 
            var = self.getAreaDesconectada()
            self.area_desconectada.setText(var+"km²") 
        if nome_atributo == self.recursos.indice_dados[14]: 
            self.percentual_area_conectada.setText(f"{float(valor):.2f}"+"%") 
            var = self.getPercentualAreaDesconectada()
            self.percentual_area_desconectada.setText(var+"%")
        if nome_atributo == self.recursos.indice_dados[21]: self.obrigacoes_unifique.setText(valor)
        if nome_atributo == self.recursos.indice_dados[20]: self.localidades_sem_conexao.setText(valor)

        if nome_atributo == self.recursos.indice_dados[19]: self.rede_municipal_ensino.setText(valor)
        if nome_atributo == self.recursos.indice_dados[18]: self.rede_estadual_ensino.setText(valor) 


    def getAreaDesconectada(self):
        area_tot = self.area_total.displayText().split("k") # removendo a string 'km²' do numero float em string pra nao dar erro na hora da conversao em float()
        area_conect = self.area_conectada.displayText().split("k")
        areaDesconectada = float(area_tot[0]) - float(area_conect[0])
        return f"{areaDesconectada:.2f}" #retorna já formatado pra mostra só duas casas após a vírgula

    
    def getPercentualAreaDesconectada(self):
        perc_conectado_string = self.percentual_area_conectada.displayText().split("%") # removendo a string '%'
        perc_conectado = float(perc_conectado_string[0])
        perc_desconectado = 100 - perc_conectado
        return f"{perc_desconectado:.2f}" #retorna já formatado pra mostra só duas casas após a vírgula
