# Generated by Django 4.0.4 on 2022-04-14 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_desinedsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationDesined',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('url', models.URLField(verbose_name='url')),
                ('image', models.ImageField(upload_to='uploads/desinedsite', verbose_name='image')),
                ('desc', models.TextField(verbose_name='description')),
                ('plat', models.CharField(default='android', max_length=50, verbose_name='platform')),
            ],
        ),
        migrations.AlterField(
            model_name='desinedsite',
            name='desc',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='desinedsite',
            name='image',
            field=models.ImageField(upload_to='uploads/desinedsite', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='desinedsite',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='desinedsite',
            name='url',
            field=models.URLField(verbose_name='url'),
        ),
    ]
