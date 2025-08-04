from django.core.management import call_command

def run_sync_command(sync_user=None):
    call_command('sync_anime', user=sync_user)

def run_nightly_command(sync_user=None):
    call_command('sync_nightly', user=sync_user)