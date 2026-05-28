import matplotlib.pyplot as plt
import numpy as np
import random


# cidades do estado do paraná - ler cidades elegiveis no projeto Vale das Araucárias
cidades = ["Abatiá","Adrianópolis","Agudos do Sul","Almirante Tamandaré","Altamira do Paraná","Alto Paraíso","Alto Paraná","Alto Piquiri",	
           	"Altônia","Alvorada do Sul","Amaporã","Ampére",	"Anahy","Andirá","Ângulo","Antonina","Antônio Olinto","Apucarana","Arapongas","Arapoti",
            "Arapuã","Araruna","Araucária","Ariranha do Ivaí","Assaí","Assis Chateaubriand","Astorga","Atalaia","Balsa Nova","Bandeirantes",
            "Barbosa Ferraz","Barra do Jacaré","Barracão","Bela Vista da Caroba","Bela Vista do Paraíso","Bituruna","Boa Esperança","Boa Esperança do Iguaçu",
            "Boa Ventura de São Roque","Boa Vista da Aparecida","Bocaiúva do Sul","Bom Jesus do Sul","Bom Sucesso","Bom Sucesso do Sul",	
            "Borrazópolis","Braganey","Brasilândia do Sul","Cafeara","Cafelândia","Cafezal do Sul","Califórnia","Cambará","Cambé","Cambira",
            "Campina da Lagoa","Campina do Simão","Campina Grande do Sul","Campo Bonito","Campo do Tenente","Campo Largo","Campo Magro","Campo Mourão",	
            "Cândido de Abreu","Candói","Cantagalo","Capanema","Capitão Leônidas Marques","Carambeí","Carlópolis","Cascavel","Castro","Catanduvas",	
            "Centenário do Sul","Cerro Azul","Céu Azul","Chopinzinho","Cianorte","Cidade Gaúcha","Clevelândia","Colombo","Colorado","Congonhinhas",
            "Conselheiro Mairinck","Contenda","Corbélia","Cornélio Procópio","Coronel Domingos Soares","Coronel Vivida","Corumbataí do Sul","Cruz Machado",
            "Cruzeiro do Iguaçu","Cruzeiro do Oeste","Cruzeiro do Sul","Cruzmaltina","Curitiba","Curiúva","Diamante do Norte","Diamante do Sul","Diamante d'Oeste",
            "Dois Vizinhos","Douradina","Doutor Camargo","Doutor Ulysses","Enéas Marques","Engenheiro Beltrão","Entre Rios do Oeste","Esperança Nova",
            "Espigão Alto do Iguaçu","Farol","Faxinal","Fazenda Rio Grande","Fênix","Fernandes Pinheiro","Figueira","Flor da Serra do Sul","Floraí","Floresta",
            "Florestópolis","Flórida","Formosa do Oeste","Foz do Iguaçu","Foz do Jordão","Francisco Alves","Francisco Beltrão","General Carneiro","Godoy Moreira",
            "Goioerê","Goioxim","Grandes Rios","Guaíra","Guairaçá","Guamiranga","Guapirama","Guaporema","Guaraci","Guaraniaçu","Guarapuava","Guaraqueçaba","Guaratuba",
            "Honório Serpa","Ibaiti","Ibema","Ibiporã","Icaraíma","Iguaraçu","Iguatu","Imbaú","Imbituva","Inácio Martins","Inajá","Indianópolis","Ipiranga","Iporã",
            "Iracema do Oeste","Irati","Iretama","Itaguajé","Itaipulândia","Itambaracá","Itambé","Itapejara d'Oeste","Itaperuçu","Itaúna do Sul","Ivaí","Ivaiporã",
            "Ivaté","Ivatuba","Jaboti","Jacarezinho","Jaguapitã","Jaguariaíva","Jandaia do Sul","Janiópolis","Japira","Japurá","Jardim Alegre","Jardim Olinda","Jataizinho",
            "Jesuítas","Joaquim Távora","Jundiaí do Sul","Juranda","Jussara","Kaloré","Lapa","Laranjal","Laranjeiras do Sul","Leópolis","Lidianópolis","Lindoeste","Loanda",
            "Lobato","Londrina","Luiziana","Lunardelli","Lupionópolis","Mallet","Mamborê","Mandaguaçu","Mandaguari","Mandirituba","Manfrinópolis","Mangueirinha",
            "Manoel Ribas","Marechal Cândido Rondon","Maria Helena","Marialva","Marilândia do Sul","Marilena","Mariluz","Maringá","Mariópolis","Maripá","Marmeleiro",
            "Marquinho","Marumbi","Matelândia","Matinhos","Mato Rico","Mauá da Serra","Medianeira","Mercedes","Mirador","Miraselva","Missal","Moreira Sales","Morretes",
            "Munhoz de Mello","Nossa Senhora das Graças","Nova Aliança do Ivaí","Nova América da Colina","Nova Aurora","Nova Cantu","Nova Esperança do Sudoeste",
            "Nova Esperança","Nova Fátima","Nova Laranjeiras","Nova Londrina","Nova Olímpia","Nova Prata do Iguaçu","Nova Santa Bárbara","Nova Santa Rosa","Nova Tebas",
            "Novo Itacolomi","Ortigueira","Ourizona","Ouro Verde do Oeste","Paiçandu","Palmas","Palmeira","Palmital","Palotina","Paraíso do Norte","Paranacity","Paranaguá",
            "Paranapoema","Paranavaí","Pato Bragado","Pato Branco","Paula Freitas","Paulo Frontin","Peabiru","Perobal","Pérola","Pérola d'Oeste","Piên","Pinhais",
            "Pinhal de São Bento","Pinhalão","Pinhão","Piraí do Sul","Piraquara","Pitanga","Pitangueiras","Planaltina do Paraná","Planalto","Ponta Grossa",
            "Pontal do Paraná","Porecatu","Porto Amazonas","Porto Barreiro","Porto Rico","Porto Vitória","Prado Ferreira","Pranchita","Presidente Castelo Branco",	
            "Primeiro de Maio","Prudentópolis","Quarto Centenário","Quatiguá","Quatro Barras","Quatro Pontes","Quedas do Iguaçu","Querência do Norte","Quinta do Sol",	
            "Quitandinha","Ramilândia","Rancho Alegre","Rancho Alegre d'Oeste","Realeza","Rebouças","Renascença","Reserva","Reserva do Iguaçu","Ribeirão Claro",	
            "Ribeirão do Pinhal","Rio Azul","Rio Bom","Rio Bonito do Iguaçu","Rio Branco do Ivaí","Rio Branco do Sul","Rio Negro","Rolândia","Roncador","Rondon",	
            "Rosário do Ivaí","Sabáudia","Salgado Filho","Salto do Itararé","Salto do Lontra","Santa Amélia","Santa Cecília do Pavão","Santa Cruz de Monte Castelo",
            "Santa Fé","Santa Helena","Santa Inês","Santa Isabel do Ivaí","Santa Izabel do Oeste","Santa Lúcia","Santa Maria do Oeste","Santa Mariana","Santa Mônica",	
            "Santa Tereza do Oeste","Santa Terezinha de Itaipu","Santana do Itararé","Santo Antônio da Platina","Santo Antônio do Caiuá","Santo Antônio do Paraíso",	
            "Santo Antônio do Sudoeste","Santo Inácio","São Carlos do Ivaí","São Jerônimo da Serra","São João","São João do Caiuá","São João do Ivaí","São João do Triunfo",
            "São Jorge do Ivaí","São Jorge do Patrocínio","São Jorge d'Oeste","São José da Boa Vista","São José das Palmeiras","São José dos Pinhais","São Manoel do Paraná",
            "São Mateus do Sul","São Miguel do Iguaçu","São Pedro do Iguaçu","São Pedro do Ivaí","São Pedro do Paraná","São Sebastião da Amoreira","São Tomé","Sapopema",
            "Sarandi","Saudade do Iguaçu","Sengés","Serranópolis do Iguaçu","Sertaneja","Sertanópolis","Siqueira Campos","Sulina","Tamarana","Tamboara","Tapejara","Tapira",
            "Teixeira Soares","Telêmaco Borba","Terra Boa","Terra Rica","Terra Roxa","Tibagi","Tijucas do Sul","Toledo","Tomazina","Três Barras do Paraná","Tunas do Paraná",
            "Tuneiras do Oeste","Tupãssi","Turvo","Ubiratã","Umuarama","União da Vitória","Uniflor","Uraí","Ventania","Vera Cruz do Oeste","Verê","Virmond","Vitorino",
            "Wenceslau Braz","Xambrê"]

QTD_CIDADES = len(cidades) # número de cidades que participam do projeto. 


if __name__ == "__main__":
    
    
    # **
    # * Gráfico de barras verticais
    # *
    # *
    # **

    # Indicadores de cada cidade - contabilizar no odoo em uma variável a quantidade de cidades por município
    # Em seguida ler e salvar nessa variável     
    'valores = [0] * QTD_CIDADES' # aloca estaticamente o tamanho do vetor de quantidade de startups
    valores = []

    
    # NOTA: é preciso ler no Odoo
    # __________Trecho P/ Testes - APAGAR
    for i in range(0, QTD_CIDADES):
        if i <= 12:
            valores.append(random.randint(1,500)) # gera valores temporarios p/ debug
        else:
            valores.append(0)
    # __________

    a=0
    # Trecho para desconsiderar no gráfico cidades com 0 startups
    for i in range(0, len(cidades)):
        if a < len(valores):
            # como python reordena a lista empurrando pra esquerda o elemento (i+1) posterior ao elemento (i) excluido
            # é necessário verificar o elemento anterior (i-1) novamente pois a lista pode ter dois zeros em sequencia.
            if valores[a] == 0: # a cidade possui startups ?
                del cidades[a] # deleta cidades com valor 0
                del valores[a] # deleta indices com valor 0
            else: # se nao possui, avança pra proxima cidade
                a += 1 

    
  
    
    'plt.figure(figsize=(40,8))' # dimensões do gráfico - 9 polegadas de largura e 3 polegadas de altura
    'plt.subplot(131)' # 131 implica que terá: 1 linha, 3 colunas, posição 1 (esquerda)
    fig, axs = plt.subplots(1, 2, figsize=(20, 8))
    axs[0].bar(cidades, valores)
    'plt.xticks(range(len(cidades)), cidades, rotation=90, ha="center")' # rotacionar o nome das cidades e dispô-los na vertical.
    axs[0].set_xticks(range(len(cidades)), cidades, rotation=90, ha="center")
    #plt.xticks(cidades[::10], cidades[::10], rotation=90)
    'plt.tight_layout()' # reduz o tamanho do grafico deixando ele numa versão mais 'thin'

    # **
    # * Gráfico de setores (Pizza)
    # *
    # *
    # **

    init_impulsos = 'Anjo Inovador 1', 'Anjo Inovador 2', 'Outro' # iniciativas de impulso
    num_startups = [400, 125, 230] # Quantidade de startus por iniciativa de impulso - NOTA: é preciso ler no odoo
    axs[1].pie(num_startups, labels=init_impulsos, autopct='%1.1f%%')


    # **
    # * Gráfico de barras horizontais
    # *
    # *
    # **

    '''verticais_atuacao = ['ADTech & Martech', 'AgroTech', 'Big Data', 'BioTech', 'ConstruTech', 'Customer Service', 'Cyber Security',
                         'EduTech', 'Entertainment & Events', 'FinTech & InsurTech', 'FoodTech', 'GovTech', 'GreenTech & Energy',
                         'HealthTech & Wellness', 'HR Tech', 'Industry 4.0', 'IT & Comm', 'LegalTech', 'LogTech', 'Mobility', 
                         'Productivity', 'Real Estate Tech', 'RetailTech', 'Social Impact', 'SporTech', 'Tourism', 'Vet & Pet Tech',
                         'Outros']
    
    municipios_por_verticais = [42,88,56,41,23,98,56,52,54,59,67,42,53,71,86,81,94,37,65,85,31,1,10,20,65,95,74,130]

    axs[2].barh(verticais_atuacao, municipios_por_verticais)
    axs[2].xlabel('Verticais')
    axs[2].ylabel('Municípios')
    axs[2].title("Verticais de atuação por município")'''
    
    plt.show()


    















'def graphBar:'

'def graphHistogram:'

'def GraphPizza:'




