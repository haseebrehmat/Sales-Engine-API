from logging import exception
from datetime import timedelta, datetime
import pandas as pd
from selenium.webdriver.common.by import By
from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, set_job_type, sleeper, previous_jobs
from utils.helpers import saveLogs,log_scraper_running_time


def load_jobs(driver):
    previous_jobs = driver.find_elements(By.CLASS_NAME,"hxecsD")
    previous_len = len(previous_jobs)
    while True:
        if not check_if_job_day_ago(previous_jobs[previous_len-1]):
            break
        sleeper()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        previous_jobs = driver.find_elements(By.CLASS_NAME, "hxecsD")
        if previous_len == len(previous_jobs):
            break
        previous_len = len(previous_jobs)

    return previous_jobs

def check_if_job_day_ago(job):
    day_ago = False
    try:
        date_elm = job.find_element(By.CLASS_NAME, "new-job-item__JobItemDate-sc-1qa4r36-5").text
        date_obj = datetime.strptime(date_elm, "%d %b")
        current_year = datetime.now().year
        date_obj = date_obj.replace(year=current_year)
        current_date = datetime.now()
        one_day_ago_date = current_date - timedelta(days=1)
        if date_obj >= one_day_ago_date:
            day_ago = True
    except Exception as e:
        saveLogs(e)
    return day_ago

def get_job_urls(driver):
    job_urls = load_jobs(driver)
    links = []
    for job_url in job_urls:
        if not check_if_job_day_ago(job_url):
            continue
        link = job_url.find_element(By.TAG_NAME, "a")
        t = job_url.find_element(
            By.CLASS_NAME, "new-job-item__JobItemDate-sc-1qa4r36-5")
        links.append([link.get_attribute("href"), t.text])
    return links


def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


def find_jobs(driver):
    scrapped_data = []
    links = get_job_urls(driver)
    exsiting_links = []
    for link in links:
        exsiting_links.append(link[0])
    existing_jobs = previous_jobs(source=ScraperNaming.JUST_REMOTE, urls=exsiting_links)
    original_window = driver.current_window_handle
    for link in links:
        data = []
        if existing_jobs.get(link[0]):
            continue
        try:
            driver.switch_to.new_window('tab')
            driver.get(link[0])
            sleeper()
            temp = driver.find_element(
                By.CLASS_NAME, "JpOdR")
            job_title = temp.find_element(
                By.CLASS_NAME, "job-title__StyledJobTitle-sc-10irtcq-0")
            job_type_check = driver.find_elements(By.CLASS_NAME, "job-meta__Wrapper-oh0pn7-0")[0].text.lower()
            append_data(data, job_title.text)
            company_name = driver.find_element(
                    By.CLASS_NAME, "ktyJgG")
            append_data(data, company_name.text.splitlines()[0])
            address = 'Remote'
            append_data(data, address)
            job_source_url = link[0]
            append_data(data, job_source_url)
            job_description = temp
            append_data(data, job_description.text)
            job_posted_date = link[1]
            append_data(data, job_posted_date)
            salary_format = "N/A"
            append_data(data, salary_format)
            salary_min = "N/A"
            append_data(data, salary_min)
            salary_max = "N/A"
            append_data(data, salary_max)
            estimated_salary = 'N/A'
            append_data(data, estimated_salary)
            job_source = ScraperNaming.JUST_REMOTE
            append_data(data, job_source)
            if 'contract' in job_type_check:
                append_data(data, set_job_type('contract'))
            elif 'permanent' in job_type_check:
                append_data(data, set_job_type('full time'))
            else:
                continue

            job_description_tags = temp.get_attribute("innerHTML")
            append_data(data, str(job_description_tags))
        except exception as e:
                saveLogs(e)
        driver.close()
        driver.switch_to.window(original_window)
        scrapped_data.append(data)
    if len(scrapped_data) > 0:
        export_to_excel(scrapped_data)
    
def export_to_excel(scrapped_data):
    df = pd.DataFrame(data=scrapped_data, columns=COLUMN_NAME)
    filename = generate_scraper_filename(ScraperNaming.JUST_REMOTE)
    df.to_excel(filename, index=False)

    ScraperLogs.objects.create(
        total_jobs=len(df), job_source="Just Remote", filename=filename
    )


# code starts from here 
@log_scraper_running_time("JustRemote")
def just_remote(link, job_type):
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        request_url(driver, link)
        find_jobs(driver)
    except Exception as e:
        saveLogs(e)
    driver.quit()
