# Generated by Django 4.2.4 on 2023-08-22 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
        ('scripts', '0002_remove_script_contents_script_contents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='script',
            name='contents',
        ),
        migrations.AddField(
            model_name='script',
            name='contents',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scripts', to='chats.roleplayingroom'),
        ),
    ]
