# Generated by Django 4.1.1 on 2022-11-17 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.BigIntegerField(default=0),
        ),
    ]
