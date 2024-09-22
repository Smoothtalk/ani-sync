# Backend/management/commands/schedule_sync.py

from django.core.management.base import BaseCommand
from django_q.tasks import schedule
from Backend.tasks import run_sync_command  # Import the task function

class Command(BaseCommand):
    help = 'Schedules the sync_anime_myo task every 30 minutes'

    def handle(self, *args, **kwargs):
        # Check if the task is already scheduled
        from django_q.models import Schedule
        if not Schedule.objects.filter(name='sync_anime_myo').exists():
            # Schedule the task
            schedule(
                func='Backend.tasks.run_sync_command',  # Fully qualified path to the function
                schedule_type='I',  # Interval-based
                minutes=30,  # Every 30 minutes
                repeats=-1,  # Repeat indefinitely
                name='sync_anime_myo'  # Unique name for this schedule
            )
            self.stdout.write(self.style.SUCCESS('Scheduled sync_anime_myo successfully!'))
        else:
            self.stdout.write(self.style.WARNING('sync_anime_myo is already scheduled.'))
