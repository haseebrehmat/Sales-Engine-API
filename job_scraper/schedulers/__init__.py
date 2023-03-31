from job_scraper.schedulers.job_upload_scheduler import job_time_scheduler, job_interval_scheduler, linkedin_scheduler, \
    indeed_scheduler, dice_scheduler, career_builder_scheduler, glassdoor_scheduler, monster_scheduler

job_interval_scheduler.start()
job_time_scheduler.start()
linkedin_scheduler.start()
indeed_scheduler.start()
dice_scheduler.start()
career_builder_scheduler.start()
glassdoor_scheduler.start()
monster_scheduler.start()


