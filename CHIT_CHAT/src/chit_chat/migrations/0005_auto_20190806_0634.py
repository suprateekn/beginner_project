# Generated by Django 2.2 on 2019-08-06 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chit_chat', '0004_message_sent_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='to_user',
            new_name='receiver',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='from_user',
            new_name='sender',
        ),
    ]
