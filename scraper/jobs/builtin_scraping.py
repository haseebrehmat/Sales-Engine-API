from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, k_conversion, configure_webdriver, set_job_type, run_pia_proxy, change_pia_location, previous_jobs, sleeper
import pandas as pd
from scraper.models.scraper_logs import ScraperLogs
from utils.helpers import saveLogs, log_scraper_running_time

class BuiltinScraper:

    def __init__(self, driver, url, type):
        self.driver: WebDriver = driver
        self.url: str = url
        self.job_type: str = type
        self.scraped_jobs: List[dict] = []
        self.job: dict = {}
        self.errs: List[dict] = []   

    @classmethod
    def call(cls,url,type):
        try:
            driver: WebDriver = configure_webdriver()
            builtin_scraper: cls.__class__ = cls(
                driver=driver, url=url, type=type) 
            try:
                flag = True
                builtin_scraper.driver.maximize_window()
                run_pia_proxy(builtin_scraper.driver)
                sleeper()
                builtin_scraper.driver.get(url)
                existing_jobs = previous_jobs(source='builtin')
                while flag:
                    flag= builtin_scraper.find_jobs(existing_jobs)
                if len(builtin_scraper.scraped_jobs) > 0:
                    builtin_scraper.export_to_excel()
            except Exception as e:
                saveLogs(e)
            finally:
                builtin_scraper.driver.quit()
 
        except:
            pass           

    def find_jobs(self, existing_jobs_dictionary):
        try:
            sleeper()
            links = self.driver.find_elements(By.CSS_SELECTOR, "a[data-id='view-job-button']")
            job_details = self.driver.find_elements(By.CLASS_NAME, "job-bounded-responsive")
            job_links = []
            job_det = []

            for link, job in zip(links,job_details):
                cur_link = link.get_attribute('href') 
                if existing_jobs_dictionary.get(cur_link):
                    continue
                job_links.append(cur_link)
                job_det.append(job.text)


            original_window = self.driver.current_url

            retries  = 5
            for i, url in enumerate(job_links):
                try:
                    job_detail = job_det[i].split('\n')
                    self.job["job_title"] = job_detail[1]
                    self.job["company_name"] = job_detail[0]
                    self.job["job_source"] = "Builtin"
                    self.job["job_posted_date"] = job_detail[2]
                    self.driver.get(url)
                    sleeper()
                    outer_loop_exit = False
                    for retry in range(retries):
                        try:
                            self.driver.find_element(By.ID, "read-more-description-toggle").click()
                            sleeper()
                            break
                        except Exception as e:
                            if retry == retries:
                                outer_loop_exit = True
                                break
                            error_status = change_pia_location(self.driver)
                            if not error_status:
                                self.driver.get(url)
                            else:
                                outer_loop_exit = True
                                break
                    if outer_loop_exit:
                        continue
                    try:
                        address = self.driver.find_element(By.CLASS_NAME, "company-address").text
                    except:
                        try:
                            address = self.driver.find_element(By.CLASS_NAME, "icon-description").text
                        except:
                            address = 'USA'
                    self.job["address"] = address
                    job_description = self.driver.find_element(By.CLASS_NAME, "job-description")
                    self.job["job_description"] = job_description.text
                    self.job["job_source_url"] = self.driver.current_url
                    self.populate_salary()
                    try:
                        job_type_check = self.driver.find_element(By.CLASS_NAME, "company-info")
                        if 'remote' in job_type_check.text.lower():
                            self.job["job_type"] = set_job_type('Full time', 'remote')
                        elif 'hybrid' in job_type_check.text.lower():
                            self.job["job_type"] = set_job_type('Full time', 'hybrid')
                        else:
                            self.job["job_type"] = set_job_type('Full time', 'onsite')
                    except Exception as e:
                        try:
                            job_type_check = self.driver.find_element(By.CLASS_NAME, "company-options")
                            if 'remote' in job_type_check.text.lower():
                                self.job["job_type"] = set_job_type('Full time', 'remote')
                            elif 'hybrid' in job_type_check.text.lower():
                                self.job["job_type"] = set_job_type('Full time', 'hybrid')
                            else:
                                self.job["job_type"] = set_job_type('Full time', 'onsite')
                        except Exception as e:
                            saveLogs(e)
                            self.job["job_type"] = set_job_type(self.job_type)
                    self.job["job_description_tags"] = job_description.get_attribute('innerHTML')

                    self.scraped_jobs.append(self.job.copy())
                    self.job = {}
                except Exception as e:
                    saveLogs(e)
                

                # switch_tab(driver, c, original_window)

            try:
                self.driver.get(original_window)
                sleeper()
                next_page = self.driver.find_element(By.CLASS_NAME, 'pagination')
                pagination = next_page.find_elements(By.TAG_NAME, 'li')
                next_page_anchor = pagination[-1].find_element(By.TAG_NAME, 'a')
                next_page_url = next_page_anchor.get_attribute('href')
                self.driver.get(next_page_url)
                return True
            except Exception as e:
                return False
        except Exception as e:
            saveLogs(e)
            return False


    def populate_salary(self):
        try:
            estimated_salary = self.driver.find_element(By.CLASS_NAME, "provided-salary")
            salary = estimated_salary.text
            if 'hour' in salary:
                 self.job["salary_format"] = "hourly"
            elif 'Annually' in salary or 'ANNUALLY' in salary:
                self.job["salary_format"] = "yearly"
            elif 'month' in salary:
                self.job["salary_format"] = "monthly"
            else:
                self.job["salary_format"] = "N/A"
            try:
                self.job["estimated_salary"] = k_conversion(salary.split(' A')[0])
            except:
                self.job["estimated_salary"] = "N/A"
            try:
                salary_min = salary.split('A')[0].split('-')[0]
                self.job["salary_min"] = k_conversion(salary_min)
            except:
                self.job["salary_min"] = "N/A"
            try:
                salary_max = salary.split('A')[0].split('-')[1]
                self.job["salary_max"] = k_conversion(salary_max)
            except:
                self.job["salary_max"] = "N/A"
        except:
            self.job["salary_format"] = "N/A"
            self.job["estimated_salary"] = "N/A"
            self.job["salary_min"] = "N/A"
            self.job["salary_max"] = "N/A"


    def export_to_excel(self) -> None:
        columns_name: list[str] = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                                   "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=self.scraped_jobs, columns=columns_name)
        filename: str = generate_scraper_filename(
            ScraperNaming.BUILTIN)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Builtin", filename=filename)

@log_scraper_running_time("Builtin")
def builtin(link, job_type):
    BuiltinScraper.call(link, job_type)

