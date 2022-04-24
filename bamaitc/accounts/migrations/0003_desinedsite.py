# Generated by Django 4.0.4 on 2022-04-14 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesinedSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='')),
                ('url', models.URLField(verbose_name='')),
                ('image', models.ImageField(upload_to='uploads/desinedsite', verbose_name='')),
                ('desc', models.TextField(verbose_name='')),
            ],
        ),
    ]
