# Generated by Django 4.1.1 on 2022-11-15 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='coment',
            new_name='post',
        ),
    ]
