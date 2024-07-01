import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.constants.const import *
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, sleeper, configure_undetected_chrome_driver, previous_jobs
from utils.helpers import saveLogs

# calls url
def request_url(driver, url):
    driver.get(url)

# append data for csv file
def append_data(data, field):
    data.append(str(field).strip("+"))

def findLinks(driver):
    links = []
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "grid"))
    )  
    sleeper() 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    sleeper()
    jobs = driver.find_elements(By.XPATH, '//*[@id="posts-index"]/section[2]/div/div/div[2]/div')
    links = [job.find_elements(By.TAG_NAME, "a")[1].get_attribute("href") for job in jobs if len(job.find_elements(By.TAG_NAME, "a")) > 1]
    sleeper()
    try:
        target_element = WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((By.XPATH, '/html/body/section[2]/div/div/a')))
        request_url(driver,target_element.get_attribute("href"))
        return True, links
    except:
        return False, links
    

# find's job name
def find_jobs(driver, job_type):
    scrapped_data = []
    scraped_links=[]
    flag = True

    while flag:
        flag, links = findLinks(driver)
        scraped_links.extend(links)
    existed_jobs = previous_jobs(source="startup",urls=scraped_links)
    for link in scraped_links:
        try:
            if existed_jobs.get(link):
                continue
            data = []
            request_url(driver,link)
            sleeper()
            title = driver.find_element(By.CLASS_NAME, 'visualHeader__title').text
            append_data(data, title)
            company_name = driver.find_element(By.CLASS_NAME, 'visualHeader__subtitle').text.split('IS')[0]
            append_data(data, company_name)
            
            try:
                address = driver.find_element(By.CLASS_NAME, 'jobListing__main__meta__location').text
            except:
                address = driver.find_element(By.CLASS_NAME, 'jobListing__main__meta__remote').text
            append_data(data, address)

            description = driver.find_element(By.CLASS_NAME, 'trix-content').text
            job_description_tags = driver.find_element(By.CLASS_NAME, 'trix-content').get_attribute('innerHTML')
            append_data(data, description)
            append_data(data, link)            
            append_data(data, 'N/A')           
            append_data(data, 'N/A')
            append_data(data, 'N/A')
            append_data(data, 'N/A')
            append_data(data, 'N/A')
            append_data(data, 'startup')
            append_data(data, job_type)
            append_data(data, job_description_tags)
            scrapped_data.append(data)
        except Exception as e:
            saveLogs(e)
    if len(scrapped_data) > 0:
        export_to_excel(scrapped_data)

def export_to_excel(scrapped_data):
    df = pd.DataFrame(data=scrapped_data, columns=COLUMN_NAME)
    filename = generate_scraper_filename("start_up")
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(total_jobs=len(df), job_source="StartUp", filename=filename)

# code starts from here
def startup(link, job_type):
    driver = configure_undetected_chrome_driver()
    try:
        driver.maximize_window()
        sleeper()
        request_url(driver, link)
        find_jobs(driver, job_type)
    except Exception as e:
        saveLogs(e)
    driver.quit()
