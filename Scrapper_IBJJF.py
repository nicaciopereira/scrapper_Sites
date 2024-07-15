import requests
from bs4 import BeautifulSoup #biblioteca para raspagem
import pandas as pd #tratamento de dados
from itertools import product


def Getpage_content(Url , Headers , Parameters):
    Response = requests.get(Url, headers= Headers, params= Parameters).text
    Soup = BeautifulSoup(Response, 'html.parser')
    return Soup

def parseAthletes(Soup):

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
            'Ranking': Ranking
        }
        Athletes.append(Athlete)
    return Athletes

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
    'page':2
}

Page =135

all_athletes = []
while True:
    Parameters['page'] = Page
    Soup_athletes = Getpage_content(Url, Headers, Parameters)
    Athletes = parseAthletes(Soup_athletes)
    if Athletes is None:
        break
    print(Page)
    all_athletes.extend(Athletes) # pega lista joga em lista maior e lista menor ainda faz parte
    Page += 1
print(all_athletes)

df_Athletes = pd.json_normalize(all_athletes)
df_Athletes

excel_File = r'C:\Users\DELL\Desktop\scrapper_Sites/athletes.xlsx'
df_Athletes.to_excel(excel_File, index=False)

