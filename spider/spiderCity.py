import requests
from lxml import etree
import os
import  csv
import pandas as pd

class Spider():
    def __init__(self):
        self.spiderUrl='https://lishi.tianqi.com/'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'
        }

    def init(self):
        if not os.path.exists("./city.csv"):
            with open('./city.csv', 'w',encoding="UTF-8", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['city','url'])

    def mian(self):
        response = requests.get(self.spiderUrl,headers=self.headers).text
        respXpath = etree.HTML(response)
        table=respXpath.xpath('//div[@class="tablebox"]/table/tbody')[0]
        citys=table.xpath('.//tr/td/ul/li/a')
        for city in citys:
            cityName=city.text
            url=city.get('href').split('/')[1] if len(city.get('href').split('/'))==3 else city.get('href').split('/')[0]
            print(cityName,url)
            self.witerRow([cityName,url])


    def witerRow(self,rowData):
        with open('./city.csv','a',encoding="UTF-8",newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(rowData)

    def cleanData(self):
        df = pd.read_csv('./city.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        print("数据为%d"%df.shape[0])
        return df.values

if __name__ == '__main__':
    spider=Spider()
    spider.mian()