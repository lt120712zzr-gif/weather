import re
import time

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
        city=df[df['city'].str.contains(self.city[:2])].url.values
        return self.spiderUrl.format(city[0],date)

    def main(self,url):
        respText = requests.get(url,headers=self.headers).text
        respXpath = etree.HTML(respText)
        monthInfo = respXpath.xpath("//div[@class='inleft_tian']/ul[@class='tian_two']/li")
        # averageHeight = re.search('-?\d+',monthInfo[0].xpath(".//div[@class='tian_twoa']")[0].text).group()
        averageHeight = re.search('-?\d+', monthInfo[0].xpath(".//div[contains(@class, 'tian_two')]")[0].text).group()
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
            wind = w.xpath("./div[@class='th140']")[3].text.split(' ')[0]
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
    def cleanData(self):
        df = pd.read_csv('./tempData.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        return df.values

    def writerRow(self,rowData):
        with open('./tempData.csv','a',encoding="UTF-8",newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(rowData)

if __name__ == '__main__':
    cityList=[
  {"province":"北京市","city":["北京市"]},
  {"province":"天津市","city":["天津市"]},
  {"province":"河北省","city":["石家庄市","唐山市","秦皇岛市","邯郸市","邢台市","保定市","张家口市","承德市","沧州市","廊坊市","衡水市"]},
  {"province":"山西省","city":["太原市","大同市","阳泉市","长治市","晋城市","朔州市","晋中市","运城市","忻州市","临汾市","吕梁市"]},
  {"province":"内蒙古自治区","city":["呼和浩特市","包头市","乌海市","赤峰市","通辽市","鄂尔多斯市","呼伦贝尔市","巴彦淖尔市","乌兰察布市","兴安盟","锡林郭勒盟","阿拉善盟"]},
  {"province":"辽宁省","city":["沈阳市","大连市","鞍山市","抚顺市","本溪市","丹东市","锦州市","营口市","阜新市","辽阳市","盘锦市","铁岭市","朝阳市","葫芦岛市"]},
  {"province":"吉林省","city":["长春市","吉林市","四平市","辽源市","通化市","白山市","松原市","白城市","延边朝鲜族自治州"]},
  {"province":"黑龙江省","city":["哈尔滨市","齐齐哈尔市","鸡西市","鹤岗市","双鸭山市","大庆市","伊春市","佳木斯市","七台河市","牡丹江市","黑河市","绥化市","大兴安岭地区"]},
  {"province":"上海市","city":["上海市"]},
  {"province":"江苏省","city":["南京市","无锡市","徐州市","常州市","苏州市","南通市","连云港市","淮安市","盐城市","扬州市","镇江市","泰州市","宿迁市"]},
  {"province":"浙江省","city":["杭州市","宁波市","温州市","嘉兴市","湖州市","绍兴市","金华市","衢州市","舟山市","台州市","丽水市"]},
  {"province":"安徽省","city":["合肥市","芜湖市","蚌埠市","淮南市","马鞍山市","淮北市","铜陵市","安庆市","黄山市","滁州市","阜阳市","宿州市","六安市","亳州市","池州市","宣城市"]},
  {"province":"福建省","city":["福州市","厦门市","莆田市","三明市","泉州市","漳州市","南平市","龙岩市","宁德市"]},
  {"province":"江西省","city":["南昌市","景德镇市","萍乡市","九江市","新余市","鹰潭市","赣州市","吉安市","宜春市","抚州市","上饶市"]},
  {"province":"山东省","city":["济南市","青岛市","淄博市","枣庄市","东营市","烟台市","潍坊市","济宁市","泰安市","威海市","日照市","临沂市","德州市","聊城市","滨州市","菏泽市"]},
  {"province":"河南省","city":["郑州市","开封市","洛阳市","平顶山市","安阳市","鹤壁市","新乡市","焦作市","濮阳市","许昌市","漯河市","三门峡市","南阳市","商丘市","信阳市","周口市","驻马店市","济源市"]},
  {"province":"湖北省","city":["武汉市","黄石市","十堰市","宜昌市","襄阳市","鄂州市","荆门市","孝感市","荆州市","黄冈市","咸宁市","随州市","恩施土家族苗族自治州"]},
  {"province":"湖南省","city":["长沙市","株洲市","湘潭市","衡阳市","邵阳市","岳阳市","常德市","张家界市","益阳市","郴州市","永州市","怀化市","娄底市","湘西土家族苗族自治州"]},
  {"province":"广东省","city":["广州市","韶关市","深圳市","珠海市","汕头市","佛山市","江门市","湛江市","茂名市","肇庆市","惠州市","梅州市","汕尾市","河源市","阳江市","清远市","东莞市","中山市","潮州市","揭阳市","云浮市"]},
  {"province":"广西壮族自治区","city":["南宁市","柳州市","桂林市","梧州市","北海市","防城港市","钦州市","贵港市","玉林市","百色市","贺州市","河池市","来宾市","崇左市"]},
  {"province":"海南省","city":["海口市","三亚市","三沙市","儋州市"]},
  {"province":"重庆市","city":["重庆市"]},
  {"province":"四川省","city":["成都市","自贡市","攀枝花市","泸州市","德阳市","绵阳市","广元市","遂宁市","内江市","乐山市","南充市","眉山市","宜宾市","广安市","达州市","雅安市","巴中市","资阳市","阿坝藏族羌族自治州","甘孜藏族自治州","凉山彝族自治州"]},
  {"province":"贵州省","city":["贵阳市","六盘水市","遵义市","安顺市","毕节市","铜仁市","黔西南布依族苗族自治州","黔东南苗族侗族自治州","黔南布依族苗族自治州"]},
  {"province":"云南省","city":["昆明市","曲靖市","玉溪市","保山市","昭通市","丽江市","普洱市","临沧市","楚雄彝族自治州","红河哈尼族彝族自治州","文山壮族苗族自治州","西双版纳傣族自治州","大理白族自治州","德宏傣族景颇族自治州","怒江傈僳族自治州","迪庆藏族自治州"]},
  {"province":"西藏自治区","city":["拉萨市","日喀则市","昌都市","林芝市","山南市","那曲市","阿里地区"]},
  {"province":"陕西省","city":["西安市","铜川市","宝鸡市","咸阳市","渭南市","延安市","汉中市","榆林市","安康市","商洛市"]},
  {"province":"甘肃省","city":["兰州市","嘉峪关市","金昌市","白银市","天水市","武威市","张掖市","平凉市","庆阳市","定西市","陇南市","临夏回族自治州","甘南藏族自治州"]},
  {"province":"青海省","city":["西宁市","海东市","海北藏族自治州","黄南藏族自治州","海南藏族自治州","果洛藏族自治州","玉树藏族自治州","海西蒙古族藏族自治州"]},
  {"province":"宁夏回族自治区","city":["银川市","石嘴山市","吴忠市","固原市","中卫市"]},
  {"province":"新疆维吾尔自治区","city":["乌鲁木齐市","克拉玛依市","吐鲁番市","哈密市","昌吉回族自治州","博尔塔拉蒙古自治州","巴音郭楞蒙古自治州","阿克苏地区","克孜勒苏柯尔克孜自治州","喀什地区","和田地区","伊犁哈萨克自治州","塔城地区","阿勒泰地区"]},
  {"province":"香港特别行政区","city":["香港"]},
  {"province":"澳门特别行政区","city":["澳门","离岛"]},
  {"province":"台湾省","city":["台北市","高雄市","台中市","台南市","新北市","桃园市","台东县","宜兰县","新竹县","苗栗县","彰化县","南投县","云林县","嘉义县","屏东县","花莲县","澎湖县","基隆市","新竹市","嘉义市","金门县","连江县"]}
]
    for item in cityList:
        city=item['city'][0]
        spiderMainObj = Spidermain(city)
        spiderMainObj.init()
        for i in spiderMainObj.dateList:
            print('正则爬取'+i+'的天气')
            spiderUrl=spiderMainObj.getUrl(i)
            print(spiderUrl)
            spiderMainObj.main(spiderUrl)
            time.sleep(10)