# Generated by Django 4.1.7 on 2023-02-18 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0016_question_image_question_image_alt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compliment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300, unique=True)),
                ('difficulty', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)),
            ],
        ),
    ]