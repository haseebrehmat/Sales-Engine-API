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
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming
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
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "descriptionstyles__DescriptionContainer-sc-13ve12b-0"))
            )
            job_title = driver.find_element(
                By.CLASS_NAME, "headerstyle__JobViewHeaderTitle-sc-1ijq9nh-5")
            append_data(data, job_title.text)
            company_name = driver.find_element(
                By.CLASS_NAME, "headerstyle__JobViewHeaderCompany-sc-1ijq9nh-6")
            append_data(data, company_name.text)
            address = driver.find_element(
                By.CLASS_NAME, "headerstyle__JobViewHeaderLocation-sc-1ijq9nh-4")
            append_data(data, address.text)
            job_description = driver.find_element(
                By.CLASS_NAME, "descriptionstyles__DescriptionBody-sc-13ve12b-4")
            append_data(data, job_description.text)
            url = driver.find_elements(
                By.CLASS_NAME, "sc-gAjuZT")
            append_data(data, url[count].get_attribute('href'))
            job_posted_date = driver.find_element(
                By.CLASS_NAME, "detailsstyles__DetailsTableDetailPostedBody-sc-1deoovj-6")
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
                    append_data(data, estimated_salary)
                    append_data(data, salary_min)
                    append_data(data, salary_max)
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
            append_data(data, job_type)
            append_data(data, job_description.get_attribute('innerHTML'))
            scrapped_data.append(data)
            count += 1
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

def monster(link, job_type):
    total_job = 0
    print("Monster")
    try:
        options = webdriver.ChromeOptions()  # newly added
        options.add_argument("--headless")
        options.add_argument("window-size=1200,1100")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
        )
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:  # modified
            try:
                driver.maximize_window()
                driver.get(link)
                total_job = find_jobs(
                    driver, job_type, total_job)
                print("SCRAPING_ENDED")
            except Exception as e:
                saveLogs(e)
                print(LINK_ISSUE)
            driver.quit()
    except Exception as e:
        saveLogs(e)
        print(e)
