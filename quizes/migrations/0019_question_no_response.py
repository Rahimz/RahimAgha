# Generated by Django 4.1.7 on 2023-03-14 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0018_alter_compliment_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='no_response',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
