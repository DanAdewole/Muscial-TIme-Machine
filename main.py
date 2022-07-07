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

# information
Billboard_URL = "https://www.billboard.com/charts/hot-100"
chrome_driver_path = "C:\\Development\\chromedriver_win32\\chromedriver.exe"
firefox_driver_path = "C:\\Development\\geckodriver.exe"

# SPOTIFY DETAILS
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

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
top_100 = [song_list[index] for index in range(100)]
# print(top_100)
print("\n")

extract_song_singers = driver.find_elements(By.CSS_SELECTOR, '.a-font-primary-s')
song_singers = [singer.text for singer in extract_song_singers]
singers_list = list(filter(None, song_singers))
top_100_singers = [singers_list[index] for index in range(100)]
# print(top_100_singers)

song_directory = {top_100[index]:top_100_singers[index]  for index in range(100)}
print(song_directory)

# driver.quit()

# ---------------------------- WORKING WITH THE SPOTIFY DATA ------------------------------------------------------- #
# scope = "user-library-read"

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
