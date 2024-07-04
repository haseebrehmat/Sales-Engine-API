from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, \
    ElementNotVisibleException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.db.models.query import QuerySet

from job_portal.models import JobDetail
from scraper.models.scraper_logs import ScraperLogs
from scraper.constants.const import COLUMN_NAME, PIA_EXTENSION_PATH, HIDE_ELEMENTS
from utils.helpers import saveLogs

from pandas import DataFrame
from typing import List, Union, Set
import datetime


class BaseScraper:
    def __init__(self, url: str, headless: bool = True, block_elements: List = []) -> None:

        self.driver: WebDriver = self.configure_webdriver(
            headless, block_elements)
        self.driver.maximize_window()
        self.url: str = url
        self.previous_links: dict = {}
        self.scraped_jobs: List[dict] = []
        self.job: dict = {}

    def configure_webdriver(self, headless: bool = True, block_elements: List = []) -> WebDriver:
        options: Options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless=new")
        if block_elements:
            hide_elements: dict = HIDE_ELEMENTS
            if 'cookies' in block_elements:
                hide_elements.update({'cookies': 2})
            if 'js' in block_elements:
                hide_elements.update({'javascript': 2})
            if 'img' in block_elements:
                hide_elements.update({'images': 2})
            prefs: dict = {
                'profile.default_content_setting_values': hide_elements}
            options.add_argument('--disable-features=EnableNetworkService')
            options.add_argument('--blink-settings=imagesEnabled=false')
            options.add_experimental_option('prefs', prefs)
        options.add_argument("window-size=1200,1100")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")

        options.add_extension(PIA_EXTENSION_PATH)

        driver: WebDriver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)

        if block_elements:
            # Enable Chrome DevTools Protocol
            driver.execute_cdp_cmd("Page.enable", {})
            driver.execute_cdp_cmd("Network.enable", {})

            # Set blocked URL patterns to disable images and stylesheets
            blocked_patterns: List = []
            if 'img' in block_elements:
                blocked_patterns.extend(
                    ["*.jpg", "*.jpeg", "*.png", "*.gif", ])
            if 'css' in block_elements:
                blocked_patterns.extend(["*.css"])
            if 'js' in block_elements:
                blocked_patterns.extend(["*.js"])
            driver.execute_cdp_cmd("Network.setBlockedURLs", {
                                   "urls": blocked_patterns})
        return driver

    def get_previous_jobs(self, job_source: str, urls: List = []) -> None:
        jobs: QuerySet[JobDetail] = JobDetail.objects.filter(
            job_source=job_source)
        if len(urls) > 0:
            jobs = jobs.filter(job_source_url__in=urls)
        previous_jobs: Set = set(jobs.values_list('job_source_url', flat=True))
        self.previous_jobs = {job: True for job in previous_jobs}

    def generate_scraper_filename(self, job_source: str) -> None:
        date_time: str = str(datetime.datetime.now())
        return f'scraper/job_data/{job_source} - {date_time}.xlsx'

    def export_to_excel(self, scraper_name: str, job_source: str) -> None:
        df: DataFrame = DataFrame(data=self.scraped_jobs, columns=COLUMN_NAME)
        filename: str = self.generate_scraper_filename(scraper_name)
        df.to_excel(filename, index=False)
        ScraperLogs.objects.create(
            total_jobs=len(df), job_source=job_source, filename=filename)

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
            saveLogs(e)
            return None

    def delete_self(self):
        self.driver.quit()
        del self
