# Generated by Django 4.1.5 on 2023-01-20 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0014_alter_question_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
