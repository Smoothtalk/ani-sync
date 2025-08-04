# Backend/management/commands/schedule_sync.py

from django.core.management.base import BaseCommand
from django_q.tasks import schedule
from Backend.tasks import run_nightly_command  # Import the task function

class Command(BaseCommand):
    help = 'Updates Anime Airing Status and User_Anime progress everyday at 11:59'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            required=True,
            help='Username to run the nightly update for'
        )

    def handle(self, *args, **kwargs):
        sync_username = kwargs['user']
        run_nightly_name = f'run_nightly_{sync_username}'

        # Check if the task is already scheduled
        from django_q.models import Schedule
        if not Schedule.objects.filter(name='run_nightly').exists():
            # Schedule the task
            schedule(
                func='Backend.tasks.run_nightly_command',  # Fully qualified path to the function
                schedule_type='D',  # Interval-based
                repeats=-1,  # Repeat indefinitely
                name=run_nightly_name,  # Unique name for this schedule
                sync_user=sync_username 
            )
            self.stdout.write(self.style.SUCCESS('Added Anime and User Anime task for {sync_username} successfully!'))
        else:
            self.stdout.write(self.style.WARNING('run_nightly is already scheduled.'))
