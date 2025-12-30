import os
import sys
import django
import csv

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Wheater_DjangoProject.settings')
django.setup()

from myApp.models import WeatherInfo

def import_data():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'spider', 'tempData.csv')

    if not os.path.exists(csv_path):
        print(f"错误: 文件不存在 {csv_path}")
        return

    # 清空现有数据
    WeatherInfo.objects.all().delete()
    print("已清空现有数据")

    # 读取并导入数据
    with open(csv_path, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            WeatherInfo.objects.create(
                averageHeight=row['averageHeight'],
                averageSmall=row['averageSmall'],
                mastHeight=row['mastHeight'],
                mastSmall=row['mastSmall'],
                averageAir=row['averageAir'],
                mastAir=row['mastAir'],
                lostAir=row['lostAir'],
                date=row['date'],
                weekDay=row['weekDay'],
                mastHeightDay=row['mastHeightDay'],
                mastSmallDay=row['mastSmallDay'],
                wearther=row['wearther'],
                wind=row['wind'],
                windOrder=row['windOrder'],
                city=row['city']
            )
            count += 1
            if count % 100 == 0:
                print(f"已导入 {count} 条数据...")

    print(f"导入完成! 总共导入 {count} 条数据")

if __name__ == '__main__':
    import_data()
