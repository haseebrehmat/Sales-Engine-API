import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type, sleeper, previous_jobs
from utils.helpers import saveLogs, log_scraper_running_time

def save_data(scrapped_data, job_title, company_name, address, job_description, job_source_url, salary_format, estimated_salary, salary_min, salary_max, job_type, job_description_tags, loc_type):
    try:
        data = []
        append_data(data, job_title)
        append_data(data, company_name)
        append_data(data, address)
        append_data(data, job_description)
        append_data(data, job_source_url)
        append_data(data, "N/A")
        append_data(data, salary_format)
        append_data(data, k_conversion(estimated_salary))
        append_data(data, k_conversion(salary_min))
        append_data(data, k_conversion(salary_max))
        append_data(data, "YCombinator")
        append_data(data, set_job_type(job_type, loc_type))
        append_data(data, job_description_tags)
        scrapped_data.append(data)
    except Exception as e:
        saveLogs(e)

def finding_job(driver, company_name, scrapped_data):
    try:
        loc_type = ''
        flag = True
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "bg-beige-lighter"))
        )
        job_title = driver.find_element(By.CLASS_NAME, "company-name").text
        details = driver.find_elements(By.CLASS_NAME, "company-details")
        details_loc = details[1].find_elements(By.TAG_NAME, "div")
        address = details_loc[0].text
        if 'remote' in details[1].text.lower():
            loc_type = 'remote'
        elif 'hybrid' in details[1].text.lower():
            loc_type = 'hybrid'
        else:
            loc_type = 'onsite'
        job_type_check = details_loc[2].text
        if 'full-time' in job_type_check.lower():
            job_type = 'full time'
        elif 'contract' in job_type_check.lower():
            job_type = 'contract'
        else:
            flag = False
        description = driver.find_element(By.CLASS_NAME, "bg-beige-lighter")
        job_description = description.find_elements(By.TAG_NAME, "div")

        desc = ""
        desc_tags = ""
        for i in range(1, len(job_description)):
            desc += job_description[i].text
            desc_tags += job_description[i].get_attribute('innerHTML')

        job_source_url = driver.current_url
        salary = driver.find_element(By.CLASS_NAME, "company-title")
        slr = salary.find_elements(By.TAG_NAME, "div")
        if len(slr) > 0 and slr[0].text != '':
            estimated_salary = slr[0].find_element(By.TAG_NAME, "span").text
            if '-' in estimated_salary:
                salary_min = estimated_salary.split(' - ')[0]
                salary_max = estimated_salary.split(' - ')[1]
                salary_format = 'N/A'
            else:
                salary_min = estimated_salary.split('K')[0]
                salary_max = estimated_salary.split('K')[0]
                salary_format = 'N/A'
        else:
            salary_format = 'N/A'
            estimated_salary = 'N/A'
            salary_min = 'N/A'
            salary_max = 'N/A'
        if flag:
            save_data(scrapped_data, job_title, company_name, address, desc, job_source_url, salary_format, estimated_salary, salary_min, salary_max, job_type, desc_tags, loc_type)
    except Exception as e:
        saveLogs(e)

def company_jobs(driver, scrapped_data, existing_jobs):
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "job-name"))
        )
        job_name = driver.find_elements(By.CLASS_NAME, "job-name")
        for job in job_name:
            try:
                link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
                if existing_jobs.get(link):
                    continue
                company_name = driver.find_element(By.CLASS_NAME, "company-name").text
                original_window = driver.current_window_handle
                driver.switch_to.new_window('tab')
                driver.get(link)
                finding_job(driver, company_name, scrapped_data)
                driver.close()
                driver.switch_to.window(original_window)
            except Exception as e:
                saveLogs(e)
    except Exception as e:
        saveLogs(e)

def loading(driver):
    while True:
        try:
            sleeper()
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "loading"))
            )
            load = driver.find_elements(By.CLASS_NAME, "loading")
            if len(load) > 0:
                load[0].location_once_scrolled_into_view
            else:
                break
        except Exception as e:
            break

def login(driver):
    try:
        # WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located(
        #         (By.CLASS_NAME, "MuiTypography-root"))
        # )
        sleeper()
        driver.find_element(By.CLASS_NAME, "MuiTypography-root").click()
        sleeper()
        # WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located(
        #         (By.CLASS_NAME, "input-group"))
        # )
        driver.find_elements(By.CLASS_NAME, "input-group")[3].click()
        sleeper()
        email = driver.find_elements(By.CLASS_NAME, "MuiInput-input")[3]
        email.clear()
        email.send_keys(Y_EMAIL)
        sleeper()

        driver.find_elements(By.CLASS_NAME, "input-group")[4].click()
        sleeper()
        password = driver.find_elements(By.CLASS_NAME, "MuiInput-input")[4]
        password.clear()
        password.send_keys(Y_PASSWORD)
        sleeper()

        driver.find_element(By.CLASS_NAME, "sign-in-button").click()
        sleeper()

        return True
    except Exception as e:
        return False


# calls url
def request_url(driver, url):
    driver.get(url)


# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# find's job name
def find_jobs(driver):
    try:
        companies = driver.find_elements(By.CLASS_NAME, "text-2xl")
        existing_jobs = previous_jobs(source='ycombinator')
        scrapped_data = []
        for i in range(1, len(companies)):
            try:
                link = companies[i].find_elements(By.TAG_NAME, "a")[0].get_attribute('href')
                original_window = driver.current_window_handle
                driver.switch_to.new_window('tab')
                driver.get(link)
                company_jobs(driver, scrapped_data, existing_jobs)
                driver.close()
                driver.switch_to.window(original_window)
            except Exception as e:
                saveLogs(e)
        if len(scrapped_data) > 0:
            df = pd.DataFrame(data=scrapped_data, columns=COLUMN_NAME)
            filename = generate_scraper_filename(ScraperNaming.YCOMBINATOR)
            df.to_excel(filename, index=False)
            ScraperLogs.objects.create(
                total_jobs=len(df), job_source="YCombinator", filename=filename)

    except Exception as e:
        saveLogs(e)


# code starts from here
@log_scraper_running_time("YCombinator")
def ycombinator(link, job_type):
    driver = configure_webdriver()
    try:
        driver.maximize_window()
        try:
            request_url(driver, YCOMBINATOR_LOGIN_URL)
            if login(driver):
                request_url(driver, link)
                loading(driver)
                find_jobs(driver)
        except Exception as e:
            saveLogs(e)
    except Exception as e:
        saveLogs(e)
    driver.quit()
