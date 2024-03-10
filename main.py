from modules.scraping import WebScrapingService, WebScraping
from modules.json import JsonFileParameter
from modules.parameters import Parameters
from modules.iptu import Iptu, IptuService
from modules.db import Db, DbService
import pandas as pd # teste
import logging

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


def main():
    logging.info('Starting program')
    json = JsonFileParameter('./parameters.json')
    if json.read_json_file(): 
        parameters = Parameters(json.json_data)
        logging.info('Json file read with success')
    else:
        logging.error('Json file read with success', exc_info=True)
        return 0

    webscrapping = WebScrapingService(WebScraping(parameters, 'SP',
                                                  'São Paulo'))
    try:
        webscrapping.run_all()
        logging.info('Webscrapping finished with success')
    except:
        logging.error('Webscrapping failed', exc_info=True)
        return 0
    
    try:
        iptu = IptuService(Iptu(webscrapping.df_iptu))
        iptu.run_all()
    except:
        logging.error('Dataframe formating failed', exc_info=True)
        return 0

    db_service = DbService(Db(parameters.driver, parameters.db_user,
                              parameters.db_pw, parameters.db_server,
                              parameters.db_port, parameters.db_name))

    db_service.run_all(iptu.df_iptu,'iptu_valores')

    # db_service.run_all(pd.DataFrame(),'iptu') # teste

    
    
if __name__ == "__main__":
    main()
