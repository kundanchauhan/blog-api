# Generated by Django 3.2.16 on 2022-12-09 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0004_createpost_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createpost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_details', to='blogapi.bloguser'),
        ),
    ]
