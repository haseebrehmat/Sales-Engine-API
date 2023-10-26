import datetime
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from scraper.constants.const import JOB_TYPE

from scraper.models import GroupScraper, GroupScraperQuery
from selenium.webdriver.support import expected_conditions as EC
import random


from utils.helpers import saveLogs
from scraper.models.accounts import Accounts



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
    RUBY_ON_REMOTE = 'ruby_on_remote'
    HUBSTAFF_TALENT = 'hubstaff_talent'
    JUST_REMOTE = 'just_remote'
    REMOTE_CO = 'remote_co'
    WE_WORK_REMOTELY = 'weworkremotely'

    def __str__(self):
        return self.value


def generate_scraper_filename(job_source):
    date_time = str(datetime.datetime.now())
    return f'scraper/job_data/{job_source} - {date_time}.xlsx'



def configure_webdriver(open_browser=False, stop_loading_images_and_css=False):
    options = webdriver.ChromeOptions()

    # Install the extension
    extension_path = 'scraper/utils/pia.crx'

    if not open_browser:
        options.add_argument("--headless=new")

    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2,
                                                        'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                        'notifications': 2, 'auto_select_certificate': 2,
                                                        'fullscreen': 2,
                                                        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                        'media_stream_mic': 2, 'media_stream_camera': 2,
                                                        'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2,
                                                        'site_engagement': 2,
                                                        'durable_storage': 2}}

    if stop_loading_images_and_css:
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

    if stop_loading_images_and_css:
        # Enable Chrome DevTools Protocol
        driver.execute_cdp_cmd("Page.enable", {})
        driver.execute_cdp_cmd("Network.enable", {})

        # Set blocked URL patterns to disable images and stylesheets
        blocked_patterns = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.css", "*.js"]
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": blocked_patterns})
    return driver


def run_pia_proxy(driver, location=None):
    pia_instances = Accounts.objects.filter(source='pia')
    for pia_instance in pia_instances:
        try:
            driver.get("chrome-extension://jplnlifepflhkbkgonidnobkakhmpnmh/html/foreground.html")
            driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')[
                0].send_keys(pia_instance.email)
            driver.find_elements(By.CSS_SELECTOR, 'input[type="password"]')[
                0].send_keys(pia_instance.password)
            driver.find_element(By.CLASS_NAME, 'btn').click()
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-success')))
            driver.find_element(By.CLASS_NAME, 'btn-success').click()
            driver.find_element(By.CLASS_NAME, 'btn-skip').click()
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
            break
        except Exception as e:
            print(str(e))

def remove_emojis(text):
    pattern =  r'[\w\s.,!?\'"“”‘’#$%^&*()_+=\-{}\[\]:;<>\|\\/~`]+'
    extracted_text = re.findall(pattern, text)
    return ' '.join(extracted_text)

def k_conversion(text):
    return text.replace("k", ",000").replace( "K", ",000")

def set_job_type(job_type):
    # if 'full time' in job_type.lower():
    #     return JOB_TYPE[0] if 'remote' in job_type.lower() else JOB_TYPE[1] if 'site' in job_type.lower() else JOB_TYPE[2] if 'hybrid' in job_type.lower() else JOB_TYPE[1]
    # elif 'hybrid' in job_type.lower():
    #     return JOB_TYPE[2] if 'full time' in job_type.lower() else JOB_TYPE[3] if 'contract' in job_type.lower() else JOB_TYPE[2]
    # elif 'contract' in job_type.lower():
    #     return JOB_TYPE[4] if 'onsite' in job_type.lower() else JOB_TYPE[4] if 'site' in job_type.lower() else JOB_TYPE[5] if 'remote' in job_type.lower() else JOB_TYPE[4]
    # else:
    #   return job_type.capitalize()

    if 'full time' in job_type.lower():
        return JOB_TYPE[0]
    elif 'contract' in job_type.lower():
        return JOB_TYPE[1]
    else:
      return job_type.capitalize()
