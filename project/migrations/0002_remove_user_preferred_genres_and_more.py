# Generated by Django 5.1.3 on 2024-12-07 00:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='preferred_genres',
        ),
        migrations.RemoveField(
            model_name='user',
            name='shown_profiles',
        ),
        migrations.CreateModel(
            name='UserGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_genres', to='project.genre')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_genres', to='project.user')),
            ],
            options={
                'unique_together': {('user', 'genre')},
            },
        ),
    ]
