import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

years = ['2017','2018','2019','2020','2021','2022']
league_type = ['standard', 'ppr']
league_size = ['8-team','10-team','12-team','14-team']
position = ['quarterback','running-back','wide-receiver','tight-end','defense','kicker']
DIR_PATH = os.path.join(os.getcwd(), "scraper_data")

for yr in years:
    for lt in league_type:
        for ls in league_size:
            for pos in position:
                url = 'https://fantasyfootballcalculator.com/adp/{0}/{1}/{2}/{3}'.format(lt, ls, pos, yr)
                
                #csv_formatter = '{0}/{1}/{2}/{3}'.format(lt, ls, pos, yr)
                #csv_list.append(csv_formatter)

                requests.get(url)
                page = requests.get(url)

                soup = BeautifulSoup(page.text, 'lxml')
                table_data = soup.find('table', class_ ="table adp")

                headers = []
                for i in table_data.find_all('th'):
                    title = i.text
                    headers.append(title)


                df = pd.DataFrame(columns = headers)

                for j in table_data.find_all('tr')[1:]:
                    row_data = j.find_all('td')
                    row = [tr.text for tr in row_data]
                    length = len(df)
                    df.loc[length] = row
        
                FILE_PATH = os.path.join(DIR_PATH, "{0}-{1}-{2}-{3}.csv".format(lt, ls, pos, yr))
                df.to_csv(FILE_PATH)
    
