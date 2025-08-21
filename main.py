from bs4 import BeautifulSoup
import requests
import pandas as pd

# Merojob job listing url
merojob_url = "https://merojob.com/services/top-job/"
merojob_response = requests.get(merojob_url)

merojob_html = merojob_response.text
merojob_soup = BeautifulSoup(merojob_html, 'html.parser')