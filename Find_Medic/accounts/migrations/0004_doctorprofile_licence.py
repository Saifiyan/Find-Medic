# Generated by Django 3.1.1 on 2021-03-30 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_doctorprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='licence',
            field=models.FileField(null=True, upload_to='doclicence'),
        ),
    ]
