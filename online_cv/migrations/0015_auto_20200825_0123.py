# Generated by Django 2.2.13 on 2020-08-25 00:23

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_cv', '0014_auto_20200824_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvinterest',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
