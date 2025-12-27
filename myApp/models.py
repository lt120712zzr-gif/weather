from django.db import models

# Create your models here.
class User(models.Model):
    id=models.AutoField('id',primary_key=True)
    username = models.CharField("用户名",max_length=255,default="")
    password = models.CharField("密码",max_length=255,default="")
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    class Meta:
        db_table = 'user'


class WeatherInfo(models.Model):
    id=models.AutoField("id",primary_key=True)
    averageHeight = models.CharField("月平均高温",max_length=255,default="")
    averageSmall = models.CharField("月平均低温", max_length=255, default="")
    mastHeight = models.CharField("月最低高温", max_length=255, default="")
    mastSmall = models.CharField("月最高低温", max_length=255, default="")
    averageAir = models.CharField("平均空气质量", max_length=255, default="")
    mastAir = models.CharField("最高空气质量", max_length=255, default="")
    lostAir = models.CharField("最低空气质量", max_length=255, default="")
    date = models.CharField("日期", max_length=255, default="")
    weekDay = models.CharField("星期", max_length=255, default="")
    mastHeightDay = models.CharField("日高温", max_length=255, default="")
    mastSmallDay = models.CharField("日低温", max_length=255, default="")
    wearther = models.CharField("天气", max_length=255, default="")
    wind = models.CharField("风向", max_length=255, default="")
    windOrder = models.CharField("风力", max_length=255, default="")
    city = models.CharField("城市", max_length=255, default="")

    class Meta:
        db_table = 'weatherinfo'

class City(models.Model):
    id=models.AutoField("id",primary_key=True)
    city = models.CharField("城市名", max_length=255, default="")
    url = models.CharField("城市参数", max_length=255, default="")

    class Meta:
        db_table = 'city'


class Part1(models.Model):
    mastHeight = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    mastSmall = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    date =models.DateField(null=True,blank=True)

    class Meta:
        db_table = 'part1'


class Part2(models.Model):
    averageHeight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    averageSmall = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'part2'

class Part3(models.Model):
    mastAir = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lostAir = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'part3'


class Part4(models.Model):

    averageAir = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'part4'

class Part5(models.Model):
    windOrder = models.CharField( max_length=10, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'part5'