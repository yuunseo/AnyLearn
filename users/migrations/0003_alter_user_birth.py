# Generated by Django 4.2.4 on 2023-09-13 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
