from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin
import re

# Merojob jobs url
merojob_url = "https://merojob.com/services/top-job/"
all_jobs = []
skipped_jobs = []

# Funtion to extract information from individual job page
def scrape_job_details(all_jobs_links):
    
    for job_link in all_jobs_links:

        job_description_page_link = job_link["job_description_link"]
        # Get job description page
        job_page = requests.get(job_description_page_link)
        job_page_html = job_page.text
        job_page_parsed = BeautifulSoup(job_page_html,'html.parser')

        job_title = job_page_parsed.select('h1[itemprop="title"]')[0]
        
        try:
            job_details = job_page_parsed.select('div[class="card-body"]')[2]
            job_info =  job_details.select('table')[0]
            job_specs =  job_details.select('table')[1]    

            job_specs_dict = {"Job Title": job_title.get_text(strip=True),
                            "Employer Profile": job_link["employer_profile_link"]
                            }
        except IndexError:
            print("Skipping job: structure missing")
            # Store Skipped job links in a seperate list
            skipped_jobs.append(job_link)
            continue

        job_info = job_info.select('tr')
        job_specs = job_specs.select('tr')

        for row_data in job_info:
            row_data = row_data.text.strip()
            matches = re.findall(r"([^\n:]+)\s*:\s*([\s\S]*?)(?=\n[^\n:]+\s*:|$)",row_data)

            for k,v in matches:
                job_specs_dict[k.strip()] = v.strip().replace("/n","")


        for row_data in job_specs:
            row_data = row_data.text.strip()
            matches = re.findall(r"([^\n:]+)\s*:\s*([\s\S]*?)(?=\n[^\n:]+\s*:|$)",row_data)

            for k,v in matches:
                job_specs_dict[k.strip()] = v.strip().replace("/n","")

        all_jobs.append(job_specs_dict)
    
all_jobs_links = []

while(merojob_url):
    merojob_response = requests.get(merojob_url)

    merojob_html = merojob_response.text
    merojob_parsed = BeautifulSoup(merojob_html, 'html.parser')

    job_postings = merojob_parsed.select('div[itemtype="http://schema.org/JobPosting"]')

    merojob_listing_dict = {}

    for job in job_postings:
        # Get link to job description
        job_description_page_link = job.select('h1 a')[0]['href']
        #print(job_description_link)
        job_description_page_link = urljoin(merojob_url,job_description_page_link)

        # Get link to employer profile 
        # If employer profile link not available, then show "Not available"
        employer_profile_link = job.select('h3 a')
        if employer_profile_link:
            employer_profile_link = employer_profile_link[0]['href']
            #print(employer_profile_link)
            employer_profile_link = urljoin(merojob_url,employer_profile_link)
        else:
            employer_profile_link ="Not available"

        job_info_links = {  "job_description_link": job_description_page_link,
                            "employer_profile_link": employer_profile_link
                        }

        all_jobs_links.append(job_info_links)

    # Get link for next page
    jobs_pages =  merojob_parsed.select('nav[aria-label="Page navigation example"] a[class="pagination-next page-link"]')
    # Check if next page exists, if not exists set merojob_url as 0, i.e null
    if(jobs_pages):
        jobs_pages = jobs_pages[0]['href']
        merojob_url = urljoin(merojob_url,jobs_pages)
    else: 
        merojob_url = 0


scrape_job_details(all_jobs_links)

all_jobs_df = pd.DataFrame(all_jobs)

#

#all_jobs_df.to_excel("merojob_job_list_v1.xlsx")