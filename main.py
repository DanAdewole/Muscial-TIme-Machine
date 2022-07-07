import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
load_dotenv()
import pprint

pp = pprint.PrettyPrinter(indent=4)

# information
Billboard_URL = "https://www.billboard.com/charts/hot-100"
chrome_driver_path = "C:\\Development\\chromedriver_win32\\chromedriver.exe"
firefox_driver_path = "C:\\Development\\geckodriver.exe"


# VALIDATE THE INPUT THE USER IS BRINGING IN
time_travel_to = input("Which year do you want to travel to? Enter your in this format YYYY-MM-DD: ")
accepted_format = "%Y-%m-%S"
try:
    datetime.strptime(time_travel_to, accepted_format)
except ValueError:
    print("Try again")
    time_travel_to = input("Which year do you want to travel to? Enter your in this format YYYY-MM-DD: ")

options = Options()
options.headless = True

driver = webdriver.Firefox(executable_path=firefox_driver_path,)
driver.get(f"{Billboard_URL}/{time_travel_to}")

# Getting it from Selenium Directly

time.sleep(30)
extracted_song = driver.find_elements(By.ID, 'title-of-a-story')
song_title_text = [element.text for element in extracted_song]

song_list = list(filter(None, song_title_text))
song_title_list = [song_list[index] for index in range(100)]
# print(song_title_list)
print("\n")

extract_song_singers = driver.find_elements(By.CSS_SELECTOR, '.a-font-primary-s')
song_singers = [singer.text for singer in extract_song_singers]
singers_list = list(filter(None, song_singers))
top_100_singers = [singers_list[index] for index in range(100)]
# print(top_100_singers)

song_directory = {song_title_list[index]:top_100_singers[index]  for index in range(100)}
print(song_directory)

# driver.quit()

# ---------------------------- WORKING WITH THE SPOTIFY DATA ------------------------------------------------------- #
spotify_end_point = 'https://api.spotify.com/v1'

# SPOTIFY DETAILS
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
scope = "playlist-modify-private"
redirect_uri = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=redirect_uri,
        cache_path='token.txt',
        show_dialog=True,
    )
)

user_id = sp.current_user()['id']

year = time_travel_to.split("-")[0]

spotipy_song_uri = []
for song in song_directory:
    uri = sp.search(
        q=f"title:{song} year:{year}",
        limit=1,
        type="track",
    )

    try:
        song_uri = uri['tracks']['items'][0]['uri']
        spotipy_song_uri.append(f'{song}-{song_uri}')
    except IndexError:
        print(f"{song} not found. Skipped")
    except requests.exceptions.HTTPError:
        print(f"{song} not found too. Skipped")


print(spotipy_song_uri)



