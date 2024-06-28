import json
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, \
    set_job_type, sleeper, previous_company_wise_titles
from utils.helpers import saveLogs, log_scraper_running_time, take_screenshot

estimated_pay_popup_closed = False


def get_next_link(driver):
    next_link = None
    try:
        anchor_elm = driver.find_element(
            By.CSS_SELECTOR, "div.pagination_container_two_pane a[title='Next Page']")
        if anchor_elm is not None:
            next_link = anchor_elm.get_attribute('href')
    except Exception as e:
        saveLogs(e)
    return next_link


def skip_email_popup(driver):
    try:
        popup_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[data-focus-lock-disabled="false"]')
            )
        )
        if popup_container is not None:
            driver.execute_script(
                "arguments[0].parentNode.removeChild(arguments[0]);", popup_container)
    except Exception as e:
        saveLogs(e)


def skip_estimated_pay_popup(driver):
    global estimated_pay_popup_closed
    try:
        popup = driver.find_element(
            By.CSS_SELECTOR, 'div[aria-label="Estimated Pay"]')
        if popup is not None:
            driver.execute_script(
                "arguments[0].parentNode.removeChild(arguments[0]);", popup)
            estimated_pay_popup_closed = True
    except Exception:
        return


def get_job_posted_date(text):
    match = re.search(r'Posted (.+)', text)
    return match.group(1) if match else "N/A"


def get_from_script(driver):
    data_hash = {}
    try:
        script_element = driver.find_element(By.ID, 'js_variables')
        raw_data = script_element.get_attribute('innerHTML')
        if raw_data:
            json_data = json.loads(raw_data)
            for j in json_data["jobList"]:
                hash_key = f"{j['Title']}-{j['OrgName']}".lower()
                data_hash[hash_key] = {
                    "address": j["City"],
                    "job_source_url": j["QuickApplyHref"],
                    "estimated_salary": j["FormattedSalary"],
                }
    except Exception as e:
        saveLogs(e)
    return data_hash


def extract_salary(salary_str):
    salary_min = salary_max = "N/A"
    salary_format = "N/A"
    patterns = [
        (r'\$(\d+(?:,\d+)?(?:\.\d+)?) (Hourly|Annually|Monthly)',
         lambda m: (m.group(1), m.group(1), m.group(2).lower())),
        (r'\$(\d+(?:,\d+)?(?:\.\d+)?) to \$(\d+(?:,\d+)?(?:\.\d+)?) (Hourly|Annually|Monthly)',
         lambda m: (m.group(1), m.group(2), m.group(3).lower())),
        (r'\$(\d+(?:,\d+)?(?:[Kk])) to \$(\d+(?:,\d+)?(?:[Kk])) (Hourly|Annually|Monthly)',
         lambda m: (m.group(1).upper(), m.group(2).upper(), m.group(3).lower())),
    ]
    for pattern, handler in patterns:
        match = re.match(pattern, salary_str.strip())
        if match:
            salary_min, salary_max, salary_format = handler(match)
            break
    if salary_min != "N/A":
        salary_min = "$" + k_conversion(salary_min)
    if salary_max != "N/A":
        salary_max = "$" + k_conversion(salary_max)
    return salary_min, salary_max, salary_format


def export_jobs(scraped_data):
    df = pd.DataFrame(data=scraped_data, columns=COLUMN_NAME)
    filename = generate_scraper_filename(ScraperNaming.ZIP_RECRUITER)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), job_source='Zip Recruiter', filename=filename
    )


def parse_jobs(driver, groups, existed, dhash, job_type):
    global estimated_pay_popup_closed
    scraped_jobs = []
    for job in groups:
        title_elm = job.find_element(By.TAG_NAME, "h2")
        title = "" if title_elm is None else title_elm.get_attribute(
            'aria-label')
        company_elm = job.find_element(
            By.CSS_SELECTOR, "a[data-testid='job-card-company']"
        )
        company = "" if company_elm is None else company_elm.text
        key = f"{title}-{company}".lower()
        if existed.get(key):
            continue
        description = description_tags = posted_date = "N/A"
        try:
            if not estimated_pay_popup_closed:
                skip_estimated_pay_popup(driver)
            driver.execute_script("arguments[0].scrollIntoView(true);", job)
            sleeper(1)
            title_elm.click()
            sleeper()
            wrapper = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[data-testid='right-pane'] div.flex.flex-col"))
            )
            if wrapper and len(wrapper) > 4 and wrapper[4] and wrapper[3]:
                description_tags = wrapper[4].get_attribute('innerHTML')
                description = wrapper[4].text
                posted_date = get_job_posted_date(wrapper[3].text)
        except Exception as e:
            saveLogs(e)
        salary_min, salary_max, salary_format = extract_salary(
            dhash[key]["estimated_salary"]
        )
        scraped_jobs.append({
            "job_title": title,
            "company_name": company,
            "address": dhash[key]["address"],
            "job_source_url": dhash[key]["job_source_url"],
            "job_description": description,
            "job_description_tags": description_tags,
            "job_posted_date": posted_date,
            "estimated_salary": dhash[key]["estimated_salary"],
            "job_source": "ziprecruiter",
            "job_type": set_job_type(job_type),
            "salary_format": salary_format,
            "salary_min": salary_min,
            "salary_max": salary_max,
        })
    return scraped_jobs


def find_jobs(driver, link,  job_type):
    driver.get(link)
    skip_email_popup(driver)
    data_hash = get_from_script(driver)
    if data_hash:
        existed_titles = previous_company_wise_titles(list(data_hash.keys()))
        job_groups = driver.find_elements(By.CSS_SELECTOR, 'article.group')
        scraped_jobs = parse_jobs(
            driver, job_groups, existed_titles, data_hash, job_type
        )
        if scraped_jobs: export_jobs(scraped_jobs)
        next_page_url = get_next_link(driver)
        if next_page_url:
            find_jobs(driver, next_page_url, job_type)
        else:
            return

@log_scraper_running_time("Ziprecruiter")
def ziprecruiter_scraping(link, job_type):
    driver = configure_webdriver(block_media=True, block_elements=['img'])
    try:
        driver.maximize_window()
        find_jobs(driver, link, job_type)
    except Exception as e:
        saveLogs(e)
    finally:
        take_screenshot(driver, 'ziprecruiter')
        driver.quit()
