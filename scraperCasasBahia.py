import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def salvar_dados_para_csv(data_execucao, dados, numero_pagina):
    nome_arquivo = f"pag{numero_pagina}.csv"
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow(["Data da Execução", "Descrição do Item", "Valor do Item", "Quantidade do Item"])

        for item in dados:
            escritor_csv.writerow([data_execucao, item['descricao'], item['valor'], item['quantidade']])

def extrair_dados(driver, numero_pagina):
    # Espera até que os itens na página estejam carregados
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1j4cxs8")))
    
    # Extrai informações sobre os itens na página
    itens = driver.find_elements(By.CSS_SELECTOR, ".css-1j4cxs8")
    dados = []
    for item in itens:
        descricao = item.find_element(By.CSS_SELECTOR, "product-special-content-partner").text
        valor = item.find_element(By.CSS_SELECTOR, "dsvia-box css-5w3u76").text
        quantidade = len(item.find_elements(By.CSS_SELECTOR, ".a-icon-row a-spacing-micro"))
        dados.append({'descricao': descricao, 'valor': valor, 'quantidade': quantidade})
    
    # Salva os dados em um arquivo CSV
    data_execucao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    salvar_dados_para_csv(data_execucao, dados, numero_pagina)

def main():
    url_base = "https://www.casasbahia.com.br/c/ar-e-ventilacao/ventiladores-e-circuladores?filtro=categoria^d:c2809_c822&icid=20231117_gen_in_hp_hb_pos4_ar_cat"
    max_paginas = 10
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Opcional: Executar o Chrome em headless
    driver = webdriver.Chrome(options=options)

    for pagina in range(1, max_paginas + 1):
        url = f"{url_base}&page={pagina}"
        driver.get(url)
        extrair_dados(driver, pagina)
    
    driver.quit()

if __name__ == "__main__":
    main()
