class Recursos():
    def __init__(self):
        super().__init__()

        #  ______________________________________________
        # |         DADOS RELEVANTES AO PROJETO          |
        # |______________________________________________|

        self.nome_atributos = ["nome","regiao","total_torres","vivo","claro","tim","obrigacoes_unifique","ddd","area_total","populacao","localidades_sem_conecao"]
        
        self.dados = ["fid","CD_MUN","NM_MUN","UF","Latitude","Longitude","AREA_KM2", "Dados_fid",
                     "Dados_NM_MUN","Dados_AREA_KM2","Dados_areaqgis","Dados_dados conec pr_NM_MUN_2",
                     "Dados_dados conec pr_AREA_KM2_2","Dados_dados conec pr_areaconec",
                     "Dados_dados conec pr_percentualconec","Dados_Torres_claro","Dados_Torres_vivo",
                     "Dados_Torres_tim","Dados_rede_estadual_ensino","Dados_rede_mun_ensino",
                     "Dados_locs_sem_conec","Dados_obgs_unifique","Dados_DDD","area_urbana_areaurbana",
                     "area_rural_arearural","pop_total_mun"]
        

        #  __________________________
        # |         ESTILOS          |
        # |__________________________|

        self.style_qframe_1 = """
            QFrame {
                background: rgba(20, 20, 30, 0.95);     /* semi-transparente */
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);         
            }
        """

        self.style_qframe_2 = """
            QFrame {
                background-image: url('imagens/back1.png');   
                background-position: top;
                background-repeat: no-repeat;
                border-radius: 16px;
                border: none;
                backdrop-filter: blur(20px);  

            }
        """

        self.style_qframe_3 = """
            QFrame {
                background-image: url('imagens/back2.png');   
                background-position: top;
                background-repeat: no-repeat;
                border-radius: 16px;
                border: none;
                backdrop-filter: blur(20px);  

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
                backdrop-filter: blur(20px);  
            };

            background: qlineargradient(
                x1:0, y1:0,
                x2:0, y2:1,
                stop:0 #111,
                stop:1 #222
            );
        """

    
    #  __________________________
    # |         ANIMAÇÕES        |
    # |__________________________|
    @staticmethod
    def animationHover():
        pass