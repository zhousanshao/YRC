# Generated by Django 4.2.19 on 2025-03-03 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Honor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('motto', models.CharField(max_length=200, verbose_name='格言')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='honors/', verbose_name='照片')),
                ('honor_type', models.CharField(choices=[('百万俱乐部', '百万俱乐部'), ('王者战队', '王者战队'), ('飞跃之星', '飞跃之星')], max_length=50, verbose_name='荣誉类型')),
                ('date_achieved', models.DateField(verbose_name='获得日期')),
            ],
            options={
                'verbose_name': '荣誉信息',
                'verbose_name_plural': '荣誉信息',
            },
        ),
    ]
