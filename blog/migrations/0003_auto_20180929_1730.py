# Generated by Django 2.0 on 2018-09-29 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180929_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avator',
            field=models.FileField(default=True, upload_to='avator/'),
        ),
    ]