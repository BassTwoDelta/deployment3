# Generated by Django 2.2.4 on 2020-06-22 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='name', max_length=100),
        ),
    ]