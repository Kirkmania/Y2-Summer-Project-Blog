# Generated by Django 2.2.12 on 2020-08-24 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_cv', '0013_auto_20200824_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvlanguage',
            name='proficiency',
            field=models.CharField(choices=[('Elementary', 'Elementary'), ('Limited Working', 'Limited Working'), ('Professional Working', 'Professional Working'), ('Full Professional', 'Full Professional'), ('Native/Bilingual', 'Native/Bilingual')], default='1', max_length=100),
        ),
    ]