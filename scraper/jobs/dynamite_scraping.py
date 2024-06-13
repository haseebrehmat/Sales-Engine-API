import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.models import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type,\
    previous_jobs
from utils.helpers import saveLogs, log_scraper_running_time
from scraper.utils.helpers import configure_webdriver


# Dynamite Constants
PAGES_TO_SCRAP = 6

# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))

def is_new_job(posted_at_str):
    return 'new' in posted_at_str.lower()

def filter_by_links(driver, jobs):
    filtered_jobs = []
    base = "https://dynamitejobs.com" 
    try:
        # Get all links
        url_elms = driver.find_elements(By.CSS_SELECTOR, '.result-item h2')
        urls = [f"{base}{elm.get_attribute('href')}" for elm in url_elms]
        # Get existing jobs
        existing_jobs = previous_jobs(source='dynamite', urls=urls)
        for job in jobs:
            link_elm = job.find_element(By.TAG_NAME, 'h2')
            posted_at = job.find_element(By.CSS_SELECTOR, 'span.leading-6')
            # Continue if job already exists
            if ((link_elm and existing_jobs.get(f"{base}{link_elm.get_attribute('href')}")) 
                or (posted_at and not is_new_job(posted_at.text))
            ): continue
            filtered_jobs.append(job)
    except Exception as e:
        saveLogs(e)
    return filtered_jobs
    
# find's job name
def find_jobs(driver, job_type):
    try:
        scrapped_data = []
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "result-item")))

        raw_jobs = driver.find_elements(By.CLASS_NAME, "result-item")
        jobs = filter_by_links(driver, raw_jobs)

        for job in jobs:
            data = []
            job.click()

            job_details = driver.find_elements(By.CLASS_NAME, "min-h-32")[0].text.split("\n")[:6]

            job_title = job_details[0]
            company_name = job_details[1]
            job_url = driver.find_element(By.CLASS_NAME, 'min-h-32').find_element(By.TAG_NAME, 'a').get_attribute(
                'href')
            if '$' in job_details[3]:
                estimated_salary = job_details[-3]
                if 'month' in estimated_salary.split(' per ')[1]:
                    salary_format = 'monthly'
                elif 'hour' in estimated_salary.split(' per ')[1]:
                    salary_format = 'hourly'
                elif ('year' or 'annum') in estimated_salary.split(' per ')[1]:
                    salary_format = 'yearly'
                address = job_details[4]
                job_posted_date = job_details[-1]
            else:
                address = job_details[3]
                estimated_salary = 'N/A'
                salary_format = 'N/A'
                job_posted_date = job_details[-2]

            job_description = driver.find_elements(By.CLASS_NAME, "p-6")[0]

            if '-' in estimated_salary:
                salary = estimated_salary.split('-')
                min_salary = salary[0].strip()
                max_salary = salary[1].split(' per')[0].strip()
            else:
                min_salary = 'N/A'
                max_salary = 'N/A'

            data.append(job_title)
            data.append(company_name)
            data.append(address)
            data.append(job_description.text)
            data.append(job_url)
            data.append(job_posted_date)
            data.append(salary_format)
            data.append(k_conversion(estimated_salary))
            data.append(k_conversion(min_salary))
            data.append(k_conversion(max_salary))
            data.append("Dynamite")
            data.append(set_job_type(job_type))
            data.append(job_description.get_attribute('innerHTML'))
            scrapped_data.append(data)

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date",
                        "salary_format", "estimated_salary", "salary_min", "salary_max", "job_source", "job_type",
                        "job_description_tags"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        filename = generate_scraper_filename(ScraperNaming.DYNAMITE)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(total_jobs=len(df), job_source="Dynamite", filename=filename)
    except Exception as e:
        saveLogs(e)


@log_scraper_running_time("Dynamite")
def dynamite(link, job_type):
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        page = 1
        try:
            while page <= PAGES_TO_SCRAP:
                request_url(driver, f'{link}&page={page}')
                find_jobs(driver, job_type)
                page += 1
        except Exception as e:
            saveLogs(e)
    except Exception as e:
        saveLogs(e)
    finally:
        driver.quit()

