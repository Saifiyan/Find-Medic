# Generated by Django 3.1.1 on 2021-03-31 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210331_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='contno',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(max_length=50),
        ),
    ]