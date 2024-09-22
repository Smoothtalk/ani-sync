from django.core.management import call_command

def run_sync_command():
    call_command('sync_anime_myo')