# Generated by Django 2.2.1 on 2021-05-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_auto_20210530_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='chapter',
            field=models.CharField(default=1, max_length=233),
            preserve_default=False,
        ),
    ]
