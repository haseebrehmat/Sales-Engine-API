import datetime
import random
import re
import time
import pandas as pd

from django.db.models import Value, CharField, functions as fn
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from scraper.constants.const import JOB_TYPE, COLUMN_NAME
from scraper.models import GroupScraper, GroupScraperQuery
from scraper.models.accounts import Accounts
from job_portal.models import JobDetail
from scraper.models.scraper_logs import ScraperLogs

def convert_time_into_minutes(interval, interval_type):
    if interval_type.lower() == 'minutes':
        pass
    elif interval_type.lower() == 'hours':
        interval = interval * 60
    elif interval_type.lower() == 'days':
        interval = interval * 60 * 24

    return interval


def is_valid_group_scraper_time(time, week_days, group_scraper=None):
    estimated_query_time = 15
    groups = GroupScraper.objects.exclude(scheduler_settings__time=None)
    days = week_days.lower().split(',')
    time = datetime.datetime.strptime(time, "%H:%M:%S")
    for x in groups:
        scheduler_weekdays = x.scheduler_settings.week_days
        scheduler_weekdays = scheduler_weekdays.split(",")
        # check = [scheduler_week_day for scheduler_week_day in scheduler_weekdays if scheduler_week_day in days]
        group_scraper_query = GroupScraperQuery.objects.filter(group_scraper=x).first()

        if group_scraper_query:
            if group_scraper_query.group_scraper == group_scraper:
                continue
            queries_count = len(group_scraper_query.queries)
            estimated_time = queries_count * estimated_query_time
            scraper_start_time = datetime.datetime.strptime(str(x.scheduler_settings.time), "%H:%M:%S")
            estimated_scraper_end_time = scraper_start_time + datetime.timedelta(minutes=estimated_time)
            estimated_scraper_end_time = estimated_scraper_end_time.strftime("%H:%M:%S")

            if str(scraper_start_time.time()) <= str(time.time()) <= str(estimated_scraper_end_time):
                return False
    return True


import enum


class ScraperNaming(enum.Enum):
    ADZUNA = 'adzuna'
    GLASSDOOR = 'glassdoor'
    CAREER_BUILDER = 'career_builder'
    CAREERJET = 'careerjet'
    INDEED = 'indeed'
    LINKEDIN = 'linkedin'
    LINKEDIN_GROUP = 'linkedin_group'
    DICE = 'dice'
    GOOGLE_CAREERS = 'google_careers'
    JOOBLE = 'jooble'
    HIRENOVICE = 'hirenovice'
    DAILY_REMOTE = 'dailyremote'
    MONSTER = 'monster'
    SIMPLY_HIRED = 'simply_hired'
    TALENT = 'talent'
    ZIP_RECRUITER = 'ziprecruiter'
    RECRUIT = 'recruit'
    RUBY_NOW = 'rubynow'
    YCOMBINATOR = 'ycombinator'
    WORKING_NOMADS = 'working_nomads'
    WORKOPOLIS = 'workopolis'
    DYNAMITE = 'dynamite'
    ARC_DEV = 'arcdev'
    REMOTE_OK = 'remoteok'
    HIMALAYAS = 'himalayas'
    USJORA = 'usjora'
    STARTWIRE =  'startwire'
    JOB_GETHER = 'job_gether'
    RECEPTIX = 'receptix'
    BUILTIN = 'builtin'
    WORKABLE = 'workable'
    THE_MUSE = 'themuse'
    CLEARANCE = 'clearance'
    SMARTRECRUITER = 'smartrecruiter'
    GETWORK = 'getwork'
    RUBY_ON_REMOTE = 'rubyonremote'
    HUBSTAFF_TALENT = 'hubstaff_talent'
    JUST_REMOTE = 'just_remote'
    REMOTE_CO = 'remote_co'
    WE_WORK_REMOTELY = 'weworkremotely'

    def __str__(self):
        return self.value


def generate_scraper_filename(job_source):
    date_time = str(datetime.datetime.now())
    return f'scraper/job_data/{job_source} - {date_time}.xlsx'


def configure_webdriver(open_browser=False, block_media=False, block_elements=['css', 'img', 'js']):
    options = webdriver.ChromeOptions()

    # Install the extension
    extension_path = 'scraper/utils/pia.crx'

    if not open_browser:
        options.add_argument("--headless=new")
    if block_media:
        hide_elements = {
            'plugins': 2, 'popups': 2, 'geolocation': 2, 'notifications': 2,
            'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2, 'mixed_script': 2,
            'media_stream': 2, 'media_stream_mic': 2, 'media_stream_camera': 2,
            'protocol_handlers': 2, 'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2
        }
        if 'cookies' in block_elements:
            hide_elements.update({'cookies': 2})
        if 'js' in block_elements:
            hide_elements.update({'javascript': 2})
        if 'img' in block_elements:
            hide_elements.update({'images': 2})
        prefs = {'profile.default_content_setting_values': hide_elements}
        options.add_argument('--disable-features=EnableNetworkService')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_experimental_option('prefs', prefs)
    options.add_argument("window-size=1200,1100")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")

    options.add_extension(extension_path)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    if block_media:
        # Enable Chrome DevTools Protocol
        driver.execute_cdp_cmd("Page.enable", {})
        driver.execute_cdp_cmd("Network.enable", {})

        # Set blocked URL patterns to disable images and stylesheets
        blocked_patterns = []
        if 'img' in block_elements:
            blocked_patterns.extend(["*.jpg", "*.jpeg", "*.png", "*.gif", ])
        if 'css' in block_elements:
            blocked_patterns.extend(["*.css"])
        if 'js' in block_elements:
            blocked_patterns.extend(["*.js"])
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": blocked_patterns})
    return driver

def configure_undetected_chrome_driver(open_browser=False):
    options = uc.ChromeOptions()
    extension_path = 'scraper/utils/extensions/pia-unpacked'
    if not open_browser:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox --no-first-run --no-service-autorun --password-store=basic")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
    options.add_experimental_option('prefs', {"extensions.ui.developer_mode": True, })
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument(f'--load-extension={extension_path}')
    driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options, use_subprocess=False)
    return driver


def run_pia_proxy(driver, location=None, undetected=False):
    pia_instances = Accounts.objects.filter(source='pia')
    for pia_instance in pia_instances:
        try:
            driver.get(get_pia_web_url(undetected))
            driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')[
                0].send_keys(pia_instance.email)
            driver.find_elements(By.CSS_SELECTOR, 'input[type="password"]')[
                0].send_keys(pia_instance.password)
            driver.find_element(By.CLASS_NAME, 'btn').click()
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-success')))
            driver.find_element(By.CLASS_NAME, 'btn-success').click()
            driver.find_element(By.CLASS_NAME, 'btn-skip').click()
            error_status = change_pia_location(driver=driver, location=location, extension_opened=True)
            if not error_status:
                break
        except Exception as e:
            print(str(e))

def get_pia_web_url(undetected=False):
    pia_extension_id = PIA_UNPACKED_EXTENSION_ID if undetected else PIA_CRX_EXTENSION_ID
    pia_web_url = f"chrome-extension://{pia_extension_id}/html/foreground.html"
    return pia_web_url

def change_pia_location(driver, location=None, extension_opened=False, undetected=False) -> bool:
    error_status = False
    try:
        if not extension_opened:
            driver.get(get_pia_web_url(undetected))
        driver.find_element(By.CLASS_NAME, 'region-content').click()
        # if no location found then select US Miami
        if location:
            driver.find_element(By.CLASS_NAME, 'region-search-input').send_keys(location)
            driver.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "ul").click()
        else:
            driver.find_element(By.CLASS_NAME, 'region-search-input').send_keys("US ")
            us_locations = [location_btn for location_btn in driver.find_elements(By.CLASS_NAME, "region-list-item")[1:]]
            if us_locations:
                random_location = random.randrange(len(us_locations))
                us_locations[random_location].click()
            else:
                driver.find_element(By.CLASS_NAME, 'region-search-input').send_keys("US Miami")
                driver.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "ul").click()
        time.sleep(5)
    except Exception as e:
        error_status = True
        print(str(e))
    return error_status

def is_cloudflare_captcha_exist(driver):
    try:
        text = driver.find_element(By.ID, 'challenge-running').text.lower()
        return text == 'checking if the site connection is secure'
    except Exception as e:
        return False


def remove_emojis(text):
    pattern =  r'[\w\s.,!?\'"“”‘’#$%^&*()_+=\-{}\[\]:;<>\|\\/~`]+'
    extracted_text = re.findall(pattern, text)
    return ' '.join(extracted_text)

def k_conversion(text):
    return text.replace("k", ",000").replace( "K", ",000")

def set_job_type(job_type, sub_type="remote"):
    # if 'full time' in job_type.lower():
    #     return JOB_TYPE[0] if 'remote' in job_type.lower() else JOB_TYPE[1] if 'site' in job_type.lower() else JOB_TYPE[2] if 'hybrid' in job_type.lower() else JOB_TYPE[1]
    # elif 'hybrid' in job_type.lower():
    #     return JOB_TYPE[2] if 'full time' in job_type.lower() else JOB_TYPE[3] if 'contract' in job_type.lower() else JOB_TYPE[2]
    # elif 'contract' in job_type.lower():
    #     return JOB_TYPE[4] if 'onsite' in job_type.lower() else JOB_TYPE[4] if 'site' in job_type.lower() else JOB_TYPE[5] if 'remote' in job_type.lower() else JOB_TYPE[4]
    # else:
    #   return job_type.capitalize()

    if 'full time' in job_type.lower() and sub_type == 'remote':
        return JOB_TYPE[0]
    elif 'full time' in job_type.lower() and sub_type == 'onsite':
        return JOB_TYPE[1]
    elif 'full time' in job_type.lower() and sub_type == 'hybrid':
        return JOB_TYPE[2]
    elif 'contract' in job_type.lower() and sub_type == 'remote':
        return JOB_TYPE[5]
    elif 'contract' in job_type.lower() and sub_type == 'onsite':
        return JOB_TYPE[4]
    elif 'contract' in job_type.lower() and sub_type == 'hybrid':
        return JOB_TYPE[3]
    else:
      return job_type.capitalize()

def make_plural(word: str = '', num: int = 1):
    return word + 's' if word and word.strip() and (num > 1 or num == 0) else word



def previous_jobs(source, urls=[]):
    jobs = JobDetail.objects.filter(job_source=source) 
    if len(urls) > 0:
        jobs = jobs.filter(job_source_url__in=urls)
    previous_jobs = set(jobs.values_list('job_source_url', flat=True))
    return {job: True for job in previous_jobs}



def sleeper(sec=0):
    seconds = sec if sec else random.randint(1, 5)
    time.sleep(seconds)
    
    
def previous_company_wise_titles(data: list = []):
    """
    Get the existing job TITLE-COMPANY (derived field)

    Args:
        data (list): list of combined job titles & company name

    Returns:
        dict: {title-company: True/False}
    """
    titles = JobDetail.objects.annotate(
        tc=fn.Concat('job_title', Value('-'), 'company_name',
                     output_field=CharField())
    ).filter(tc__in=data).values_list('tc', flat=True)
    return {title: True for title in titles}

def export_to_excel(data, scraper_name, job_source):
    if not data or not scraper_name or not job_source:
        return
    df = pd.DataFrame(data=data, columns=COLUMN_NAME)
    filename = generate_scraper_filename(scraper_name)
    df.to_excel(filename, index=False)
    ScraperLogs.objects.create(
        total_jobs=len(df), 
        job_source=job_source, 
        filename=filename
    )

# pia extension ids
PIA_CRX_EXTENSION_ID = 'jplnlifepflhkbkgonidnobkakhmpnmh'
PIA_UNPACKED_EXTENSION_ID = 'olfblhmobjbfckldmpdgehfecmjapkob'
