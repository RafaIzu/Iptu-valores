from abc import ABC, abstractclassmethod
import pandas as pd
import re


class IptuInterface(ABC):
    @abstractclassmethod
    def format_valor_column(self):
        pass
    
    @abstractclassmethod
    def format_info_column(self):
        pass

    @abstractclassmethod
    def create_tipo_residencia_column(self):
        pass

    @abstractclassmethod
    def create_num_dormitorios_column(self):
        pass

    @abstractclassmethod
    def create_num_vagas_column(self):
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

    def format_info_column(self):
        self.__df_iptu['info'] = self.__df_iptu['info'].str.replace('\n','')

    def create_tipo_residencia_column(self):
        self.__df_iptu['tipo_residencia'] = self.__df_iptu['info'].apply(lambda x: self.__get_residency_type(x.lower()))

    def create_num_dormitorios_column(self):
        self.__df_iptu['num_dorm'] = self.__df_iptu['info'].apply(lambda x: self.__get_num_dorm(x.lower()))
    
    def create_num_vagas_column(self):
        self.__df_iptu['num_vagas'] = self.__df_iptu['info'].apply(lambda x: self.__get_num_vagas(x.lower()))

    def create_mes_column(self):
        self.__df_iptu['mes'] = self.__df_iptu['data'].str.split()[0][0]
        self.__df_iptu['mes'] = self.__df_iptu['mes'].apply(lambda x: self.__months_pt.get(x, ''))

    def create_ano_column(self):
        self.__df_iptu['ano'] = self.__df_iptu['data'].str.split()[0][1]
    
    @staticmethod
    def __get_residency_type(residence_info):
        if 'kitnets e apartamentos de 1 dor' in residence_info:
            return 'kitnet/apartamento 1 dorm'
        elif 'kitnets / studios / lofts e apartamentos 1' in residence_info:
            return 'kitnet/studio/loft/apartamento 1 dorm'
        elif 'apartamento' in residence_info:
            return 'apartamento acima de 1 dorm'
        elif 'casa' in residence_info:
            return 'casa'
        else:
            return 'outros'
    
    @staticmethod
    def __get_num_dorm(residence_info):
        if 'kitnets e apartamentos de 1 dor' in residence_info \
            or 'kitnets / studios / lofts e apartamentos 1' in residence_info:
            return '1'
        match_regex = re.search(r'\d*\s*e*\s*\d\sdormi', residence_info)
        if match_regex:
            return match_regex.group(0).replace('dormi', '').strip()
        match_regex = re.search(r'\d\ssuítes\sou\s\d\sou\smais\sdorm', residence_info)
        if match_regex:
            return match_regex.group(0).replace('dorm', '').strip()
        return 'NO INFO'
    
    @staticmethod
    def __get_num_vagas(residence_info):
        if 'sem vaga' in residence_info:
            return '0'
        match_regex = re.search(r'\d\svaga', residence_info)
        if match_regex:
            return match_regex.group(0).replace('vaga', '').strip()
        match_regex = re.search(r'\d\sou\smais\svaga', residence_info)
        if match_regex:
            return match_regex.group(0).replace('vaga', '').strip()
        return 'NO INFO'
    
    @property
    def df_iptu(self):
        return self.__df_iptu[['estado', 'municipio', 'regiao', 'bairro',
                               'tipo_residencia', 'num_dorm', 'num_vagas',
                               'valor_m2', 'info', 'mes', 'ano']]


class IptuService:
    def __init__(self, iptu:Iptu) -> None:
        self.__iptu = iptu
    
    def run_all(self):
        self.__iptu.format_info_column()
        self.__iptu.format_valor_column()
        self.__iptu.create_tipo_residencia_column()
        self.__iptu.create_num_dormitorios_column()
        self.__iptu.create_num_vagas_column()
        self.__iptu.create_mes_column()
        self.__iptu.create_ano_column()
        
    def get_csv_file_sample(self):
        self.__iptu.df_iptu.to_csv(f'./iptu_{self.__iptu.df_iptu['ano'][0]}.csv', index=False)

    def get_excel_file_sample(self):
        self.__iptu.df_iptu.to_csv(f'./iptu_{self.__iptu.df_iptu['ano'][0]}.xlsx', index=False)
    
    @property
    def df_iptu(self):
        return self.__iptu.df_iptu


    

