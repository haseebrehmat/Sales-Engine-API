from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from scraper.constants.const import *
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, previous_jobs
from utils.helpers import saveLogs
import time
import pandas as pd
from scraper.models.scraper_logs import ScraperLogs
from typing import List
from job_portal.models import JobDetail

class SimplyHiredScraper:

    def __init__(self, driver, url, type) -> None:
        self.driver: WebDriver = driver
        self.url: str = url
        self.job_type: str = type
        self.scraped_jobs: List[dict] = []
        self.scrape_job_urls: List[str] = []
        self.job: dict = {}

    @classmethod
    def call(cls, url, type):
        print("Running Simply Hired...")
        try:
            driver: WebDriver = configure_webdriver()
            driver.maximize_window()
            simply_hired_scraper: cls.__class__ = cls(
                driver=driver, url=url, type=type)
            simply_hired_scraper.driver.get(url)

            try:
                flag = True
                page_no = 2
                while flag and page_no <= 40:
                    flag = simply_hired_scraper.find_urls(page_no)
                    page_no += 1
                if len(simply_hired_scraper.scrape_job_urls) > 0:
                    existing_jobs_dictionary = previous_jobs(source='simplyhired', urls=simply_hired_scraper.scrape_job_urls) 
                    simply_hired_scraper.find_jobs(existing_jobs_dictionary)
                if len(simply_hired_scraper.scraped_jobs) > 0:             
                    simply_hired_scraper.export_to_excel()
                simply_hired_scraper.driver.quit()
            except Exception as e:
                saveLogs(e)
        except Exception as e:
            saveLogs(e)
        print("Done Simply Hired...")

    def find_urls(self, next_page_no):
        jobs = self.driver.find_elements(By.CLASS_NAME,"css-1igwmid")
        for job in jobs:
            job_url = job.find_element(
                    By.CSS_SELECTOR, "h2 > .css-1djbb1k").get_attribute("href") 
            self.scrape_job_urls.append(job_url)   
        try:
            next_page = self.driver.find_elements(By.CLASS_NAME, "css-1vdegr")
            next_page_clicked = False
            for i in next_page:
                if i.text == f'{next_page_no}':
                    i.click()
                    time.sleep(3)
                    next_page_clicked = True
                    break
            return next_page_clicked
        except Exception as e:
            saveLogs(e)
            self.driver.quit()
            return False   

    def populate_salary(self,context):
        salary = context[3].text
        if len(context) == 5:
            estimated_salary = salary.split(' a')[0]
            if "d: " in estimated_salary:
                estimated_salary = estimated_salary.split(": ")[1]
            if "to " in estimated_salary:
                estimated_salary = estimated_salary.split("to ")[1]
            self.job["estimated_salary"] = k_conversion(
                                estimated_salary)
            try:
                self.job["salary_min"] = k_conversion(
                            estimated_salary.split(' - ')[0])
            except:
                self.job["salary_min"] = "N/A"
            try:
                self.job["salary_max"] = k_conversion(
                            estimated_salary.split(' - ')[1])
            except:
                self.job["salary_max"] = "N/A"           
            if 'year' in salary:
                salary_format = 'yearly'
            elif 'month' in salary:
                salary_format = 'monthly'
            elif 'day' in salary:
                salary_format = 'daily'
            elif 'hour' in salary:
                salary_format = 'hourly'
            else:
                salary_format = 'N/A'
            self.job['salary_format'] = salary_format

            job_posted_date = context[4].text
        else:
            self.job["estimated_salary"] = 'N/A'
            self.job["salary_min"] = 'N/A'
            self.job["salary_max"] = 'N/A'
            self.job['salary_format'] = 'N/A'
            job_posted_date = context[3].text
        self.job['job_posted_date'] = job_posted_date             

    def find_jobs(self,existing_jobs_dictionary):
        for job in self.scrape_job_urls:
            if existing_jobs_dictionary.get(job):
                continue
            try:
                self.driver.get(job)
                job_title = self.driver.find_element(By.CLASS_NAME,'css-yvgnf2').text
                self.job['job_title'] = job_title
                context = self.driver.find_elements(By.CLASS_NAME,'css-xyzzkl')
                try:
                    company_name = context[0].text.split('-')[0]
                except:
                    company_name = context[0].text
                self.job['company_name'] = company_name
                address = context[1].text
                self.job['address'] = address
                self.job['job_source_url'] = job
                self.job['job_source'] = 'simplyhired'
                self.job['job_type'] = self.job_type
                
                self.populate_salary(context)
                
                descriptions = self.driver.find_elements(By.CLASS_NAME,'css-10747oj')
                self.job['job_description'] = descriptions[1].text
                self.job['job_description_tags'] = descriptions[1].get_attribute('innerHTML')

                self.scraped_jobs.append(self.job.copy())
                self.job = {}
            except Exception as e:
                saveLogs(e)
    

    def export_to_excel(self) -> None:
        columns_name: list[str] = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                                   "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=self.scraped_jobs, columns=columns_name)
        filename: str = generate_scraper_filename(
            ScraperNaming.SIMPLY_HIRED)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Simply Hired", filename=filename)


def simply_hired(url:str, job_type:str) -> None:
    print('simplyhired started')
    SimplyHiredScraper.call(url, job_type)
    print('simplyhired ended')
