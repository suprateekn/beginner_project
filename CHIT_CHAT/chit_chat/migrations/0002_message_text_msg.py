# Generated by Django 2.2 on 2019-08-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chit_chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='text_msg',
            field=models.TextField(blank=True, null=True),
        ),
    ]