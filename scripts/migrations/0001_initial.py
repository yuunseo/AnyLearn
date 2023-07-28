# Generated by Django 4.2.3 on 2023-07-27 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('contents', models.TextField()),
                ('level', models.CharField(choices=[('level1', 'Level1'), ('level2', 'Level2'), ('level3', 'Level3')], max_length=10)),
                ('learningDate', models.DateField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scripts', to=settings.AUTH_USER_MODEL)),
                ('hashtag', models.ManyToManyField(to='scripts.tag')),
            ],
        ),
    ]