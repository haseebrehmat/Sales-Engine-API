from scraper.jobs.adzuna_scraping import adzuna_scraping
from scraper.jobs.careerbuilder_scraping import career_builder
from scraper.jobs.careerjet_scraping import careerjet
from scraper.jobs.dice_scraping import dice
from scraper.jobs.glassdoor_scraping import glassdoor
from scraper.jobs.google_careers_scraping import google_careers
from scraper.jobs.indeed_scraping import indeed
from scraper.jobs.jooble_scraping import jooble
from scraper.jobs.linkedin_scraping import linkedin
from scraper.jobs.monster_scraping import monster
from scraper.jobs.simply_hired_scraping import simply_hired
from scraper.jobs.talent_scraping import talent
from scraper.jobs.ziprecruiter_scraping import ziprecruiter_scraping
from scraper.jobs.recruit_scraping import recruit
from scraper.jobs.dailyremote_scraping import dailyremote
from scraper.jobs.rubynow_scraping import rubynow

single_scrapers_functions = {'careerbuilder': career_builder, 'career_builder': career_builder, 'dice': dice,
                             'glassdoor': glassdoor, 'indeed': indeed, 'linkedin': linkedin, 'monster': monster,
                             'simplyhired': simply_hired, 'simply_hired': simply_hired, 'jooble': jooble,
                             'ziprecruiter': ziprecruiter_scraping, 'ziprecruiter_scraping': ziprecruiter_scraping,
                             'google_careers': google_careers, 'googlecareers': google_careers, 'talent': talent,
                             'adzuna': adzuna_scraping, 'careerjet': careerjet, 'career_jet': careerjet,
                             'recruit': recruit, 'dailyremote': dailyremote, 'rubynow': rubynow}
