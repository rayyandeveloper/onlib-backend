# Generated by Django 4.2.3 on 2023-07-22 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='groups',
            new_name='group',
        ),
    ]
