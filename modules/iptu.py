from abc import ABC, abstractclassmethod
import pandas as pd
import re


class IptuInterface(ABC):
    @abstractclassmethod
    def remove_empty_rows(self):
        pass

    @abstractclassmethod
    def format_valor_column(self):
        pass

    @abstractclassmethod
    def drop_na_values(self):
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
        self.df_iptu = df
        self.__months_pt = {
        'jan': '1',
        'fev': '2',
        'mar': '3',
        'abr': '4',
        'mai': '5',
        'jun': '6',
        'jul': '7',
        'ago': '8',
        'set': '9',
        'out': '10',
        'nov': '11',
        'dez': '12'
    }
        super().__init__()
    
    def remove_empty_rows(self):
        self.df_iptu['valor_m2'] = self.df_iptu['valor_m2'].str.replace(u'\xa0', '')
        self.df_iptu = self.df_iptu[self.df_iptu['valor_m2'] != '']

    def format_valor_column(self):
        self.df_iptu['valor_m2'] = self.df_iptu['valor_m2'].str.replace('R$', '').str.replace('.', '').str.replace(',', '.')
        self.df_iptu['valor_m2'] = pd.to_numeric(self.df_iptu['valor_m2'],errors='coerce')

    def drop_na_values(self):
        self.df_iptu = self.df_iptu.dropna()

    def format_info_column(self):
        self.df_iptu['info'] = self.df_iptu['info'].str.replace('\n','')
        self.df_iptu.reset_index(drop=True, inplace=True)

    def create_tipo_residencia_column(self):
        self.df_iptu['tipo_residencia'] = self.df_iptu['info'].apply(lambda x: self.__get_residency_type(x.lower()))

    def create_num_dormitorios_column(self):
        self.df_iptu['num_dorm'] = self.df_iptu['info'].apply(lambda x: self.__get_num_dorm(x.lower()))
    
    def create_num_vagas_column(self):
        self.df_iptu['num_vagas'] = self.df_iptu['info'].apply(lambda x: self.__get_num_vagas(x.lower()))

    def create_mes_column(self):
        regex_match = re.search(r'\d\d\.\w+\.\d+', self.df_iptu['data'][0])
        if regex_match:
            self.df_iptu['data'] = self.df_iptu['data'].str.extract(r'(\d\d\.\w+\.\d+)')
            self.df_iptu['mes'] = self.df_iptu['data'].str.split('.')[0][1]
        else:
            self.df_iptu['mes'] = self.df_iptu['data'].str.split()[0][2]
        self.df_iptu['mes'] = self.df_iptu['mes'].apply(lambda x: self.__months_pt.get(x.lower()[:3], ''))

    def create_ano_column(self):
        regex_match = re.search(r'\d\d\.\w+\.\d+', self.df_iptu['data'][0])
        if regex_match:
            self.df_iptu['data'] = self.df_iptu['data'].str.extract(r'(\d\d\.\w+\.\d+)')
            self.df_iptu['ano'] = self.df_iptu['data'].str.split('.')[0][2]
        else:
            self.df_iptu['ano'] = self.df_iptu['data'].str.split()[0][1]
    
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
    
    def sort_columns(self):
        self.df_iptu = self.df_iptu[['estado', 'municipio', 'regiao', 'bairro',
                               'tipo_residencia', 'num_dorm', 'num_vagas',
                               'valor_m2', 'info', 'mes', 'ano']]


class IptuService:
    def __init__(self, iptu:Iptu) -> None:
        self.__iptu = iptu
    
    def run_all(self):
        self.__iptu.remove_empty_rows()
        self.__iptu.format_info_column()
        self.__iptu.format_valor_column()
        self.__iptu.drop_na_values()
        self.__iptu.create_tipo_residencia_column()
        self.__iptu.create_num_dormitorios_column()
        self.__iptu.create_num_vagas_column()
        self.__iptu.create_mes_column()
        self.__iptu.create_ano_column()
        self.__iptu.sort_columns()
        
    def get_csv_file_sample(self):
        self.__iptu.df_iptu.to_csv(f'./iptu_{self.__iptu.df_iptu['ano'][0]}.csv', index=False)

    def get_excel_file_sample(self):
        self.__iptu.df_iptu.to_csv(f'./iptu_{self.__iptu.df_iptu['ano'][0]}.xlsx', index=False)
    
    @property
    def df_iptu(self):
        return self.__iptu.df_iptu


    

