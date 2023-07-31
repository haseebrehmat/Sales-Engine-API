import datetime

from scraper.models import GroupScraper, GroupScraperQuery


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
    DICE = 'dice'
    GOOGLE_CAREERS = 'google_careers'
    JOOBLE = 'jooble'
    DAILY_REMOTE = 'dailyremote'
    MONSTER = 'monster'
    SIMPLY_HIRED = 'simply_hired'
    TALENT = 'talent'
    ZIP_RECRUITER = 'ziprecruiter'
    RECRUIT = 'recruit'
    Ruby_Now = 'rubynow'



    def __str__(self):
        return self.value


def generate_scraper_filename(job_source):
    date_time = str(datetime.datetime.now())
    return f'scraper/job_data/{job_source} - {date_time}.xlsx'
