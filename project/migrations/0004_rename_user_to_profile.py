# Generated manually
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('project', '0003_rename_spotify_url_song_youtube_url'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Profile',
        ),
        migrations.RenameField(
            model_name='usergenre',
            old_name='user',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='usersong',
            old_name='user',
            new_name='profile',
        ),
        migrations.RenameField(
            model_name='shownprofile',
            old_name='user',
            new_name='profile',
        ),
    ]