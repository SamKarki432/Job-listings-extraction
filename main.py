from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin

# Merojob job listing url
merojob_url = "https://merojob.com/services/top-job/"

all_jobs = []
while(merojob_url):
    merojob_response = requests.get(merojob_url)

    merojob_html = merojob_response.text
    merojob_soup = BeautifulSoup(merojob_html, 'html.parser')

    job_postings = merojob_soup.select('div[itemtype="http://schema.org/JobPosting"]')

    merojob_listing_dict = {}

    for job in job_postings:
        # Get link to job description
        job_description_link = job.select('h1 a')[0]['href']
        #print(job_description_link)
        job_description_link = urljoin(merojob_url,job_description_link)

        # Get link to employer profile 
        # If employer profile link not available, then show "Not available"
        employer_profile_link = job.select('h3 a')
        if employer_profile_link:
            employer_profile_link = employer_profile_link[0]['href']
            #print(employer_profile_link)
            employer_profile_link = urljoin(merojob_url,employer_profile_link)
        else:
            employer_profile_link ="Not available"

        job_links = {   "job_description_link": job_description_link,
                        "employer_profile_link": employer_profile_link
                        }
        all_jobs.append(job_links)

    # Get link for next page
    jobs_pages =  merojob_soup.select('nav[aria-label="Page navigation example"] a[class="pagination-next page-link"]')
    # Check if next page exists, if not exists set merojob_url as 0
    if(jobs_pages):
        jobs_pages = jobs_pages[0]['href']
        merojob_url = urljoin(merojob_url,jobs_pages)
        print(urljoin(merojob_url,jobs_pages))
    else: 
        merojob_url = 0

print(all_jobs)