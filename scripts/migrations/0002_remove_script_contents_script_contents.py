# Generated by Django 4.2.4 on 2023-08-22 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
        ('scripts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='script',
            name='contents',
        ),
        migrations.AddField(
            model_name='script',
            name='contents',
            field=models.ManyToManyField(null=True, to='chats.roleplayingroom'),
        ),
    ]