from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scraper.utils.helpers import ScraperNaming, configure_webdriver, set_job_type, \
     previous_jobs, sleeper, export_to_excel, previous_company_wise_titles
from utils.helpers import saveLogs, log_scraper_running_time
import html

# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))


# loading jobs
def loading(driver, count):
    try:
        sleeper()
        load = driver.find_element(
            By.CLASS_NAME, "jobsList__button-container--3FEJ-")
        btn = load.find_element(By.TAG_NAME, "button")
        btn.location_once_scrolled_into_view
        btn.click()
        count += 1
        if count == 30:
            return False, count
        return True, count
    except:
        return False, count


# click accept cookie footer
def accept_cookie(driver):
    try:
        driver.find_element(
            By.CLASS_NAME, "styles__primary-button--tFH2O").click()
    except Exception as e:
        saveLogs(e)


def find_job_data_hash(job):
    dhash = {"link": "", "tc": ""} # tc stands for title and company
    try:
        anchor = job.find_element(By.TAG_NAME, "a")
        title_n_company = anchor.get_attribute("aria-label")
        dhash["link"] = anchor.get_attribute("href")
        dhash["tc"] = str(html.unescape(title_n_company.replace(" at ", "-"))).lower()
    except Exception as e:
        saveLogs(e)
    return dhash


# find's job
def find_jobs(driver, job_type):
    try:
        scrapped_data = []
        sleeper()
        raw_jobs = driver.find_elements(
            By.CLASS_NAME, "jobsList__list-item--3HLIF")
        jobs, tcs, urls = zip(*[(dhash := find_job_data_hash(job), dhash["tc"], dhash["link"])
              for job in raw_jobs])
        existed_tcs = previous_company_wise_titles(list(tcs))
        existed_urls = previous_jobs(source='workable', urls=list(urls))
        for job in list(jobs):
            try:
                if existed_urls.get(job["link"]) or existed_tcs.get(job["tc"]): 
                    continue
                data = []
                driver.get(job["link"])
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "jobBreakdown__job-breakdown--31MGR"))
                )
                job_title = driver.find_element(
                    By.CLASS_NAME, "jobOverview__job-title--kuTAQ")
                append_data(data, job_title.text)
                company_name = driver.find_element(
                    By.CLASS_NAME, "companyName__link--2ntbf")
                append_data(data, company_name.text)
                address = driver.find_elements(
                    By.CLASS_NAME, "jobDetails__job-detail--3As6F")[1]
                append_data(data, address.text)
                job_description = driver.find_element(
                    By.CLASS_NAME, "jobBreakdown__job-breakdown--31MGR")
                append_data(data, job_description.text)
                append_data(data, driver.current_url)
                job_posted_date = driver.find_element(
                    By.CLASS_NAME, "jobOverview__date-posted-container--9wC0t")
                append_data(data, job_posted_date.text)
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "N/A")
                append_data(data, "Workable")
                try:
                    job_type_check = driver.find_element(
                        By.CLASS_NAME, "jobOverview__job-details--3JOit")
                    if 'contract' in job_type_check.text.lower():
                        append_data(data, set_job_type('Contract', determine_job_sub_type(job_type_check.text)))
                    elif 'full time' in job_type_check.text.lower():
                        append_data(data, set_job_type('Full time', determine_job_sub_type(job_type_check.text)))
                    else:
                        append_data(data, set_job_type(job_type))
                except Exception as e:
                    saveLogs(e)
                    append_data(data, set_job_type(job_type))
                append_data(data, job_description.get_attribute('innerHTML'))
                scrapped_data.append(data)
            except Exception as e:
                saveLogs(e)
        if scrapped_data:
            export_to_excel(scrapped_data, ScraperNaming.WORKABLE, 'Workable')
    except Exception as e:
        saveLogs(e)

def determine_job_sub_type(type):
    sub_type = 'onsite'
    if 'remote' in type.lower():
        sub_type = 'remote'
    if 'hybrid' in type.lower():
        sub_type = 'hybrid'
    return sub_type
    

@log_scraper_running_time("Workable")
def workable(link, job_type):
    driver = configure_webdriver(block_media=True, block_elements=['img'])
    try:
        driver.maximize_window()
        try:
            flag = True
            driver.get(link)
            driver.maximize_window()
            accept_cookie(driver)
            count = 0
            while flag:
                flag, count = loading(driver, count)
            find_jobs(driver, job_type)
        except Exception as e:
            saveLogs(e)
    except Exception as e:
        saveLogs(e)
    driver.quit()
    