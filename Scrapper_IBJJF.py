import requests
from bs4 import BeautifulSoup #biblioteca para raspagem
import pandas as pd #tratamento de dados
from itertools import product


def Getpage_content(Url , Headers , Parameters):
    Response = requests.get(Url, headers= Headers, params= Parameters).text
    Soup = BeautifulSoup(Response, 'html.parser')
    return Soup

def parseAthletes(Soup,Kimono,Category, Genero, Faxa, Filter_division ):
    Table = Soup.find('table')
    #print(Table)
    if not Table:
        return None
    Athletes = []
    Rows = Table.find_all('tr')
    #print(Rows)
    if not Rows:
        return None

    #coletando todos os dados dos atletas
    for Row in Rows:
        Photo_Cell = Row.find('td', class_ ='photo reduced')
        Name_cell = Row.find('td', class_ ='name-academy')
        Points_cell = Row.find('td', class_ ='pontuation' )
        Ranking_cell = Row.find('td', class_ ='position')


        Photo = Photo_Cell.find('img')['src']
        Name_tag = Name_cell.find('div', class_ ='name').find('a')
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

def List_filters(Soup, filter_id):
    filters = Soup.find(id = filter_id).findAll('option')
    return [item['value'] for item in filters[1:]]

#cabeçario
Domain = 'https://ibjjf.com'
Url = f'{Domain}/2024-athletes-ranking'
Headers = {'User-Agent': 'Mozilla/5.0'}
Parameters ={
    'utf8':  '✔',
    'filters[s]':'ranking-geral-gi',
    'filters[ranking_category]':'adult',
    'filters[gender]':'male',
    'filters[belt]':'black',
    'filters[weight]':None, 
    'page':1
    }

Soup_filters = Getpage_content(Url, Headers, Parameters)

Kimono = List_filters(Soup_filters, 'filters_s')
Category = List_filters(Soup_filters, 'filters_ranking_category')
Genero = List_filters(Soup_filters, 'filters_gender')
Faxa = List_filters(Soup_filters, 'filters_belt')
Filter_division = List_filters(Soup_filters, 'weight_filter')



all_athletes = []

for kim, categ, gend, faxa, dvsion in product(Kimono,Category, Genero, Faxa, Filter_division):
    Page =1
    #while True:

    while Page<=2:
        print(f'Scraping: {kim}, {categ}, {gend}, {faxa}, {dvsion} for page {Page}')
        Parameters['filters[s]']:kim 
        Parameters['filters[ranking_category]']:categ
        Parameters['filters[gender]']:gend
        Parameters['filters[belt]']:faxa
        Parameters['filters[weight]']:dvsion 
        Parameters['page']:Page
        Soup_athletes = Getpage_content(Url, Headers, Parameters)
        Athletes = parseAthletes(Soup_athletes,kim,categ,gend,faxa,dvsion)
        if Athletes is None:
            break
    
        all_athletes.extend(Athletes) # pega lista joga em lista maior e lista menor ainda faz parte
        Page += 1

df_Athletes = pd.json_normalize(all_athletes)
df_Athletes
print(df_Athletes)

excel_File = r'C:\Users\DELL\Desktop\scrapper_Sites/athletes.xlsx'
df_Athletes.to_excel(excel_File, index=False)

