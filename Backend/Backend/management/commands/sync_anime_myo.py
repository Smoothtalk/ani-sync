from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    help = 'Calls get_mag_links, get_downloads, download_releases'

    def handle(self, *args, **kwargs):
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
            self.stdout.write(self.style.SUCCESS(f'Synced {download['release_title']} to Myo successfully'))
        
        self.stdout.write(self.style.SUCCESS('Completed fetching'))

