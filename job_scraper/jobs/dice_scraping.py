from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from job_scraper.constants.const import *
from selenium import webdriver

import pandas as pd
import time

class DiceScraping:

  # returns driver
  def driver():
    return webdriver.Chrome()

  # calls url
  def request_url(driver, url):
    driver.get(url)

  # append data for csv file
  def append_data(data, field):
    data.append(str(field).strip("+"))

  # find's job name
  def find_jobs(driver, scrapped_data):
    count = 0
    WebDriverWait(driver, 30).until(
      EC.presence_of_element_located((By.CLASS_NAME, "card-title-link"))
    )
    jobs = driver.find_elements(By.TAG_NAME, "dhi-search-card")

    for job in jobs:
      data = []

      job_title = driver.find_elements(By.CLASS_NAME,"card-title-link")
      DiceScraping.append_data(data, job_title[count].text)
      c_name = driver.find_elements(By.CLASS_NAME,"card-company")
      company_name = c_name[count].find_elements(By.TAG_NAME,"a")
      for company in company_name:
        DiceScraping.append_data(data, company.text)
      address = driver.find_elements(By.CLASS_NAME,"search-result-location")
      DiceScraping.append_data(data, address[count].text)
      job_description = driver.find_elements(By.CLASS_NAME,"card-description")
      DiceScraping.append_data(data, job_description[count].text)
      DiceScraping.append_data(data, driver.current_url)
      job_posted_date = driver.find_elements(By.CLASS_NAME,"posted-date")
      DiceScraping.append_data(data, job_posted_date[count].text)

      count += 1
      scrapped_data.append(data)

    finished = "disabled"
    pagination = driver.find_elements(By.CLASS_NAME, "pagination-next")
    next_page = pagination[0].get_attribute('class')
    if finished in next_page:
      columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date"]
      df = pd.DataFrame(data=scrapped_data, columns=columns_name)
      df.to_csv("dice_results.csv")
      return False
    else:
      pagination[0].click()
      time.sleep(5)

    return True

# code starts from here
def dice():
  scrapped_data = []
  scrap = DiceScraping
  driver = scrap.driver()
  scrap.request_url(driver, DICE_RESULTS)
  while scrap.find_jobs(driver, scrapped_data):
    columns_name = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date"]
    df = pd.DataFrame(data=scrapped_data, columns=columns_name)
    df.to_csv(DICE_CSV)
  print(SCRAPING_ENDED)
