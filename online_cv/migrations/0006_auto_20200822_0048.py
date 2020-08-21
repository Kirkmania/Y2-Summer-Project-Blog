# Generated by Django 2.2.12 on 2020-08-21 23:48

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_cv', '0005_cvworkhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cveducation',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cvprofile',
            name='text',
            field=ckeditor.fields.RichTextField(default="Silly billy didn't write anything here!"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cvworkhistory',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
