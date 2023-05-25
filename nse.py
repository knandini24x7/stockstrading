import requests
import pandas as pd
from datetime import datetime
from io import BytesIO

class NSE():
    def __init__(self, timeout=10):
        self.base_url = 'https://www.nseindia.com'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9"
        }
        self.timeout = timeout
        self.cookies = []
    
    def __getCookies(self, renew=False):
        if len(self.cookies) > 0 and renew == False:
            return self.cookies

        r = requests.get(self.base_url, timeout=self.timeout, headers=self.headers)
        self.cookies = dict(r.cookies)
        return self.__getCookies()
    
    def getHistoricalData(self, symbol, series, from_date, to_date):
        try:
            url = "/api/historical/cm/equity?symbol={0}&series=[%22{1}%22]&from={2}&to={3}&csv=true".format(symbol.replace('&', '%26'), series, from_date.strftime('%d-%m-%Y'), to_date.strftime('%d-%m-%Y'))
            r = requests.get(self.base_url + url, headers=self.headers, timeout=self.timeout, cookies=self.__getCookies())
            if r.status_code != 200:
                r = requests.get(self.base_url + url, headers=self.headers, timeout=self.timeout, cookies=self.__getCookies(True))
            
            df = pd.read_csv(BytesIO(r.content), sep=',', thousands=',')
            df = df.rename(columns={'Date ': 'date', 'series ': 'series', 'OPEN ': 'open', 'HIGH ': 'high', 'LOW ': 'low', 'PREV. CLOSE ': 'prev_close', 'ltp ': 'ltp', 'close ': 'close', '52W H ': 'hi_52_wk', '52W L ': 'lo_52_wk', 'VOLUME ': 'trdqty', 'VALUE ': 'trdval', 'No of trades ': 'trades'})
            df.date = pd.to_datetime(df.date).dt.strftime('%Y-%m-%d')
            return df
        except:
            return None


if __name__ == '__main__':
    from datetime import date
    from nse import NSE
    nse = NSE()
    df = nse.getHistoricalData('SBIN', 'EQ', date(2023,1,1), date(2023,5,20))
    print(df)
