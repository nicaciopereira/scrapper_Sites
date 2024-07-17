# scrapper_Sites


Scraper de Atletas IBJJF
Este projeto é um web scraper que coleta dados de atletas do site da IBJJF (International Brazilian Jiu-Jitsu Federation). O código faz a raspagem de dados dos atletas, incluindo nome, foto, pontos, ranking e detalhes adicionais, e salva os dados em um arquivo Excel.

Requisitos
Python 3.x
Bibliotecas:
requests
beautifulsoup4
pandas
itertools
Você pode instalar as bibliotecas necessárias usando o comando:
pip install requests beautifulsoup4 pandas

Estrutura do Código
1. Importação das Bibliotecas
python

import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import product
requests: Usado para fazer requisições HTTP.
BeautifulSoup: Biblioteca para análise de HTML e raspagem de dados.
pandas: Usado para manipulação e análise de dados.
itertools: Biblioteca para operações iterativas eficientes, usada aqui para combinar diferentes filtros.

2. Função Getpage_content

def Getpage_content(Url, Headers, Parameters):
    Response = requests.get(Url, headers=Headers, params=Parameters).text
    Soup = BeautifulSoup(Response, 'html.parser')
    return Soup

Essa função faz uma requisição HTTP GET à URL fornecida, usando cabeçalhos e parâmetros específicos. Ela retorna o conteúdo da página analisado pelo BeautifulSoup.

3. Função parseAthletes

def parseAthletes(Soup, Kimono, Category, Genero, Faxa, Filter_division):
    Table = Soup.find('table')
    if not Table:
        return None

    Athletes = []
    Rows = Table.find_all('tr')
    if not Rows:
        return None

    for Row in Rows:
        Photo_Cell = Row.find('td', class_='photo reduced')
        Name_cell = Row.find('td', class_='name-academy')
        Points_cell = Row.find('td', class_='pontuation')
        Ranking_cell = Row.find('td', class_='position')

        if Photo_Cell and Name_cell and Points_cell and Ranking_cell:
            Photo = Photo_Cell.find('img')['src']
            Name_tag = Name_cell.find('div', class_='name').find('a')
            Name = Name_tag.get_text(strip=True)
            Details = Domain + Name_tag['href']
            Points = Points_cell.get_text(strip=True)
            Ranking = Ranking_cell.get_text(strip=True)

            Athlete = {
                'Photo': Photo,
                'Name': Name,
                'Details': Details,
                'Points': Points,
                'Ranking': Ranking,
                'kimono': Kimono,
                'category': Category,
                'genero': Genero,
                'faxa': Faxa,
                'filter_division': Filter_division
            }
            Athletes.append(Athlete)
    return Athletes

Essa função analisa a página HTML para encontrar a tabela de atletas. Em seguida, itera sobre cada linha da tabela, extraindo os detalhes dos atletas e adicionando-os a uma lista.

4. Função List_filters

def List_filters(Soup, filter_id):
    filters = Soup.find(id=filter_id).findAll('option')
    return [item['value'] for item in filters[1:]]
Essa função extrai e retorna uma lista de valores de um filtro específico na página HTML.

5. Coleta de Filtros

Domain = 'https://ibjjf.com'
Url = f'{Domain}/2024-athletes-ranking'
Headers = {'User-Agent': 'Mozilla/5.0'}
Parameters = {
    'utf8': '✔',
    'filters[s]': 'ranking-geral-gi',
    'filters[ranking_category]': 'adult',
    'filters[gender]': 'male',
    'filters[belt]': 'black',
    'filters[weight]': None,
    'page': 1
}

Soup_filters = Getpage_content(Url, Headers, Parameters)

Kimono = List_filters(Soup_filters, 'filters_s')
Category = List_filters(Soup_filters, 'filters_ranking_category')
Genero = List_filters(Soup_filters, 'filters_gender')
Faxa = List_filters(Soup_filters, 'filters_belt')
Filter_division = List_filters(Soup_filters, 'weight_filter')
Aqui, os filtros disponíveis na página são coletados e armazenados em listas separadas.

6. Coleta de Dados dos Atletas
python


all_athletes = []

for kim, categ, gend, faxa, dvsion in product(Kimono, Category, Genero, Faxa, Filter_division):
    Page = 1
    while Page <= 2:
        print(f'Scraping: {kim}, {categ}, {gend}, {faxa}, {dvsion} for page {Page}')
        Parameters['filters[s]'] = kim 
        Parameters['filters[ranking_category]'] = categ
        Parameters['filters[gender]'] = gend
        Parameters['filters[belt]'] = faxa
        Parameters['filters[weight]'] = dvsion 
        Parameters['page'] = Page
        Soup_athletes = Getpage_content(Url, Headers, Parameters)
        Athletes = parseAthletes(Soup_athletes, kim, categ, gend, faxa, dvsion)
        if Athletes is None:
            break
    
        all_athletes.extend(Athletes)
        Page += 1

df_Athletes = pd.json_normalize(all_athletes)
print(df_Athletes)

excel_File = r'C:\Users\DELL\Desktop\scrapper_Sites/athletes.xlsx'
df_Athletes.to_excel(excel_File, index=False)
Essa seção combina todos os filtros possíveis e coleta os dados dos atletas para cada combinação de filtros, salvando os resultados em um arquivo Excel.

Melhorias Futuras
Paralelização: Utilizar threads ou processos para paralelizar a coleta de dados, melhorando a eficiência.
Tratamento de Erros: Implementar tratamento de exceções para lidar com falhas na requisição ou na raspagem dos dados.
Interface Gráfica: Criar uma interface gráfica para facilitar a configuração dos parâmetros de busca e exibir os resultados.
Armazenamento: Integrar com um banco de dados para armazenar e consultar os dados dos atletas de forma mais eficiente.
Análise de Dados: Adicionar análises e visualizações dos dados coletados para insights mais profundos.