import os
import csv
from django.core.management.base import BaseCommand
from myApp.models import WeatherInfo


class Command(BaseCommand):
    help = '从 CSV 文件导入天气数据到数据库'

    def handle(self, *args, **options):
        # 获取 CSV 文件路径
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(base_dir, 'spider', 'tempData.csv')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"错误: 文件不存在 {csv_path}"))
            return

        # 清空现有数据
        WeatherInfo.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("已清空现有数据"))

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
                    self.stdout.write(f"已导入 {count} 条数据...")

        self.stdout.write(self.style.SUCCESS(f"导入完成! 总共导入 {count} 条数据"))
