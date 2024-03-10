from abc import ABC, abstractclassmethod
import pandas as pd


class IptuInterface(ABC):
    @abstractclassmethod
    def format_valor_column(self):
        pass

    @abstractclassmethod
    def create_mes_column(self):
        pass

    @abstractclassmethod
    def create_ano_column(self):
        pass


class Iptu(IptuInterface):
    def __init__(self, df:pd.DataFrame) -> None:
        self.__df_iptu = df
        self.__months_pt = {
        'janeiro': '1',
        'fevereiro': '2',
        'março': '3',
        'abril': '4',
        'maio': '5',
        'junho': '6',
        'julho': '7',
        'agosto': '8',
        'setembro': '9',
        'outubro': '10',
        'novembro': '11',
        'dezembro': '12'
    }
        super().__init__()
    
    def format_valor_column(self):
        self.__df_iptu['valor_m2'] = self.__df_iptu['valor_m2'].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float)

    def create_mes_column(self):
        self.__df_iptu['mes'] = self.__df_iptu['data'].str.split()[0][0]
        self.__df_iptu['mes'] = self.__df_iptu['mes'].apply(lambda x: self.__months_pt.get(x, ''))

    def create_ano_column(self):
        self.__df_iptu['ano'] = self.__df_iptu['data'].str.split()[0][1]
    
    @property
    def df_iptu(self):
        return self.__df_iptu[['estado', 'municipio', 'regiao', 'bairro', 'valor_m2', 'mes', 'ano']]


class IptuService:
    def __init__(self, iptu:Iptu) -> None:
        self.__iptu = iptu
    
    def run_all(self):
        self.__iptu.format_valor_column()
        self.__iptu.create_mes_column()
        self.__iptu.create_ano_column()
    
    @property
    def df_iptu(self):
        return self.__iptu.df_iptu


    

