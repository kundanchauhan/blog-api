# Generated by Django 3.2.16 on 2022-12-10 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0008_auto_20221210_0630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logger',
            name='user',
        ),
    ]
