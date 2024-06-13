import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, previous_jobs, set_job_type
from utils.helpers import log_scraper_running_time, saveLogs

# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver, job_type, job_urls):
    try:
        scrapped_data = []

        existing_jobs_dictionary = previous_jobs("dice", job_urls)

        original_window = driver.current_window_handle
        driver.switch_to.new_window('tab')
        for url in job_urls:
            try:
                if not existing_jobs_dictionary.get(url):
                    data = []
                    driver.get(url)
                    job_title = driver.find_element(By.TAG_NAME, "h1")
                    append_data(data, job_title.text)
                    company_name = driver.find_element(By.CLASS_NAME, "companyInfo")
                    append_data(data, company_name.text)
                    address = driver.find_elements(By.CLASS_NAME, "job-header_jobDetail__ZGjiQ")
                    job_location = REMOTE
                    if 'Posted' in address[0].text:
                        job_posted_date = address[0].text.split(' |')[0]
                    else:
                        try:
                            job_location = address[0].text
                            job_posted_date = address[1].text.split(' |')[0]
                        except:
                            continue
                    append_data(data, job_location)

                    time.sleep(2)
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "job-description")))
                    try:
                        driver.find_element(By.ID, "descriptionToggle").click()
                    except:
                        driver.close()
                        continue
                    job_description = driver.find_element(By.CLASS_NAME, "job-description")
                    append_data(data, job_description.text)
                    append_data(data, url)
                    append_data(data, job_posted_date)
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "Dice")
                    append_data(data, set_job_type(job_type, determine_job_sub_type(job_type)))
                    append_data(data, job_description.get_attribute('innerHTML'))

                    scrapped_data.append(data)
                    time.sleep(0.5)
            except:
                pass

        driver.close()
        driver.switch_to.window(original_window)

        df = pd.DataFrame(data=scrapped_data, columns=COLUMN_NAME)
        filename = generate_scraper_filename(ScraperNaming.DICE)
        df.to_excel(filename, index=False)

        ScraperLogs.objects.create(total_jobs=len(df), job_source="Dice", filename=filename)
    except:
        pass
    
def determine_job_sub_type(type):
    sub_type = 'remote'
    if 'onsite' in type.strip().lower() or 'on site' in type.strip().lower():
        sub_type = 'onsite'
    if 'hybrid' in type.strip().lower():
        sub_type = 'hybrid'
    return sub_type

def load_jobs(driver, job_urls):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-title-link"))
        )

        jobs = driver.find_elements(By.TAG_NAME, "dhi-search-card")
        job_urls += [f"https://www.dice.com/job-detail/{job.find_element(By.CLASS_NAME, 'card-title-link').get_attribute('id')}" for job in jobs if job.find_element(By.CLASS_NAME, 'card-title-link')]

        pagination = driver.find_elements(By.CLASS_NAME, "pagination-next")
        try:
            next_page = pagination[0].get_attribute('class')
            if 'disabled' in next_page:
                return False, job_urls
            else:
                pagination[0].click()
                time.sleep(3)
            return True, job_urls
        except Exception as e:
            return False, job_urls
    except:
        return False, job_urls


# code starts from here
@log_scraper_running_time("dice")
def dice(link, job_type):
    print("Dice")
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        job_urls = []
        flag = True
        try:
            request_url(driver, link)
            while flag:
                flag, job_urls = load_jobs(driver, job_urls)
            find_jobs(driver, job_type, job_urls)
        except Exception as e:
            saveLogs(e)

    except Exception as e:
        saveLogs(e)
    finally:
        driver.quit()
    