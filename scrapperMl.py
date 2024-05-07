import time
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# URL base do Mercado Livre para a categoria de interesse (por exemplo, iPhones)
base_url = "https://lista.mercadolivre.com.br/iphone#D[A:iphone]"

# PARAMETRO PARA NOSSO BROSERS SABER COMO ESTAMOS TRABALHANDO, UMA MANEIRA DE SIMULAR UM NAVEGADOR WEB NORMAL
headers = {
    'User-Agent': "Mozilla/5.0(windons NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/86.0.4240.189 Safari/537.36"
}

# DATA E HORA ATUAIS E FORMATADAS
date_execution = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# Lista para armazenar as URLs de todas as páginas
urls = []

# Número máximo de páginas a serem analisadas
max_pages = 10

# Loop através das páginas
for page_number in range(1, max_pages + 1):
    # Construindo a URL da página atual e adicionando à lista de URLs
    url = f"{base_url}&page={page_number}"
    urls.append(url)

# Configuração do ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Para execução em segundo plano, sem abrir uma janela do navegador
service = Service('C:\\chrome_driver\\chromedriver.exe')  # Substitua pelo caminho para o seu ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Loop sobre cada URL
for index, url in enumerate(urls):
    # Navegando para a URL
    driver.get(url)
    time.sleep(3)  # Espera para garantir que a página seja carregada completamente

    # Obtendo o conteúdo da página
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Encontrando os itens na página
    infos = soup.find_all('div', class_='ui-search-result__content-wrapper')

    # Listas para armazenar os dados da página atual
    quantity_in_pages = []
    values = []
    descriptions = []

    # Iterando sobre os itens encontrados
    for info in infos:

         # Clicando no produto para acessar a página do produto e extrair a descrição
        link = info.find('a', class_='ui-search-link')
        product_url = link['href']
        driver.get(product_url)
        time.sleep(3)  # Espera para garantir que a página seja carregada completamente

        # OBTENDO CONTEUDO DA PAGINA
        soup_product = BeautifulSoup(driver.page_source, 'html.parser')

         # ENCONTRANDO QUANTIDADE NA PAGINA 
        try:
            quantity_button = soup_product.find('button', id='quantity_selector')
            if quantity_button:
                #se o botao for encontrado, procurar pelo span que contena quntidade disponivel
                quantity_span = quantity_button.find('sapn', class_='ui-pdp-buybox__quantity__available')
                #EXTRAINDO VALOR DA QUANTIDADE
                quantity_page = quantity_span.text.strip() if quantity_span else 'NAO ENCONTRADO'
            else:
                quantity_page = 'QUANTIDADE NAO DISPONIVEL'
        except Exception as e:
            quantity_page = 'ERRO AO ENCONTRAR QUANTIDADE' + str(e)
        quantity_in_pages.append(quantity_page)

        # Extração dos VALORES 
        value = info.find('div', class_='ui-search-item__group ui-search-item__group--price ui-search-item__group--price-grid-container')
        values.append(value.text.strip() if value else "NÃO ENCONTRADO")

        # EXTRAÇAO DA DSCRIÇAO
        desc = soup_product.find('p', class_='ui-pdp-description__content')
        descriptions.append(desc.text.strip() if desc else "NÃO ENCONTRADO")

    # IMPRIMINDO NO TERNINAL
    print(f'****** pagina {index + 1} ******')
    for i in range(len(values)):
        print(f'valor: {values[i]}, description: {descriptions[i]}, quantity_in_page: {quantity_in_pages[i]}')
    print("-" *50)


# Verificando se a quantidade de valores adicionados é a mesma
if len(values) == len(descriptions) == len(quantity_in_pages):
    # IMPRIMINDO NO TERMINAL
    print(f'****** página {index + 1} ******')
    for i in range(len(values)):
        print(f'valor: {values[i]}, description: {descriptions[i]}, quantity_in_page: {quantity_in_pages[i]}')
    print("-" *50)
else:
    print("O número de valores, descrições e quantidades não corresponde. Algo deu errado.")


    # Criando DataFrame com os dados coletados da página atual
    data = {
        'Valor': values,
        'Description': descriptions,
        'Quantity_in_page': quantity_in_pages,
        'Date_execution': [date_execution] * len(values)
    }
    df = pd.DataFrame(data)

    # Salvando os dados em um arquivo CSV correspondente à página
    df.to_csv(f"{index + 1}.csv", index=False)

# Fechando o navegador
driver.quit()
