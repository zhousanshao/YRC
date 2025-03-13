#定义模型
from django.db import models

class SalesData(models.Model):
    name = models.CharField(max_length=50, verbose_name="销售人员姓名")
    daily_sales = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="当天业绩")
    monthly_sales = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="当月业绩")
    date = models.DateField(verbose_name="日期")

    class Meta:
        verbose_name = "销售数据"
        verbose_name_plural = "销售数据"

    def __str__(self):
        return f"{self.name} - {self.date}"


class Honor(models.Model):
    HONOR_CHOICES = [
        ('百万俱乐部', '百万俱乐部'),
        ('王者战队', '王者战队'),
        ('飞跃之星', '飞跃之星'),
    ]

    name = models.CharField(max_length=100, verbose_name="姓名")
    motto = models.CharField(max_length=200, verbose_name="格言")
    photo = models.ImageField(upload_to='honors/', null=True, blank=True, verbose_name="照片")
    honor_type = models.CharField(max_length=50, choices=HONOR_CHOICES, verbose_name="荣誉类型")
    date_achieved = models.DateField(verbose_name="获得日期")

    class Meta:
        verbose_name = "荣誉信息"
        verbose_name_plural = "荣誉信息"

    def __str__(self):
        return f"{self.name} - {self.honor_type}"