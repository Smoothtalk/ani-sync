from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import requests

User = get_user_model()

class Command(BaseCommand):
    help = 'Calls get_mag_links, get_downloads, download_releases'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, help='Username of the person triggering the sync')

    def handle(self, *args, **kwargs):

        username = kwargs['user']
        user = None

        if username:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(self.style.NOTICE(f"Running sync as user: {user.username}"))
            except User.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"User {username} does not exist"))
                return

        # your main sync logic here
        # optionally log user if needed

        self.stdout.write(self.style.SUCCESS('Starting to fetch data...'))

        get_magnet_links = requests.get('http://localhost:8000/subsplease/get_magnet_links/')
        magnet_links_data = get_magnet_links.json()

        self.stdout.write(self.style.WARNING('Done getting magnet links'))

        get_releases = requests.get('http://localhost:8000/transmission/get_downloads/')
        release_data = get_releases.json()

        self.stdout.write(self.style.WARNING('Done getting setting up releases'))

        download_releases = requests.get('http://localhost:8000/transmission/download_releases/')
        download_data = download_releases.json()

        self.stdout.write(self.style.WARNING('Done downloading releases'))

        # response2 = requests.get('http://localhost:8000/transmission/get_downloads/', params={'key': magnet_links_data.get('some_key')})
        # data2 = response2.json()

        # response3 = requests.post('http://localhost:8000/transmission/download_releases/', json={'key': data2.get('some_other_key')})
        # data3 = response3.json()

        for download in download_data:            
            self.stdout.write(self.style.SUCCESS(f'Synced {download["release_title"]} to {user.username} successfully'))
        
        self.stdout.write(self.style.SUCCESS(f'Completed fetching Anime for {user.username}'))

