# Generated by Django 4.0.4 on 2022-04-18 06:28

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_applicationdesined_alter_desinedsite_desc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationdesined',
            name='desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AlterField(
            model_name='desinedsite',
            name='desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
    ]
