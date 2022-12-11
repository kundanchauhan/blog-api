# Generated by Django 3.2.16 on 2022-12-10 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0009_remove_logger_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logger',
            old_name='blog',
            new_name='log',
        ),
        migrations.AddField(
            model_name='logger',
            name='action',
            field=models.CharField(choices=[('Created', 'Created'), ('Edited', 'Edited'), ('Deleted', 'Deleted')], max_length=50, null=True),
        ),
    ]
