from scraper.jobs.careerbuilder_scraping import career_builder
from scraper.jobs.dice_scraping import dice
from scraper.jobs.glassdoor_scraping import glassdoor
from scraper.jobs.indeed_scraping import indeed
from scraper.jobs.jooble_scraping import jooble
from scraper.jobs.linkedin_scraping import linkedin
from scraper.jobs.monster_scraping import monster
from scraper.jobs.simply_hired_scraping import simply_hired

single_scrapers_functions = {'careerbuilder': career_builder, 'career_builder': career_builder, 'dice': dice,
                             'glassdoor': glassdoor, 'indeed': indeed, 'linkedin': linkedin, 'monster': monster,
                             'simplyhired': simply_hired, 'simply_hired': simply_hired, 'jooble': jooble}
