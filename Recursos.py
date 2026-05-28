from PySide6.QtGui import QColor

WIDTH = 1600
HEIGHT = 900
NOME_SOFT = "GeoTorres Connect Paraná"
VER = "1.0.0.01"
PATH_DADOS = "dados.json" # dados da DRI
PATH_MUNICIPIOS = "municipios.json" # dados próprios usados pra desenhar os mapas - possui todos os vertices dos municipios do paraná
COR_PADRAO = QColor("#555555")
COR_PADRAO_2 = QColor("#3f4e54")
AZUL_PARANA = QColor("#3388ff")
VERDE_PARANA = QColor("#008b3b")
COR_TORRES = QColor("#d80000")

#CORES PARA REGIÕES:
COR_REGIAO_CURITIBA = QColor("#555555")
COR_REGIAO_CASCAVEL = QColor("#474747")
COR_REGIAO_PONTAGROSSA = QColor("#383838")
COR_REGIAO_LONDRINA = QColor("#252525")
COR_REGIAO_MARINGA = QColor("#1D1D1D")
COR_REGIAO_GUARAPUAVA = QColor("#141414")

class Recursos():
    def __init__(self):
        super().__init__()


        #  ______________________________________________
        # |         DADOS RELEVANTES AO PROJETO          |
        # |______________________________________________|

        self.nome_atributos = ["nome","regiao","total_torres","vivo","claro","tim","obrigacoes_unifique","ddd","area_total","populacao","localidades_sem_conecao", "ligga"]
        
        self.indice_dados = ["fid","CD_MUN","NM_MUN","UF","Latitude","Longitude","AREA_KM2", "Dados_fid",
                     "Dados_NM_MUN","Dados_AREA_KM2","Dados_areaqgis","Dados_dados conec pr_NM_MUN_2",
                     "Dados_dados conec pr_AREA_KM2_2","Dados_dados conec pr_areaconec",
                     "Dados_dados conec pr_percentualconec","Dados_Torres_claro","Dados_Torres_vivo",
                     "Dados_Torres_tim","Dados_rede_estadual_ensino","Dados_rede_mun_ensino",
                     "Dados_locs_sem_conec","Dados_obgs_unifique","Dados_DDD","area_urbana_areaurbana",
                     "area_rural_arearural","pop_total_mun"]
        
        #  __________________________
        # |           URLs           |
        # |__________________________|

        self.path_vivo = "imagens/vivo.png"
        self.path_claro = "imagens/claro.png"
        self.path_tim = "imagens/tim.png"
        self.path_ligga = "imagens/ligga.png"
        self.path_torres_totais = "imagens/torres_totais.png"
        self.path_zoom_out = "imagens/zoom_out.png"
        self.path_zoom_in = "imagens/zoom_in.png"
        self.path_toolbox = "imagens/toolbox.png"
        self.path_button_off = "imagens/off2.png"
        self.path_button_on = "imagens/on2.png"
        self.path_button_graphics_hide = "imagens/graphs_hide.png"
        self.path_button_graphics_show = "imagens/graphs_show.png"
        self.path_animation_off = "imagens/off3.png"
        self.path_animation_on = "imagens/on3.png"

        #  __________________________
        # |         ESTILOS          |
        # |__________________________|

        self.style_qframe_1 = """
            QFrame {
                background: rgba(20, 20, 30, 0.45);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            QLineEdit {
                background-color: rgba(255, 255, 255, 0.08);   /* fundo leve */
                border: none;                                   /* remove borda */
                border-radius: 8px;
                padding: 6px 8px;
                color: white;
                font-size: 11px;
            }

            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(0, 120, 255, 0.6);
            }

            QLabel {
                background-color: transparent;
                font-size: 10px;
                padding: 2px 0px;
                border: none; 
            }
        """

        self.style_theme_1 = """
            QFrame {
                background-image: url('imagens/back1_2.png');   
                background-position: top;
                background-repeat: no-repeat;
                border-radius: 16px;
                border: none;

            }
        """

        self.style_theme_1_aux = """
            QFrame {
                background-image: url('imagens/back2.png');   
                background-position: top;
                background-repeat: no-repeat;
                border-radius: 16px;
                border: none;

            }
        """

        self.style_theme_2 = """
            QFrame {
                background-image: url('imagens/back_parana_right.png');   
                background-position: top;
                background-repeat: no-repeat;
                border-radius: 16px;
                border: none;
            }
        """

        self.style_theme_2_aux = """
            QFrame {
                background-image: url('imagens/back_parana_left.png');   
                background-position: top;
                background-repeat: no-repeat;
                border-radius: 16px;
                border: none;
            }
        """

        self.card_board_gradient_vertical = """
            background: qlineargradient(
                x1:0, y1:0,
                x2:0, y2:1,
                stop:0 #111,
                stop:1 #222
            );
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
            
        """

        self.card_board_gradient_horizontal = """
            background: qlineargradient(
                x1:0, y1:0,
                x2:1, y2:0,
                stop:0 #0b0b0b,
                stop:0.5 #1b1b1b,
                stop:1 #2a2a2a
            );
        """

        self.background_logo = """
            QLabel {
                background-image: url('imagens/logo_seia_sidebar.png');   
                background-position: top;
                background-repeat: no-repeat;
                border-radius: 16px;
                border: none;
            };

            background: qlineargradient(
                x1:0, y1:0,
                x2:0, y2:1,
                stop:0 #111,
                stop:1 #222
            );
        """
    
        self.vivo_config_style = """
            background-image: url(imagens/vivo.png);
            background-repeat: no-repeat;
            background-position: center;
            background-color: transparent;
            font-size: 18px;
            font-weight: bold;
            border: none;
            padding-top: 65px;
            qproperty-alignment: AlignHCenter;
        """

        self.claro_config_style = """
            background-image: url(imagens/claro.png);
            background-repeat: no-repeat;
            background-position: center;
            background-color: transparent;
            font-size: 18px;
            font-weight: bold;
            border: none;
            padding-top: 65px;
            qproperty-alignment: AlignHCenter;
        """

        self.tim_config_style = """
            background-image: url(imagens/tim.png);
            background-repeat: no-repeat;
            background-position: center;
            background-color: transparent;
            font-size: 18px;
            font-weight: bold;
            border: none;
            padding-top: 65px;
            qproperty-alignment: AlignHCenter;
        """

        self.ligga_config_style = """
            background-image: url(imagens/ligga.png);
            background-repeat: no-repeat;
            background-position: center;
            background-color: transparent;
            font-size: 18px;
            font-weight: bold;
            border: none;
            padding-top: 65px;
            qproperty-alignment: AlignHCenter;
        """

        self.torres_totais_config_style = """
            background-image: url(imagens/torres_totais.png);
            background-repeat: no-repeat;
            background-position: center;
            background-color: transparent;
            font-size: 18px;
            font-weight: bold;
            color: black;
            border: none;
            padding-top: 65px;
            qproperty-alignment: AlignHCenter;
        """

        self.titulos = """
            background: none;
            font-size: 16px;
            font-weight: bold;
            border: none;
        """

        self.tooltips = """
            QToolTip {
                color: white;
                background-color: #333333;
                border: 1px solid #ffffff;
                padding: 8px;
                border-radius: 4px;
                opacity: 230;
            }
        """

        # estilo nao usado atualmente
        self.checkbox_button_edition = """
            QCheckBox {
                spacing: 20px;
            }
            QCheckBox::indicator {
                width: 23px;
                height: 23px;
                border: 1px solid gray;
                border-radius: 18px;
            }
            QCheckBox::indicator:unchecked {
                image: url(imagens/off2.png); 
                border: 1px solid gray;
                border-radius: 18px;
                background-color: transparent;
            }
            QCheckBox::indicator:checked {
                image: url(imagens/on2.png);
                border: 1px solid #2196F3;
                border-radius: 18px;
                background-color: transparent;
            }
        """

        self.push_button = """
            QPushButton {
            }
            QPushButton::indicator {
                background-color: transparent;
            }
            QPushButton::indicator:unchecked {
                background-color: transparent;
            }
            QPushButton::indicator:checked {
                background-color: #D8FEE9;
            }
        """
        

    
    #  __________________________
    # |         ANIMAÇÕES        |
    # |__________________________|
    def animationHover():
        pass

    def getHTML(self, nome_municipio, nome_arquivo):
        #  __________________________
        # |           HTML           |
        # |__________________________|
        
        # HTML com imagem + texto embaixo
        html = f"""
            <div style='text-align: center;'>
                <img src='brasoes/{nome_arquivo}' width='70' height='70'>
                <br><b>{nome_municipio}</b>
            </div>
        """
        return html