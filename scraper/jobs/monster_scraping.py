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
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type
from utils.helpers import saveLogs
total_job = 0

def append_data(data, field):
    data.append(str(field).strip("+"))

def load_jobs(driver):
    time.sleep(5)
    loading = "job-search-load-more"
    try:
        for load in driver.find_elements(By.CLASS_NAME, "sc-kdBSHD"):
            if loading in load.get_attribute("id"):
                return True
        return False

    except Exception as e:
        return False

# find's job name
def find_jobs(driver, job_type, total_job):
    scrapped_data = []
    count = 0
    time.sleep(7)
    while load_jobs(driver):
        try:
            jobs = driver.find_elements(
                By.CLASS_NAME, "job-search-resultsstyle__JobCardWrap-sc-1wpt60k-4")
            for job in jobs:
                job.location_once_scrolled_into_view
        except Exception as e:
            print(e)
    jobs = driver.find_elements(
        By.CLASS_NAME, "job-search-resultsstyle__JobCardWrap-sc-1wpt60k-4")
    for job in jobs:
        try:
            
            data = []
            job.click()
            try: 
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "jobview-containerstyles__JobViewWrapper-sc-n3vjwx-0 fJluds"))
                )
            except:
                print("")
            job_title = driver.find_element(By.CLASS_NAME, "headerstyle__JobViewHeaderJobName-sc-onfits-9")
            append_data(data, job_title.text)
            company_name = driver.find_element(By.CLASS_NAME, "headerstyle__JobViewHeaderCompanyName-sc-onfits-12")
            append_data(data, company_name.text)
            address = driver.find_element(By.CLASS_NAME, "headerstyle__JobViewHeaderDetails-sc-onfits-10").find_elements(By.TAG_NAME, "li")[1]
            append_data(data, address.text)
            job_description = driver.find_element(By.CLASS_NAME, "descriptionstyles__DescriptionContainerOuter-sc-7dvtrp-0")
            append_data(data, job_description.text)
            url = driver.find_elements(
                By.CLASS_NAME, "sc-gAjuZT")
            append_data(data, url[count].get_attribute('href'))
            count += 1
            job_posted_date = driver.find_element(By.CLASS_NAME, "headerstyle__JobViewHeaderDetails-sc-onfits-10").find_elements(By.TAG_NAME, "li")[2]
            append_data(data, job_posted_date.text)
            try:
                salary_string = driver.find_element(
                    By.CLASS_NAME, "detailsstyles__DetailsTableDetailBody-sc-1deoovj-5")
                if "$" in salary_string.text:
                    salary_format = "N/A"
                    estimated_salary = salary_string.text.split(" ")[0]
                    salary_min = salary_string.text.split("-")[0]
                    salary_max = salary_string.text.split("-")[1].split(" ")[0]
                    append_data(data, salary_format)
                    append_data(data, k_conversion(estimated_salary))
                    append_data(data, k_conversion(salary_min))
                    append_data(data, k_conversion(salary_max))
                else:
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")
                    append_data(data, "N/A")
            except:
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
            append_data(data, "Monster")
            append_data(data, set_job_type(job_type, determine_job_sub_type(job_type)))
            append_data(data, job_description.get_attribute('innerHTML'))
            scrapped_data.append(data)
            total_job += 1
        except Exception as e:
            print("Exception in Monster => ", e)
    columns_name = ["job_title", "company_name", "address", "job_description",
                    'job_source_url', "job_posted_date", "salary_format", "estimated_salary", "salary_min",
                    "salary_max", "job_source", "job_type", "job_description_tags"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    filename = generate_scraper_filename(ScraperNaming.MONSTER)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Monster", filename=filename)
    return total_job
# code starts from here

def determine_job_sub_type(type):
    sub_type = 'remote'
    if 'onsite' in type.lower() or 'on site' in type.lower():
        sub_type = 'onsite'
    if 'hybrid' in type.lower():
        sub_type = 'hybrid'
    return sub_type
    

def monster(link, job_type):
    total_job = 0
    print("Monster")
    driver = configure_webdriver()
    try:
        try:
            driver.maximize_window()
            driver.get(link)
            total_job = find_jobs(
                driver, job_type, total_job)
            print("SCRAPING_ENDED")
        except Exception as e:
            saveLogs(e)
            print(LINK_ISSUE)
    except Exception as e:
        saveLogs(e)
        print(e)
    driver.quit()
