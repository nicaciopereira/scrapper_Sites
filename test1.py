import time
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

url_Page = 'https://www.amazon.com.br/s?rh=n%3A17923695011&fs=true&ref=lp_17923695011_sar'

# Número máximo de páginas
max_Pages = 10

# Configuração do ChromeDriver
chrome_Option = Options()
chrome_Option.add_argument('--headless')
service = Service('C:\\chrome_driver\\chromedriver.exe')  # Substitua pelo caminho para o seu ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_Option)

# Loop pelas páginas
for page_Number in range(1, max_Pages + 1):
    print(f"Extraindo dados da página {page_Number} de {max_Pages}...")
    # Navegar para a URL da página atual
    url = f"{url_Page}&page={page_Number}"
    driver.get(url)
    time.sleep(4)

    # Conteúdo da página
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Encontrar itens da página
    page_items = soup.find_all('div', class_='s-result-item')

    # Lista para armazenar dados de todos os produtos na página
    all_product_data = []

    for item in page_items:
        # Extrair título do produto
        title_element = item.find('span', class_='a-size-base-plus a-color-base a-text-normal')
        title = title_element.text.strip() if title_element else 'N/A'

        # Extrair preço do produto
        price_element = item.find('span', class_='a-price')
        value = price_element.find('span', class_='a-offscreen').text.strip() if price_element else 'N/A'

        # Extrair descrição do produto
        description_element = item.find('span', class_='a-size-base-plus a-color-base a-text-normal')
        description = description_element.text.strip() if description_element else 'N/A'

        # Adicionar dados do produto à lista
        all_product_data.append({'title': title, 'value': value, 'description': description})

    # Criar DataFrame com os dados dos produtos
    df = pd.DataFrame(all_product_data)

    # Obter data da execução
    date_execution = datetime.datetime.now().strftime('%Y-%m-%d')

    # Nome do arquivo CSV
    file_name = f"page_{page_Number}_{date_execution}.csv"

    # Adicionar data da execução ao DataFrame
    df['data_execucao'] = date_execution

    # Salvar dados em arquivo CSV
    df.to_csv(file_name, index=False)

# Fechar o driver após a conclusão
driver.quit()
print()
print()