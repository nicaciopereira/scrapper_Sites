import os
import time
from datetime import date
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

url = "https://lista.mercadolivre.com.br/iphone#D[A:iphone]"

# PARAMETRO PARA NOSSO BROSERS SABER COMO ESTAMOS TRABALHANDO, UMA MANEIRA DE SIMULAR UM NAVEGADOR WEB NORMAL
headers = {
    'User-Agent': "Mozilla/5.0(windons NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/86.0.4240.189 Safari/537.36"
}

class AmazonProductScraper:
    def __init__(self):
        self.driver = self.initialize_driver()
        self.category_name = None
        self.formatted_category_name = None

    def initialize_driver(self):
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--log-level=OFF')
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        return webdriver.Chrome(options=opt)

    def get_category_url(self):
        category_url = "https://www.amazon.com.br/b/?ie=UTF8&node=16364755011&ref_=sv_megamenu_pc_3"
        category_url = category_url.format(self.formatted_category_name)
        print(">> Category URL: ", category_url)
        self.driver.get(category_url)
        return category_url

    def extract_webpage_information(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        page_results = soup.find_all('div', {'data-component-type': 's-search-result'})
        return page_results

    @staticmethod
    def extract_product_information(page_results):
        temp_record = []
        for item in page_results:
            a_tag_item = item.h2.a
            description = a_tag_item.text.strip()
            category_url = "https://www.amazon.in/" + a_tag_item.get('href')

            try:
                product_price_location = item.find('span', 'a-price')
                product_price = product_price_location.find('span', 'a-offscreen').text
            except AttributeError:
                product_price = "N/A"

            try:
                product_review = item.i.text.strip()
            except AttributeError:
                product_review = "N/A"

            try:
                review_number = item.find('span', {'class': 'a-size-base'}).text
            except AttributeError:
                review_number = "N/A"

            product_information = (description, product_price[1:], product_review, review_number, category_url)
            temp_record.append(product_information)

        return temp_record

    def navigate_to_other_pages(self, category_url):
        records = []
        print("\n>> Page 1 - webpage information extracted")

        try:
            max_number_of_pages = "//span[@class='s-pagination-item s-pagination-disabled']"
            number_of_pages = self.driver.find_element_by_xpath(max_number_of_pages)
            print("Maximum Pages: ", number_of_pages.text)
        except NoSuchElementException:
            max_number_of_pages = "//li[@class='a-normal'][last()]"
            number_of_pages = self.driver.find_element_by_xpath(max_number_of_pages)

        for i in range(2, int(number_of_pages.text) + 1):
            next_page_url = category_url + "&page=" + str(i)
            self.driver.get(next_page_url)
            page_results = self.extract_webpage_information()
            temp_record = self.extract_product_information(page_results)

            extraction_information = ">> Page {} - webpage information extracted"
            print(extraction_information.format(i))

            for j in temp_record:
                records.append(j)

        print("\n>> Creating an excel sheet and entering the details...")
        return records

    def product_information_spreadsheet(self, records):
        today = date.today().strftime("%d-%m-%Y")
        file_name = "{}_{}.csv".format(self.category_name, today)

        with open(file_name, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'Product URL'])
            writer.writerows(records)

        message = f">> Information about the product '{self.category_name}' is stored in {file_name}\n"
        print(message)
        os.startfile(file_name)

if __name__ == "__main__":
    my_amazon_bot = AmazonProductScraper()
    category_details = my_amazon_bot.get_category_url()
    my_amazon_bot.extract_product_information(my_amazon_bot.extract_webpage_information())
    navigation = my_amazon_bot.navigate_to_other_pages(category_details)
    my_amazon_bot.product_information_spreadsheet(navigation)


print()
print()