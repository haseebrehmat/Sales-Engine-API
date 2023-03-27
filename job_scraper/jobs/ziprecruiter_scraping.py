from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from job_scraper.constants.const import ZIP_RECRUITER_CSV

links = [
    'https://www.ziprecruiter.com/candidate/search?search=Developer&location=USA&refine_by_location_type=no_remote&radius=100&days=1&refine_by_salary=&refine_by_tags=employment_type%3Afull_time&refine_by_title=&refine_by_org_name=',
    'https://www.ziprecruiter.com/candidate/search?search=Developer&location=USA&refine_by_location_type=&radius=100&days=1&refine_by_salary=&refine_by_tags=employment_type%3Acontract&refine_by_title=&refine_by_org_name=',
    'https://www.ziprecruiter.com/candidate/search?search=Developer&location=USA&refine_by_location_type=only_remote&radius=100&days=1&refine_by_salary=&refine_by_tags=employment_type%3Afull_time&refine_by_title=&refine_by_org_name=',
]


def ziprecruiter_scraping():
    driver = webdriver.Chrome()
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    details_window = driver.current_window_handle
    all_data = []
    for i in links:
        driver.switch_to.window(original_window)
        next_link = i
        while 'candidate' in next_link:
            driver.switch_to.window(original_window)
            driver.get(next_link)
            try:
                job_search = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-type='job_results']"))
                )
            except:
                continue

            for job in job_search.find_elements(By.TAG_NAME, 'article'):
                driver.switch_to.window(original_window)
                job_detail = {'job_title': job.get_attribute('data-job-title'),
                              'company_name': job.get_attribute('data-company-name'),
                              'job_source': job.get_attribute('data-posted-on'),
                              'address': job.get_attribute('data-location'),
                              'job_type': job.find_element(By.XPATH, "//section[@class='perks_item perks_type']").text,
                              'job_description': job.find_element(By.XPATH,
                                                                  "//p[@data-tracking='job_description']").text,
                              'job_source_url': job.find_element(By.TAG_NAME, 'a').get_attribute('href')
                              }
                if 'https://www.ziprecruiter.com/k' in job_detail['job_source_url']:
                    driver.switch_to.window(details_window)
                    driver.get(job_detail['job_source_url'])
                    job_data = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='job_more_section']"))
                    )
                    for single_job in job_data.find_elements(By.XPATH, "//p[@class='job_more']"):
                        if 'Posted date:' in single_job.text:
                            job_detail['job_posted_date'] = single_job.text
                else:
                    job_detail['job_posted_date'] = 'Today'

                all_data.append(job_detail)
            next_link = 'https://www.ziprecruiter.com' + job_search.get_attribute('data-next-url')

    df = pd.DataFrame.from_dict(all_data)
    df['job_description'] = df['job_description'].str.replace('<.*?>', '', regex=True)
    df['job_posted_date'] = df['job_posted_date'].str.replace('Posted date: ', '')
    df['job_type'] = df['job_type'].str.replace('Type\n', '')
    df.to_csv(ZIP_RECRUITER_CSV, index=False)
    driver.close()
