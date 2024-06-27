from selenium.webdriver.common.by import By
from scraper.utils.helpers import ScraperNaming, k_conversion, configure_webdriver, \
    set_job_type, sleeper, previous_jobs, export_to_excel
from utils.helpers import log_scraper_running_time, saveLogs, is_cloudflare
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def filter_jobs(driver):
    filtered = []
    jobs_exist = True
    while jobs_exist:
        sleeper()
        all_jobs = driver.find_elements(By.CLASS_NAME, "slider_container")
        for job in all_jobs:
            try:
                job_key = job.find_element(
                    By.TAG_NAME, 'a').get_attribute('data-jk')
                posted_date = job.find_element(
                    By.CSS_SELECTOR, '[data-testid="myJobsStateDate"]')
                filtered.append({
                    'link': f"https://www.indeed.com/viewjob?jk={job_key}",
                    'posted_date': posted_date.text.split('\n')[1]
                })
            except:
                continue
        try:
            next_page = driver.find_element(
                By.CSS_SELECTOR, "a[aria-label='Next Page']"
            )
            next_page.click()
            sleeper()
        except:
            jobs_exist = False
            break
    return filtered


def find_jobs(driver, job_type):
    scrapped_data = []
    filtered_jobs = filter_jobs(driver)
    previous_links = previous_jobs('indeed', [row['link'] for row in filtered_jobs])
    for job in filtered_jobs:
        if job['link'] in previous_links:
            continue
        data = {}
        try:
            driver.get(job["link"])
            if is_cloudflare(driver, 'Indeed'): continue
            sleeper()
            main_job_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jobsearch-JobComponent"))
            )
            job_title = main_job_container.find_element(
                By.CLASS_NAME, "jobsearch-JobInfoHeader-title"
            )
            data["job_title"] = job_title.text
            company_name = main_job_container.find_element(
                By.CSS_SELECTOR, '[data-testid="inlineHeader-companyName"]'
            )
            data["company_name"] = company_name.text
            data["address"] = extract_address(main_job_container)
            data["job_type"] = set_job_type(job_type)
            description = main_job_container.find_element(
                By.ID, "jobDescriptionText"
            )
            data["job_description_tags"] = description.get_attribute(
                'innerHTML')
            data["job_description"] = description.text
            # Extracting Salary Details
            data = extract_salary(data, main_job_container)
            data["job_source"] = "Indeed"
            data["job_source_url"] = job["link"]
            data["job_posted_date"] = job["posted_date"]
            scrapped_data.append(data)
        except Exception as e:
            saveLogs(e)
    if scrapped_data:
        export_to_excel(scrapped_data, ScraperNaming.INDEED, 'Indeed')

def extract_salary(data, main_job_container):
    salary = main_job_container.find_element(
        By.XPATH, '//*[@id="salaryInfoAndJobType"]/span[1]'
    )
    if salary and '$' in salary.text:
        if 'hour' in salary.text:
            data["salary_format"] = "hourly"
        elif ('year' or 'annum') in salary.text:
            data["salary_format"] = "yearly"
        elif 'month' in salary.text:
            data["salary_format"] = "monthly"
        else:
            data["salary_format"] = "N/A"
        try:
            delimiter = ' a' if ' a ' in salary.text else ' an'
            data["estimated_salary"] = k_conversion(
                salary.text.split(delimiter)[0])
        except:
            data["estimated_salary"] = "N/A"
        try:
            salary_min = salary.text.split('$')[1]
            data["salary_min"] = k_conversion(
                salary_min.split(' ')[0])
        except:
            data["salary_min"] = "N/A"
        try:
            salary_max = salary.text.split('$')[2]
            data["salary_max"] = k_conversion(
                salary_max.split(' ')[0])
        except:
            data["salary_max"] = "N/A"
    else:
        data["salary_max"] = "N/A"
        data["salary_min"] = "N/A"
        data["salary_format"] = "N/A"
        data["estimated_salary"] = "N/A"
    return data


def extract_address(main_job_container):
    try:
        address = main_job_container.find_element(
            By.CSS_SELECTOR, '[data-testid="inlineHeader-companyLocation"]'
        )
        return address.text
    except:
        "remote"

@log_scraper_running_time("Indeed")
def indeed(link, job_type):
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        try:
            driver.get(link)
            driver.maximize_window()
            if is_cloudflare(driver, 'Indeed'): return
            sleeper()
            find_jobs(driver, job_type)
        except Exception as e:
            saveLogs(e)
    except Exception as e:
        saveLogs(e)
    driver.quit()
