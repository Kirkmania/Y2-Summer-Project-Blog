# Generated by Django 2.2.12 on 2020-08-22 03:10

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200822_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Text'),
        ),
    ]
