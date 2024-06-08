import requests
from bs4 import BeautifulSoup
import os
import re
import time

# Define the URL to scrape
base_url = "https://leagueoflegends.fandom.com"
champions_url = "https://leagueoflegends.fandom.com/wiki/User_blog:Rifqikimen/Champions/Splash_Arts"

# Define the directory to save images
save_dir = "champion_splash_arts"
os.makedirs(save_dir, exist_ok=True)

# Function to download an image from a direct URL
def download_image_direct(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        # print(f"Saved image to {save_path}")
    else:
        print(f"Failed to retrieve image from {url}")

# Fetch the champions page
response = requests.get(champions_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all instances of "Original {ChampName}"
for tag in soup.find_all(string=lambda text: text and "Original" in text):
    if "Original" in tag:
        champ_name = tag.replace("Original", "").strip()

        # Handle exceptions for special champions
        if champ_name == "K'Sante":
            champ_name = "KSante"
        elif champ_name == "Kog'Maw":
            champ_name = "KogMaw"
        elif champ_name == "LeBlanc":
            champ_name = "Leblanc"
        elif champ_name == "Rek'Sai":
            champ_name = "RekSai"
        elif champ_name == "Renata Glasc":
            champ_name = "Renata"
        elif champ_name == "Wukong":
            champ_name = "MonkeyKing"

        # Handle exceptions for apostrophes and capitalization
        if "'" in champ_name:
            champ_name = champ_name.replace("'", "")
            champ_name = champ_name[0].upper() + champ_name[1:].lower()
        elif "." in champ_name:
            champ_name = champ_name.replace(".", "")

        # Remove spaces from champ_name
        champ_name = champ_name.replace(" ", "")
        
        # Construct the image URL
        image_url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ_name}_0.jpg"
        
        # Define the path to save the image
        save_path = os.path.join(save_dir, f"{champ_name}.jpg")
        
        # Download the image
        download_image_direct(image_url, save_path)

