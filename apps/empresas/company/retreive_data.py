from datetime import datetime

import requests
import yahooquery as yq
import yfinance as yf
from django.conf import settings

FINHUB_TOKEN = settings.FINHUB_TOKEN

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}


class RetreiveCompanyData:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
    
    def get_current_price(self):
        current_price = 0
        current_currency = 'None'

        try:
            company_info = yf.Ticker(self.ticker).info
            if 'currentPrice' in company_info:
                current_price = company_info['currentPrice']
                current_currency = company_info['currency']
            else:
                company_info = yq.Ticker(self.ticker).financial_data
                if 'currentPrice' in company_info:
                    current_price = company_info['currentPrice']
                    current_currency = company_info['financialCurrency']

        except Exception as e:
            current_price, current_currency = self.scrap_price_yahoo()
        
        return {
            'current_price': current_price,
            'current_currency': current_currency,
        }

    def scrap_price_yahoo(self):
        url_current_price = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker}'
        current_price_jsn = requests.get(url_current_price, headers=headers).json()['chart']['result']
        current_price = [infos['meta']['regularMarketPrice'] for infos in current_price_jsn][0]
        current_currency = [infos['meta']['currency'] for infos in current_price_jsn][0]

        return current_price, current_currency
    
    def get_news(self):
        day = str(int(datetime.now().strftime("%Y-%m-%d")[-2:])-2)
        final_date = (datetime.now().strftime(f"%Y-%m-{day}"))
        return requests.get(f'https://finnhub.io/api/v1/company-news?symbol={self.ticker}&from={final_date}&to={datetime.now().strftime("%Y-%m-%d")}&token={FINHUB_TOKEN}').json()

    
            
            
            
