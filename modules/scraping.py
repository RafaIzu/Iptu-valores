from abc import ABC, abstractclassmethod
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

from .parameters import Parameters


class WebScrapingInterface(ABC):
    @abstractclassmethod
    def get_html_from_request(self):
        pass

    @abstractclassmethod
    def get_urls(self, keyword):
        pass

    @abstractclassmethod
    def get_html_elements(self):
        pass

    @abstractclassmethod
    def convert_html_table_to_dataframe(self):
        pass

class WebScraping(WebScrapingInterface):
    def __init__(self, parameters:Parameters, state, city) -> None:
        super().__init__()
        self.main_url = parameters.main_url
        self.main_html = None
        self.state = state
        self.city = city
        self.__df_iptu = None
        self.hiperlinks_by_regions = [self.main_url]
        self.html_tables = []
        self.page_dates = []
    
    def get_html_from_request(self, url:str):
        request = requests.get(url)
        status_code = request.status_code
        if status_code == 200:
            return request.text
        else:
            raise ConnectionError(f"The url {url} return {status_code}")
    
    def get_urls(self, keyword='valor m'):
        soup = BeautifulSoup(self.main_html, 'html.parser')
        hiperlinks = soup.find_all('a')
        for hiperlink in hiperlinks:
            if hiperlink.find('span'):
                if keyword in hiperlink.find('span').getText().lower():
                    self.hiperlinks_by_regions.append(hiperlink['href'])

    def get_html_elements(self):
        for hiperlink in self.hiperlinks_by_regions:
            html = self.get_html_from_request(hiperlink)
            soup = BeautifulSoup(html, 'html.parser')
            tables = soup.find_all("table")
            self.page_dates = soup.find_all("div", {"class": "data-top"})[0].getText()
            for table in tables:
                self.html_tables.append((table, self.page_dates))
            
    def convert_html_table_to_dataframe(self):
        table_rows = []
        for table, page_date in self.html_tables:
            residence_info = table.find_all('tr')[0].findChildren()[0].getText()
            num_html_table_columns = table.find_all('tr')[2].findChildren()
            region = table.find_all('tr')[0].findChildren()[-1].getText()
            table_data_elements = table.find_all('tr')
            regex_match = re.search(r'dados\s\w+\s\d+', table_data_elements[-1].getText().lower())
            date = regex_match.group(0).replace('dados', '').strip() if regex_match else page_date
            for i_row in range(2, len(table_data_elements) - 1):
                table_data = table_data_elements[i_row].find_all('td')
                if num_html_table_columns == 2:
                    table_rows.append((self.state, self.city, table_data[0].getText(), residence_info, table_data[1].getText(), region, date))
                else:
                    table_rows.append((self.state, self.city, table_data[0].getText(), residence_info, table_data[2].getText(), table_data[1].getText(), date))
        
        self.__df_iptu = pd.DataFrame(table_rows, columns=['estado', 'municipio', 'bairro', 'info', 'valor_m2', 'regiao', 'data'])
    
    @property
    def df_iptu(self):
        return self.__df_iptu


class WebScrapingService:
    def __init__(self, web_scraping: WebScraping) -> None:
        self.web_scraping = web_scraping
    
    def run_all(self, multiples_urls:bool):
        self.web_scraping.main_html = self.web_scraping.get_html_from_request(self.web_scraping.main_url)
        if multiples_urls: self.web_scraping.get_urls()
        self.web_scraping.get_html_elements()
        self.web_scraping.convert_html_table_to_dataframe()
    
    @property
    def df_iptu(self):
        return self.web_scraping.df_iptu
    