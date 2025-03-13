# Generated by Django 4.2.19 on 2025-02-27 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SalesData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='销售人员姓名')),
                ('daily_sales', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='当天业绩')),
                ('monthly_sales', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='当月业绩')),
                ('date', models.DateField(verbose_name='日期')),
            ],
            options={
                'verbose_name': '销售数据',
                'verbose_name_plural': '销售数据',
            },
        ),
    ]
