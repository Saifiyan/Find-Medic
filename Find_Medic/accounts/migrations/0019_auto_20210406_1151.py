# Generated by Django 3.1.1 on 2021-04-06 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_patientdetails_nowdatetime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctorprofile',
            options={'ordering': ('city',)},
        ),
        migrations.AddField(
            model_name='patientdetails',
            name='doctorname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
