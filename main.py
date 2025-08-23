from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin

# Merojob job listing url
merojob_url = "https://merojob.com/services/top-job/"
merojob_response = requests.get(merojob_url)

merojob_html = merojob_response.text
merojob_soup = BeautifulSoup(merojob_html, 'html.parser')

job_postings = merojob_soup.select('div[itemtype="http://schema.org/JobPosting"]')
all_jobs = []
merojob_listing_dict = {}
for job in job_postings:
    # Get link to job description
    job_description_link = job.select('h1 a')[0]['href']
    job_description_link = urljoin(merojob_url,job_description_link)

    # Get link to employer profile  
    employer_profile_link = job.select('h3 a')[0]['href']
    employer_profile_link = urljoin(merojob_url,employer_profile_link)

    job_links = {   "job_description_link": job_description_link,
                    "employer_profile_link": employer_profile_link
                    }
    all_jobs.append(job_links)

print(all_jobs)