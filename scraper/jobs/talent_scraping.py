import pandas as pd
from selenium.webdriver.common.by import By

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type, \
    previous_jobs, sleeper
from utils.helpers import saveLogs, log_scraper_running_time



# Talent Constants
BASE_URL = "https://www.talent.com"

# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def filter_links(jobs):
    existing_jobs = {}
    try:
        urls = [f"{BASE_URL}{elm.get_attribute('data-link')}" for elm in jobs]
        existing_jobs = previous_jobs(source='talent', urls=urls)
    except Exception as e:
        saveLogs(e)
    return existing_jobs

# find's job name
def find_jobs(driver, job_type):
    scrapped_data = []
    sleeper()
    jobs = driver.find_elements(By.CLASS_NAME, "link-job-wrap")
    existing_jobs = filter_links(jobs)
    for job in jobs:
        try:
            job_url = f"{BASE_URL}{job.get_attribute('data-link')}"
            if existing_jobs.get(job_url):
                continue
            data = []
            sleeper()
            job.click()
            sleeper()

            job_title = driver.find_element(
                By.CLASS_NAME, "jobPreview__header--title")
            append_data(data, job_title.text)
            company_name = driver.find_element(
                By.CLASS_NAME, "jobPreview__header--company")
            append_data(data, company_name.text)
            address = driver.find_element(
                By.CLASS_NAME, "jobPreview__header--location")
            append_data(data, address.text)
            job_description = driver.find_element(
                By.CLASS_NAME, "jobPreview__body--description")
            append_data(data, job_description.text)
            append_data(data, job_url)
            posted_at = job.find_element(
                By.CLASS_NAME, "c-card__jobDatePosted")            
            append_data(data, posted_at.text if posted_at else 'Posted Today')
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "N/A")
            append_data(data, "Talent")
            if 'remote' in job_type.lower():
                append_data(data, set_job_type(job_type))
            elif 'hybrid' in job_type.lower():
                append_data(data, set_job_type(job_type, 'hybrid'))
            else:
                append_data(data, set_job_type(job_type, 'onsite'))
            append_data(data, job_description.get_attribute('innerHTML'))

            scrapped_data.append(data)
        except Exception as e:
            saveLogs(e)
    df = pd.DataFrame(data=scrapped_data, columns=COLUMN_NAME)
    filename = generate_scraper_filename(ScraperNaming.TALENT)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Talent", filename=filename)
    pagination = driver.find_elements(
        By.CLASS_NAME, "pagination")

    if len(pagination) == 0:
        return False
    else:
        next_page = pagination[0].find_elements(
            By.TAG_NAME, "a")
        try:
            next_page[-1].click()
            return True
        except Exception as e:
            saveLogs(e)
            return False


# code starts from here
@log_scraper_running_time("Talent")
def talent(link, job_type):
    driver = configure_webdriver(block_media=True, block_elements=['img'])
    try:
        driver.maximize_window()
        try:
            flag = True
            request_url(driver, link)
            driver.maximize_window()
            while flag:
                flag = find_jobs(driver, job_type)
        except Exception as e:
            saveLogs(e)

    except Exception as e:
        saveLogs(e)
    driver.quit()
