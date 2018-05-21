from bs4 import BeautifulSoup
import requests
import urllib.request
import shutil
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('albumurl')
args = parser.parse_args()

album_url = args.albumurl

def get_file(track_url):
	track_name = urllib.request.unquote(track_url.split("/")[-1]).replace('%20', ' ')
	print(f'Getting {track_name}... ', end='')

	with urllib.request.urlopen(track_url) as response, open(track_name, 'wb') as file:
		shutil.copyfileobj(response, file)

	print('Done.')

def get_track_urls(album_url):
	print('Extracting track urls... ', end='')

	soup = BeautifulSoup(requests.get(album_url).text, 'html.parser')
	track_table = soup.find('table', id='songlist')
	links = [ 'https://downloads.khinsider.com' + link['href'] for link in track_table.find_all('a') ]
	links = sorted(list(set(links)))

	for link in links:
		soup = BeautifulSoup(requests.get(link).text, 'html.parser')
		file_url = soup.find('a', text="Click here to download as MP3")["href"]

	print(f'{len(links)} track urls retrieved.')
	return links

for track_url in get_track_urls(album_url):
	get_file(track_url)
