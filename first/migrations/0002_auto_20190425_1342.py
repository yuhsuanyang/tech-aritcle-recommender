# Generated by Django 2.1.7 on 2019-04-25 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='link',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.TextField(),
        ),
    ]
