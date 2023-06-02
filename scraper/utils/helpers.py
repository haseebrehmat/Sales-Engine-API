from scraper.models import GroupScraper, GroupScraperQuery
import datetime

def convert_time_into_minutes(interval, interval_type):
    if interval_type.lower() == 'minutes':
        pass
    elif interval_type.lower() == 'hours':
        interval = interval * 60
    elif interval_type.lower() == 'days':
        interval = interval * 60 * 24

    return interval



def is_valid_group_scraper_time(time, week_days):
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
            queries_count = len(group_scraper_query.queries)
            estimated_time = queries_count * estimated_query_time
            scraper_start_time = datetime.datetime.strptime(str(x.scheduler_settings.time), "%H:%M:%S")
            estimated_scraper_end_time = scraper_start_time + datetime.timedelta(minutes=estimated_time)
            estimated_scraper_end_time = estimated_scraper_end_time.strftime("%H:%M:%S")

            if str(scraper_start_time) <= str(time) >= str(estimated_scraper_end_time):
                return False
    return True