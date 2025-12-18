import requests
from lxml import etree
import os
import  csv
import pandas as pd

class Spidermain():
    def __init__(self,city,):
        self.spiderUrl = 'https://lishi.tianqi.com/{}/{}.html'
        self.dateList = ['202301','202302','202303','202304','202305','202306','202307','202308','202309','202310','202311','202312']
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'
        }
        self.city = city

    def init(self):
        if not os.path.exists('./tempData.csv') :
            with open('./tempData.csv', "w",encoding='UTF-8',newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'averageHeight',
                    "averageSmall",
                    'mastHeight',
                    'masterSmall',
                    'averageAir',
                    'mastAir',
                    'lostAir',
                    'date',
                    'weekDay',
                    'mastHeightDay',
                    'mastSmallDay',
                    'wearther',
                    'wind',
                    'windOrder',
                    'city'
                ])

    def getUrl(self,date):
        df = pd.read_csv('./city.csv')
        city=df[df['city'].str.contains(self.city[:2])].url_values
        return self.spiderUrl.format(city[0].date)

    def main(self,url):
        respText = requests.get(url,headers=self.headers).text
        respXpath = etree.HTML(respText)