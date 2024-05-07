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

    # Encontrar seletor de quantidade de itens por página
    quantity_selector = soup.find('div', class_='a-section a-spacing-base a-spacing-top-micro }')

    # Extrair opções de quantidade
    if quantity_selector:
        options = quantity_selector.find_all("span", class_='a-size-medium a-color-success')
        string_Qauntity = options.text.strip()
       # quantity_in_page = len(options)
    else:
        quantity_in_page = 0

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

        #encontrar a quantidade
        quantity_element = soup.find("a", class_='a-dropdown-link') 

        #extrair Quantidade por pagina
        #quantities = [element.text.strip() for element in quantity_element]
        #quantity_in_page = quantity_element.text.strip() if quantity_element else 'N/A'

        if quantity_element:
            # tentando extrair com atributo datavalue , verificar antes
            quantity_in_page = quantity_element.get('data-value', 'N/A')
        else:
            quantity_in_page = 'N/A'



        # Adicionar dados do produto à lista
        all_product_data.append({'title': title, 'value': value, 'description': description})

    # Criar DataFrame com os dados dos produtos
    df = pd.DataFrame(all_product_data)

    # Obter data da execução
    date_execution = datetime.datetime.now().strftime('%Y-%m-%d')

    # Nome do arquivo CSV
    file_name = f"page_{page_Number}_{date_execution}.csv"

    # Adicionar data da execução e quantidade de itens por página ao DataFrame
    df['data_execucao'] = date_execution
    df['quantity_In_Page'] = quantity_in_page

    # Salvar dados em arquivo CSV
    df.to_csv(file_name, index=False)

# Fechar o driver após a conclusão
driver.quit()
print()

print("EXTRAÇAO CONCLUIDA")