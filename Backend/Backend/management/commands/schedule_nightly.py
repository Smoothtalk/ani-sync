# Backend/management/commands/schedule_sync.py

from django.core.management.base import BaseCommand
from django_q.tasks import schedule
from Backend.tasks import run_nightly_command  # Import the task function

class Command(BaseCommand):
    help = 'Updates Anime Airing Status and User_Anime progress everyday at 11:59'

    def handle(self, *args, **kwargs):
        # Check if the task is already scheduled
        from django_q.models import Schedule
        if not Schedule.objects.filter(name='run_nightly').exists():
            # Schedule the task
            schedule(
                func='Backend.tasks.run_nightly_command',  # Fully qualified path to the function
                schedule_type='D',  # Interval-based
                repeats=-1,  # Repeat indefinitely
                name='run_nightly'  # Unique name for this schedule
            )
            self.stdout.write(self.style.SUCCESS('Added Anime and User Anime task successfully!'))
        else:
            self.stdout.write(self.style.WARNING('run_nightly is already scheduled.'))
