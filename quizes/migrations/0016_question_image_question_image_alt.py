# Generated by Django 4.1.5 on 2023-02-17 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0015_quiz_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='book-images/'),
        ),
        migrations.AddField(
            model_name='question',
            name='image_alt',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
    ]