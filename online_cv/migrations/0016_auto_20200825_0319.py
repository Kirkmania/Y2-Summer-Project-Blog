# Generated by Django 2.2.13 on 2020-08-25 02:19

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_cv', '0015_auto_20200825_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvskill',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='cvworkhistory',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]