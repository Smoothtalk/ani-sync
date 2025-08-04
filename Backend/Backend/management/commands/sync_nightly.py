from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import requests

User = get_user_model()

class Command(BaseCommand):
    help = 'Calls anilist/get_anime_list/'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, help='Username of the person triggering the sync')

    def handle(self, *args, **kwargs):

        username = kwargs['user']
        user = None

        if username:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(self.style.NOTICE(f"Running nightly update as user: {user.username}"))
            except User.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"User {username} does not exist"))
                return

        self.stdout.write(self.style.WARNING('Starting to update data...'))

        update_anime = requests.get(f'http://localhost:8000/anilist/get_anime_list/?username={username}')
        anime_data = update_anime.json()

        self.stdout.write(self.style.SUCCESS(f'Done updating Anime of {username}'))

