# Generated by Django 4.1.5 on 2023-01-19 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0009_quizresponse_step'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ('created',)},
        ),
    ]
