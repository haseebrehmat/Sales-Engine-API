import traceback
from typing import List, Union, Set
import pandas as pd
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, \
    ElementNotVisibleException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from scraper.models.scraper_logs import ScraperLogs
from scraper.utils.helpers import generate_scraper_filename, ScraperNaming, configure_webdriver, run_pia_proxy, previous_jobs, sleeper
from utils.helpers import log_scraper_running_time, saveLogs

class LinkedinScraper:
    def __init__(self, driver, url) -> None:
        self.driver: WebDriver = driver
        self.url: str = url
        self.links: Set[str] = []
        self.scraped_jobs: List[dict] = []
        self.job: dict = {}
        self.errs: List[dict] = []

    @classmethod
    def call(cls, url, job_type):
        driver: WebDriver = configure_webdriver(
            block_media=True,
            block_elements=['img', 'cookies']
        )
        try:
            driver.maximize_window()
            run_pia_proxy(driver)
            linkdedin_scraper: cls.__class__ = cls(driver=driver, url=url)
            linkdedin_scraper.find_jobs(job_type)
        except Exception as e:
            cls.handle_exception(e)
        driver.quit()

    def request_page(self) -> None:
        self.driver.get(self.url)

    def handle_exception(self, exception: Union[Exception, str]) -> None:
        saveLogs(exception)
        traceback.format_exc()
        traceback_data = traceback.extract_tb(exception.__traceback__)
        if traceback_data and traceback_data[0]:
            self.errs.append({
                'scraper': 'linkedin',
                'file_path': traceback_data[0].filename or "",
                'line_number': traceback_data[0].lineno or "",
                'error_line': traceback_data[0].line or "",
                'from_function': traceback_data[0].name or ""
            })

    def get_element(self, locator: str, parent: WebElement = None, selector: str = 'class',
                    alls: bool = False) -> Union[WebElement, List[WebElement], None]:
        try:
            by: str = By.CLASS_NAME
            if selector == 'css':
                by: str = By.CSS_SELECTOR
            if selector == 'xpath':
                by: str = By.XPATH
            if selector == 'tag':
                by: str = By.TAG_NAME
            if selector == 'name':
                by: str = By.NAME  # For Input fields
            wait: WebDriverWait = WebDriverWait(parent or self.driver, 10)
            ec: EC = EC.presence_of_all_elements_located((by, locator)) if alls else EC.presence_of_element_located(
                (by, locator))
            return wait.until(ec)
        except (
                WebDriverException, TimeoutException, NoSuchElementException, ElementNotVisibleException,
                Exception) as e:
            self.handle_exception(e)
            return None

    def home_page_loaded(self) -> bool:
        loaded: bool = False
        for retry in range(1, 6):
            try:
                self.request_page()
                homepage_element: WebElement = self.get_element(
                    locator='jobs-search__results-list')
                if homepage_element:
                    loaded = True
                    break
            except (WebDriverException, TimeoutException, NoSuchElementException, ElementNotVisibleException) as e:
                if retry < 5:
                    print(f"Retry {retry}/{5} due to: {e}")
                else:
                    self.handle_exception(e)
                    self.driver.quit()
                    break
        return loaded

    def extract_links(self) -> None:
        load_more_btn: WebElement = self.get_element(
            locator="infinite-scroller__show-more-button"
        )
        no_more_jobs_alert: WebElement = self.get_element(
            locator="see-more-jobs__viewed-all"
        )
        if not load_more_btn and not no_more_jobs_alert:
            return
        
        while not ((no_more_jobs_alert and no_more_jobs_alert.is_displayed()) or (load_more_btn and load_more_btn.is_displayed())):
            sleeper()
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of(load_more_btn))
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of(no_more_jobs_alert))
            except TimeoutException:
                continue
        curr_jobs = self.populate_links(0)
        while not no_more_jobs_alert.is_displayed():
            load_more_btn.click()
            curr_jobs = self.populate_links(curr_jobs)
            if curr_jobs == 0:
                break

    def populate_links(self, previous_len) -> int:
        sleeper()
        jobs_list: list[WebElement] = self.get_element(
            locator='base-card__full-link',
            alls=True
        )
        start = len(self.links)
        for item in jobs_list[start:]:
            if item:
                self.links.append(item.get_attribute('href').split('?')[0])
        return 0 if len(jobs_list)==previous_len else len(jobs_list)

    def find_jobs(self, job_type) -> None:
        try:
            if self.home_page_loaded():
                self.extract_links()
            existing_jobs = previous_jobs(source='linkedin', urls=self.links)
            if len(self.links) > 0:
                for url in self.links:
                    if existing_jobs.get(url):
                        continue
                    try:
                        self.job['job_source_url'] = url
                        self.job['job_source'] = 'linkedin'
                        self.job['job_type'] = job_type
                        self.driver.get(url=url)
                        visited: bool = self.tab_visited()
                        if visited:
                            self.scraped_jobs.append(self.job.copy())
                            self.job = {}
                        else:
                            continue
                    except Exception as e:
                        self.handle_exception(e)
                        continue
            self.driver.quit()
            self.export_to_excel() if len(self.scraped_jobs) > 0 else None
        except Exception as e:
            self.handle_exception(e)
            self.driver.quit()

    def populate_salary(self):
        try:
            salaryElement = self.get_element(locator='compensation__salary').text
            if 'yr' in salaryElement:
                self.job['salary_format'] = 'yearly'
            elif 'hr' in salaryElement:
                self.job['salary_format'] = 'hourly'
            else:
                self.job['salary_format'] = 'N/A'
            self.job['estimated_salary'] = salaryElement
            salary = salaryElement.split('-')
            salary_min = salary[0].split('/')
            salary_max = salary[1].split('/')
            self.job['salary_min'] = salary_min[0]
            self.job['salary_max'] = salary_max[0]
        except:
            self.job["salary_format"] = "N/A"
            self.job["estimated_salary"] = "N/A"
            self.job["salary_min"] = "N/A"
            self.job["salary_max"] = "N/A"

    def tab_visited(self) -> bool:
        title = self.get_element(locator='top-card-layout__title').text
        self.job['job_title'] = title
        company_name = self.get_element(locator='topcard__org-name-link').text
        self.job['company_name'] = company_name
        address = self.get_element(locator='topcard__flavor--bullet').text
        self.job['address'] = address
        date_posted = self.get_element(locator='posted-time-ago__text').text        
        self.job['job_posted_date'] = date_posted
        self.populate_salary()
        button = self.get_element(locator='show-more-less-html__button')
        button.click()
        description = self.get_element(locator='show-more-less-html__markup')
        self.job['job_description'] = description.text
        self.job["job_description_tags"] = description.get_attribute('innerHTML')
        return True

    def export_to_excel(self) -> None:
        columns_name: list[str] = ["job_title", "company_name", "address", "job_description", 'job_source_url', "job_posted_date", "salary_format",
                                   "estimated_salary", "salary_min", "salary_max", "job_source", "job_type", "job_description_tags"]
        df = pd.DataFrame(data=self.scraped_jobs, columns=columns_name)
        filename: str = generate_scraper_filename(
            ScraperNaming.LINKEDIN)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(
            total_jobs=len(df), job_source="Linkedin", filename=filename)

@log_scraper_running_time("LinkedIn")
def linkedin(url: str, job_type: str) -> None:
    LinkedinScraper.call(url, job_type)
