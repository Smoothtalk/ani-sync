from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    help = 'Calls anilist/get_anime_list/'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting to update data...'))

        update_anime = requests.get('http://localhost:8000/anilist/get_anime_list/?username=Myo')
        anime_data = update_anime.json()

        self.stdout.write(self.style.SUCCESS('Done updating Anime'))
    

