# Generated by Django 2.2.12 on 2020-08-22 03:10

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('online_cv', '0006_auto_20200822_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cv',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='Auto default text', verbose_name='text'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cvprofile',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Personal Statement'),
        ),
        migrations.AlterField(
            model_name='cvworkhistory',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='Auto default text', verbose_name='Description'),
            preserve_default=False,
        ),
    ]