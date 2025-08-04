# Backend/management/commands/schedule_sync.py

from django.core.management.base import BaseCommand
from django_q.tasks import schedule
from Backend.tasks import run_sync_command  # Import the task function

class Command(BaseCommand):
    help = 'Schedules the sync_anime_myo task every 30 minutes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            required=True,
            help='Username to run the sync for'
        )

    def handle(self, *args, **kwargs):
        sync_username = kwargs['user']
        sync_anime_name = f'sync_anime_{sync_username}'

        # Check if the task is already scheduled
        from django_q.models import Schedule
        if not Schedule.objects.filter(name='sync_anime').exists():
            # Schedule the task
            schedule(
                func='Backend.tasks.run_sync_command',  # Fully qualified path to the function
                schedule_type='I',  # Interval-based
                minutes=30,  # Every 30 minutes
                repeats=-1,  # Repeat indefinitely
                name=sync_anime_name,  # Unique name for this schedule
                sync_user=sync_username 
            )
            self.stdout.write(self.style.SUCCESS('Scheduled sync_anime_{sync_username} successfully!'))
        else:
            self.stdout.write(self.style.WARNING('sync_anime_{sync_username} is already scheduled.'))
