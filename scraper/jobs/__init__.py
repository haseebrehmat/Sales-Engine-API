from scraper.jobs.adzuna_scraping import adzuna_scraping
from scraper.jobs.arc_dev_scraping import arc_dev
from scraper.jobs.careerbuilder_scraping import career_builder
from scraper.jobs.careerjet_scraping import careerjet
from scraper.jobs.dice_scraping import dice
from scraper.jobs.glassdoor_scraping import glassdoor
from scraper.jobs.google_careers_scraping import google_careers
from scraper.jobs.indeed_scraping import indeed
from scraper.jobs.job_gether_scraping import job_gether
from scraper.jobs.jooble_scraping import jooble
from scraper.jobs.hirenovice_scraping import hirenovice
from scraper.jobs.linkedin_scraping import linkedin
from scraper.jobs.monster_scraping import monster
from scraper.jobs.receptix_scraping import receptix
from scraper.jobs.simply_hired_scraping import simply_hired
from scraper.jobs.talent_scraping import talent
from scraper.jobs.working_nomads_scraping import working_nomads
from scraper.jobs.ziprecruiter_scraping import ziprecruiter_scraping
from scraper.jobs.recruit_scraping import recruit
from scraper.jobs.dailyremote_scraping import dailyremote
from scraper.jobs.rubynow_scraping import rubynow
from scraper.jobs.workopolis_scraping import workopolis
from scraper.jobs.himalayas_scraping import himalayas
from scraper.jobs.dynamite_scraping import dynamite
from scraper.jobs.startwire_scraping import startwire
from scraper.jobs.remote_ok_scraping import remoteok
from scraper.jobs.the_muse_scraping import the_muse
from scraper.jobs.hubstaff_talent_scraping import hubstaff_talent
from scraper.jobs.just_remote_scraping import just_remote
from scraper.jobs.remote_co_scraping import remote_co
from scraper.jobs.builtin_scraping import builtin
from scraper.jobs.start_up_scraping import startup
from scraper.jobs.getwork_scraping import getwork
from scraper.jobs.ruby_on_remote_scraping import ruby_on_remote
from scraper.jobs.smartrecruiter_scraping import smartrecruiter
from scraper.jobs.clearance_scraping import clearance
from scraper.jobs.us_jora_scraping import us_jora
from scraper.jobs.workable_scraping import workable
from scraper.jobs.ycombinator_scraping import ycombinator
from scraper.jobs.ziprecruiter_scraping import ziprecruiter_scraping
from scraper.jobs.wwr_scraping import weworkremotely

single_scrapers_functions = {'careerbuilder': career_builder, 'career_builder': career_builder, 'dice': dice,
                             'glassdoor': glassdoor, 'indeed': indeed, 'linkedin': linkedin, 'monster': monster,
                             'simplyhired': simply_hired, 'simply_hired': simply_hired, 'jooble': jooble,
                             'ziprecruiter': ziprecruiter_scraping, 'ziprecruiter_scraping': ziprecruiter_scraping,
                             'google_careers': google_careers, 'googlecareers': google_careers, 'talent': talent, 'google': google_careers,
                             'adzuna': adzuna_scraping, 'careerjet': careerjet, 'career_jet': careerjet,
                             'recruit': recruit, 'dailyremote': dailyremote, 'rubynow': rubynow,
                             'workingnomads': working_nomads, 'working_nomads': working_nomads, 'workopolis': workopolis,
                             'dynamite': dynamite, "arcdev": arc_dev, "arc_dev": arc_dev,
                             'himalayas': himalayas, 'startwire': startwire, "jobgether": job_gether,
                             "remote_ok": remoteok,  "the_muse": the_muse, 'receptix': receptix, 'hirenovice': hirenovice,
                             'himalayas': himalayas, 'startwire': startwire, "jobgether": job_gether, "remoteok": remoteok,
                             "hubstaff_talent": hubstaff_talent, "just_remote": just_remote, 'remote_co': remote_co, 'remoteco': remote_co, 'built_in': builtin, 'builtin': builtin,
                             'startup': startup, 'getwork': getwork, 'get_work': getwork, 'ruby_on_remote': ruby_on_remote, 'rubyonremote': ruby_on_remote, 'smartrecruiter': smartrecruiter,
                             'smart_recruiter': smartrecruiter, 'clearance': clearance, 'usjora': us_jora, 'us_jora': us_jora, 'workable': workable,
                             'ycombinator': ycombinator, 'y_combinator': ycombinator, 'ziprecruiter_scraping': ziprecruiter_scraping, 'ziprecruiter': ziprecruiter_scraping,
                             'weworkremotely': weworkremotely, 'we_work_remotely': weworkremotely}
