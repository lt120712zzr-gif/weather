import re

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
        monthInfo = respXpath.xpath("//div[@class='inleft_tian']/ul[@class='tian_two']/li")
        averageHeight = re.search('-?\d+',monthInfo[0].xpath(".//div[@class='tian_twoa']")[0].text).group()
        averageSmall = re.search('-?\d+',monthInfo[0].xpath(".//div[@class='tian_twoa']")[1].text).group()
        mastHeight = re.search('-?\d+',monthInfo[1].xpath(".//div[@class='tian_twoa']")[0].text).group()
        try:
            mastSmall = re.search('-?\d+',monthInfo[2].xpath(".//div[@class='tian_twoa']")[0].text).group()
        except:
            mastSmall = 0
        averageAir = monthInfo[3].xpath(".//div[@class='tian_twoa']")[0].text
        mastAir = monthInfo[4].xpath(".//div[@class='tian_twoa']")[0].text
        lostAir = monthInfo[5].xpath(".//div[@class='tian_twoa']")[0].text

        weatherList = respXpath.xpath("//ul[@class='thrui']/li")
        for w in weatherList:
            date = w.xpath("./div[@class='th200']")[0].text.split(' ')[0]
            weekDay = w.xpath("./div[@class='th200']")[0].text.split(' ')[1]
            try:
                mastHeightDay = re.search('-?\d+', w.xpath("./div[@class='th140']")[0].text).group()
            except:
                mastHeightDay = 0
            try:
                mastSmallDay = re.search('-?\d+', w.xpath("./div[@class='th140']")[1].text).group()
            except:
                mastSmallDay = 0
            try:
                wearther =  w.xpath("./div[@class='th140']")[2].text
            except:
                wearther = '晴'
            wind = w.xpath("./div[@class='th200']")[3].text.split(' ')[0]
            try:
               windOrder = re.search('-?\d+', w.xpath("./div[@class='th140']")[3].text.split(' ')[1]).group()
            except:
                windOrder = 3
            self.writerRow([
                averageHeight,
                averageSmall,
                mastHeight,
                mastSmall,
                averageAir,
                mastAir,
                lostAir,
                date,
                weekDay,
                mastHeightDay,
                mastSmallDay,
                wearther,
                wind,
                windOrder,
                self.city.replace('市','')
            ])