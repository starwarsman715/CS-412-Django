# Generated by Django 5.1.3 on 2024-12-06 23:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShownProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=200)),
                ('release_year', models.PositiveIntegerField()),
                ('spotify_url', models.URLField()),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='project.genre')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('birth_date', models.DateField()),
                ('bio', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('preferred_genres', models.ManyToManyField(related_name='users', to='project.genre')),
                ('shown_profiles', models.ManyToManyField(related_name='shown_to', through='project.ShownProfile', to='project.user')),
            ],
        ),
        migrations.AddField(
            model_name='shownprofile',
            name='shown_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shown_to_users', to='project.user'),
        ),
        migrations.AddField(
            model_name='shownprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shown_profiles_records', to='project.user'),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_matches', to='project.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_matches', to='project.user')),
            ],
            options={
                'unique_together': {('sender', 'receiver')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='project.match')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_comments', to='project.user')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='shownprofile',
            unique_together={('user', 'shown_profile')},
        ),
        migrations.CreateModel(
            name='UserSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_songs', to='project.song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_songs', to='project.user')),
            ],
            options={
                'unique_together': {('user', 'song')},
            },
        ),
    ]