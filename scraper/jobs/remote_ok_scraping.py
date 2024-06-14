from datetime import timedelta, datetime
from logging import exception
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, remove_emojis, k_conversion, configure_webdriver, set_job_type, previous_jobs, sleeper
from utils.helpers import saveLogs, log_scraper_running_time


def load_jobs(driver):
    previous_jobs = driver.find_elements(By.CLASS_NAME, "job")
    previous_len = len(previous_jobs)

    while True:
        if not check_if_job_day_ago(previous_jobs[previous_len-1]):
            break
        sleeper()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleeper()
        previous_jobs = driver.find_elements(By.CLASS_NAME, "job")
        if previous_len == len(previous_jobs):
            break
        previous_len = len(previous_jobs)


def get_job_urls(driver):
    load_jobs(driver)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "tr[data-slug][data-id]"))
        )
    except Exception as error:
        saveLogs(e)
    job_urls = driver.find_elements(By.CSS_SELECTOR, "tr[data-slug][data-id]")
    links = []
    for job_url in job_urls:
        try:
            link = job_url.get_attribute("data-href")
            links.append("https://remoteok.com"+link)
        except Exception as e:
            saveLogs(e)
    return links

def check_if_job_day_ago(job):
    day_ago = False
    try:
        date_elm = job.find_element(By.TAG_NAME, "time")
        date_str = date_elm.get_attribute("datetime")
        date_obj = datetime.fromisoformat(date_str)
        current_date = datetime.now(tz=date_obj.tzinfo)
        one_day_ago_date = current_date - timedelta(days=1)
        if date_obj >= one_day_ago_date: 
            day_ago = True
    except Exception as e:
        saveLogs(e)
    return day_ago

# calls url


def is_convertible_to_number(s):
    if isinstance(s, str):
        try:
            int(s)
            return True
        except ValueError:
            return False
    return False


def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def find_jobs(driver, job_type):
    scrapped_data = []
    links = get_job_urls(driver)
    existing_jobs = previous_jobs(source='remoteok',urls=links)
    original_window = driver.current_window_handle
    try:
        for link in links:
            data = []
            if existing_jobs.get(link):
                continue
            try:
                driver.switch_to.new_window('tab')
                driver.get(link)
                sleeper()
                id = link.split("-")[-1]
                if is_convertible_to_number(id):
                    id = int(id)
                    job = WebDriverWait(driver, 40).until(
                        EC.presence_of_element_located(
                        (By.CLASS_NAME, f"job-{id}")))
                    job_desc = WebDriverWait(driver, 40).until(
                        EC.presence_of_element_located(
                        (By.CLASS_NAME, "expandContents")))

                    temp = job.find_element(
                        By.CLASS_NAME, "company_and_position").text
                    temp = temp.splitlines()
                    job_title = remove_emojis(temp[0])
                    append_data(data, job_title)
                    company_name = remove_emojis(temp[1])
                    append_data(data, company_name)
                    address = remove_emojis(temp[2])
                    append_data(data, address)
                    job_source_url = link
                    append_data(data, job_source_url)
                    job_description = job_desc.text
                    append_data(data, job_description)
                    temp1 = job.find_element(By.CLASS_NAME, "time").text
                    job_posted_date = temp1
                    append_data(data, job_posted_date)
                    salary_format = "yearly"
                    append_data(data, salary_format)
                    temp2 = temp[-1].split(" ")
                    if len(temp2[-3]) >= 4 and temp2[-3][0] == "$":
                        salary_min = remove_emojis(temp2[-3])
                    else:
                        salary_min = "N/A"
                    append_data(data, salary_min)
                    if len(temp2[-1]) >= 4 and temp2[-1][0] == "$":
                        salary_max = remove_emojis(temp2[-1])
                    else:
                        salary_max = "N/A"
                    append_data(data, salary_max)
                    if salary_max == "N/A" or salary_min == "N/A":
                        estimated_salary = "N/A"
                    else:
                        estimated_salary = f"{salary_min}-{salary_max}"
                    append_data(data, estimated_salary)
                    job_source = ScraperNaming.REMOTE_OK
                    append_data(data, job_source)
                    append_data(data, job_type)
                    job_description_tags = job_desc.get_attribute("innerHTML")
                    append_data(data, str(job_description_tags))
            except exception as e:
                    saveLogs(e)
                
            driver.close()
            driver.switch_to.window(original_window)
            if data == []:
                continue
            scrapped_data.append(data)
    except Exception as e:
        saveLogs(e)
    if len(scrapped_data) > 0:
        export_to_excel(scrapped_data)

def export_to_excel(scrapped_data):
    df = pd.DataFrame(data=scrapped_data, columns=COLUMN_NAME)
    filename = generate_scraper_filename(ScraperNaming.REMOTE_OK)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Remote ok", filename=filename
    )


# code starts from here
@log_scraper_running_time("RemoteOk")
def remoteok(link, job_type):
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        sleeper()
        request_url(driver, link)
        sleeper()
        find_jobs(driver, job_type)
    except Exception as e:
        saveLogs(e)
    finally:
        driver.quit()
