# Generated by Django 3.2.16 on 2022-12-09 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
