# Generated by Django 4.1.5 on 2023-01-12 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
