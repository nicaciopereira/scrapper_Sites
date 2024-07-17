import requests  # Importa a biblioteca requests para fazer requisições HTTP
from bs4 import BeautifulSoup  # Importa a BeautifulSoup para analisar o HTML e raspar dados
import pandas as pd  # Importa o pandas para manipulação e análise de dados
from itertools import product  # Importa product da biblioteca itertools para criar combinações de filtros

# Função que obtém o conteúdo da página
def Getpage_content(Url, Headers, Parameters):
    Response = requests.get(Url, headers=Headers, params=Parameters).text  # Faz uma requisição GET e obtém o conteúdo da página como texto
    Soup = BeautifulSoup(Response, 'html.parser')  # Analisa o HTML da resposta usando BeautifulSoup
    return Soup  # Retorna o objeto Soup analisado

# Função que analisa os atletas na página
def parseAthletes(Soup, Kimono, Category, Genero, Faxa, Filter_division):
    Table = Soup.find('table')  # Encontra a tabela de atletas na página
    if not Table:  # Se a tabela não for encontrada
        return None  # Retorna None
    Athletes = []  # Cria uma lista vazia para armazenar os dados dos atletas
    Rows = Table.find_all('tr')  # Encontra todas as linhas na tabela
    if not Rows:  # Se nenhuma linha for encontrada
        return None  # Retorna None

    # Coletando todos os dados dos atletas
    for Row in Rows:
        Photo_Cell = Row.find('td', class_='photo reduced')  # Encontra a célula da foto do atleta
        Name_cell = Row.find('td', class_='name-academy')  # Encontra a célula do nome e academia do atleta
        Points_cell = Row.find('td', class_='pontuation')  # Encontra a célula dos pontos do atleta
        Ranking_cell = Row.find('td', class_='position')  # Encontra a célula do ranking do atleta

        if Photo_Cell and Name_cell and Points_cell and Ranking_cell:  # Verifica se todas as células necessárias foram encontradas
            Photo = Photo_Cell.find('img')['src']  # Obtém o URL da foto do atleta
            Name_tag = Name_cell.find('div', class_='name').find('a')  # Encontra a tag do nome do atleta
            Name = Name_tag.get_text(strip=True)  # Obtém o nome do atleta
            Details = Domain + Name_tag['href']  # Constrói a URL dos detalhes do atleta
            Points = Points_cell.get_text(strip=True)  # Obtém os pontos do atleta
            Ranking = Ranking_cell.get_text(strip=True)  # Obtém o ranking do atleta

            Athlete = {
                'Photo': Photo,  # Adiciona a foto ao dicionário
                'Name': Name,  # Adiciona o nome ao dicionário
                'Details': Details,  # Adiciona a URL dos detalhes ao dicionário
                'Points': Points,  # Adiciona os pontos ao dicionário
                'Ranking': Ranking,  # Adiciona o ranking ao dicionário
                'kimono': Kimono,  # Adiciona o filtro de kimono ao dicionário
                'category': Category,  # Adiciona o filtro de categoria ao dicionário
                'genero': Genero,  # Adiciona o filtro de gênero ao dicionário
                'faxa': Faxa,  # Adiciona o filtro de faixa ao dicionário
                'filter_division': Filter_division  # Adiciona o filtro de divisão ao dicionário
            }
            Athletes.append(Athlete)  # Adiciona o dicionário do atleta à lista de atletas
    return Athletes  # Retorna a lista de atletas

# Função que lista os filtros disponíveis
def List_filters(Soup, filter_id):
    filters = Soup.find(id=filter_id).findAll('option')  # Encontra todos os elementos de opção no filtro especificado
    return [item['value'] for item in filters[1:]]  # Retorna uma lista dos valores dos filtros, ignorando o primeiro (geralmente uma opção padrão)

# Definição das variáveis principais
Domain = 'https://ibjjf.com'  # Define o domínio do site
Url = f'{Domain}/2024-athletes-ranking'  # Define a URL da página de ranking de atletas
Headers = {'User-Agent': 'Mozilla/5.0'}  # Define os cabeçalhos da requisição para imitar um navegador
Parameters = {
    'utf8': '✔',  # Define que a página deve ser codificada em UTF-8
    'filters[s]': 'ranking-geral-gi',  # Define o filtro de ranking geral com kimono
    'filters[ranking_category]': 'adult',  # Define o filtro de categoria como adulto
    'filters[gender]': 'male',  # Define o filtro de gênero como masculino
    'filters[belt]': 'black',  # Define o filtro de faixa como preta
    'filters[weight]': None,  # Define o filtro de peso como None (será preenchido depois)
    'page': 1  # Define a página inicial como 1
}

Soup_filters = Getpage_content(Url, Headers, Parameters)  # Obtém o conteúdo da página de filtros

Kimono = List_filters(Soup_filters, 'filters_s')  # Obtém os filtros de kimono
Category = List_filters(Soup_filters, 'filters_ranking_category')  # Obtém os filtros de categoria
Genero = List_filters(Soup_filters, 'filters_gender')  # Obtém os filtros de gênero
Faxa = List_filters(Soup_filters, 'filters_belt')  # Obtém os filtros de faixa
Filter_division = List_filters(Soup_filters, 'weight_filter')  # Obtém os filtros de divisão de peso

all_athletes = []  # Cria uma lista vazia para armazenar todos os atletas

# Itera sobre todas as combinações de filtros
for kim, categ, gend, faxa, dvsion in product(Kimono, Category, Genero, Faxa, Filter_division):
    Page = 1  # Inicializa a página como 1
    while Page <= 2:  # Limita a raspagem a 2 páginas por combinação de filtros
        print(f'Scraping: {kim}, {categ}, {gend}, {faxa}, {dvsion} for page {Page}')  # Exibe a combinação de filtros e a página atual
        Parameters['filters[s]'] = kim  # Atualiza o filtro de kimono nos parâmetros
        Parameters['filters[ranking_category]'] = categ  # Atualiza o filtro de categoria nos parâmetros
        Parameters['filters[gender]'] = gend  # Atualiza o filtro de gênero nos parâmetros
        Parameters['filters[belt]'] = faxa  # Atualiza o filtro de faixa nos parâmetros
        Parameters['filters[weight]'] = dvsion  # Atualiza o filtro de divisão de peso nos parâmetros
        Parameters['page'] = Page  # Atualiza a página nos parâmetros
        Soup_athletes = Getpage_content(Url, Headers, Parameters)  # Obtém o conteúdo da página de atletas
        Athletes = parseAthletes(Soup_athletes, kim, categ, gend, faxa, dvsion)  # Analisa os atletas na página
        if Athletes is None:  # Se não houver atletas na página
            break  # Interrompe o loop
        all_athletes.extend(Athletes)  # Adiciona os atletas à lista principal
        Page += 1  # Incrementa o número da página

df_Athletes = pd.json_normalize(all_athletes)  # Normaliza a lista de atletas em um DataFrame do pandas
print(df_Athletes)  # Exibe o DataFrame

excel_File = r'C:\Users\DELL\Desktop\scrapper_Sites/athletes.xlsx'  # Define o caminho do arquivo Excel
df_Athletes.to_excel(excel_File, index=False)  # Salva o DataFrame em um arquivo Excel, sem incluir os índices das linhas
