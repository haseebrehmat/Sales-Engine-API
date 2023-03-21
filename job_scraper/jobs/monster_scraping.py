from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from job_scraper.constants.const import *
from selenium import webdriver
import pandas as pd
import time


class MonsterScraping:

    # returns driver
    def driver():
        return webdriver.Chrome()

    # calls url
    def request_url(driver, url):
        driver.get(url)

    # append data for csv file
    def append_data(data, field):
        data.append(str(field).strip("+"))

    def load_jobs(driver):
        finished = "No More Results"
        button = driver.find_element(By.CLASS_NAME, "job-search-resultsstyle__LoadMoreContainer-sc-1wpt60k-1")
        data_exists = button.find_element(By.TAG_NAME, "span")

        if finished in data_exists.text:
            return False

        return True

    # find's job name
    def find_jobs(driver, scrapped_data):
        count = 0

        time.sleep(7)

        while MonsterScraping.load_jobs(driver):
            jobs = driver.find_elements(By.CLASS_NAME, "job-search-resultsstyle__JobCardWrap-sc-1wpt60k-5")
            for job in jobs:
                job.click()
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "descriptionstyles__DescriptionContainer-sc-13ve12b-0"))
                )

        jobs = driver.find_elements(By.CLASS_NAME, "job-search-resultsstyle__JobCardWrap-sc-1wpt60k-5")
        for job in jobs:
            data = []
            job.click()
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "descriptionstyles__DescriptionContainer-sc-13ve12b-0"))
            )
            job_title = driver.find_element(By.CLASS_NAME, "headerstyle__JobViewHeaderTitle-sc-1ijq9nh-5")
            MonsterScraping.append_data(data, job_title.text)
            company_name = driver.find_element(By.CLASS_NAME, "headerstyle__JobViewHeaderCompany-sc-1ijq9nh-6")
            MonsterScraping.append_data(data, company_name.text)
            address = driver.find_element(By.CLASS_NAME, "headerstyle__JobViewHeaderLocation-sc-1ijq9nh-4")
            MonsterScraping.append_data(data, address.text)
            job_description = driver.find_element(By.CLASS_NAME, "descriptionstyles__DescriptionBody-sc-13ve12b-4")
            MonsterScraping.append_data(data, job_description.text)
            url = driver.find_elements(By.CLASS_NAME, "job-cardstyle__JobCardTitle-sc-1mbmxes-2")
            MonsterScraping.append_data(data, url[count].get_attribute('href'))
            job_posted_date = driver.find_element(By.CLASS_NAME,
                                                  "detailsstyles__DetailsTableDetailPostedBody-sc-1deoovj-6")
            MonsterScraping.append_data(data, job_posted_date.text)

            scrapped_data.append(data)
        count += 1

        columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date"]
        df = pd.DataFrame(data=scrapped_data, columns=columns_name)
        df.to_csv(MONSTER_CSV)

    # check if there is more jobs available or not
    def data_exists(driver):
        pagination = driver.find_element(By.CLASS_NAME, "nextButton")
        next_page = pagination.get_attribute('disabled')
        return False if next_page else True


# code starts from here
def monster():
    scrapped_data = []
    scrap = MonsterScraping
    driver = scrap.driver()
    driver.maximize_window()
    scrap.request_url(driver, MONSTER_REMOTE_RESULTS)
    scrap.find_jobs(driver, scrapped_data)
    print(SCRAPING_ENDED)
