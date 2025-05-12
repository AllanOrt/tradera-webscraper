# Licensed under the MIT License. See LICENSE file in the project root for full license information.

import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://www.tradera.com/category/1000242?af-computer_retro=Datorer%20%26%20sk%C3%A4rmar&itemType=FixedPrice&sellerType=All&sortBy=AddedOn"
SEEN_FILE = "latest_ad.txt"

def load_seen_url():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_seen_url(url):
    with open(SEEN_FILE, "w") as f:
        f.write(url)

def parse_site(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_latest_ad():
    soup = parse_site(URL)
    ad_elems = soup.find_all("div", class_="item-card-inner-wrapper")
    latest_ad = ad_elems[0]

    # find name, url, price, img
    try:
        ad_name = latest_ad.find("a", class_="button_button__bmQqK button_theme__kbDOb button_theme-link__y9e_l button_linkReverted__IwTuC text-left text-truncate-one-line text-inter-light").text
        ad_url = latest_ad.find("a", class_="button_button__bmQqK button_theme__kbDOb button_theme-link__y9e_l button_linkReverted__IwTuC text-left text-truncate-one-line text-inter-light")['href']
    except:
        ad_name = latest_ad.find("a", class_="button_button__bmQqK button_theme__kbDOb button_theme-link__y9e_l button_linkReverted__IwTuC text-left text-truncate-two-lines text-inter-light").text
        ad_url = latest_ad.find("a", class_="button_button__bmQqK button_theme__kbDOb button_theme-link__y9e_l button_linkReverted__IwTuC text-left text-truncate-two-lines text-inter-light")['href']

    ad_url = f"https://www.tradera.com{ad_url}"
    ad_price = latest_ad.find("span", class_="text-nowrap font-weight-bold font-hansen pr-1").text
    ad_img = latest_ad.find("img", class_="item-card-image_fill-aspect-ratio__fgi0B item-card-image_primary-image__i8LZ_")['src']

    return ad_name, ad_url, ad_price, ad_img


ad_name, ad_url, ad_price, ad_img = get_latest_ad()
seen_url = load_seen_url() # So it doesn't detect the most recent ad when it starts, but the one after that

while True:
    ad_name, ad_url, ad_price, ad_img = get_latest_ad()
    seen_url = load_seen_url()

    if ad_url != seen_url:
        print("\n\nNy annons!")
        print(f"Namn: {ad_name}")
        print(f"Pris: {ad_price}")
        print(f"Url: {ad_url}"),
        print(f"Image: {ad_img}")
        save_seen_url(ad_url)

    time.sleep(10)