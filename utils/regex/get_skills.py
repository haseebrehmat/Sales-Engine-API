import re

from utils.regex.devops import devops_skill_regex, devops_regex


def get_skills(description, regex_arr):
    skills = []
    for regex in regex_arr:
        pattern = re.compile(regex['exp'])
        if pattern.search(description):
            skills.append(regex['tech_stack'])
    return skills


def get_devops_skills(description):
    description = description.lower()
    skills = list(set(re.findall(devops_skill_regex, description, re.IGNORECASE)))
    return skills


description = """Qualifications
Ruby on Rails (Required)

AWS (Required)

Terraform (IAAC) (Required)

CI/CD (Required)

Full Job Description
Below is the Job description:

Title: Sr. Software Engineer (Ruby on Rails)

Type: Contract

Must have backend experience and experience with AWS

Job Responsibilities:

· We are looking for a problem solver with a strong technical background (Ruby on Rails, SQL, AWS), skilled in agile development with solid understanding of the full software development life-cycle and DevOps, who will work in highly productive and collaborative scrum teams and partner with product and business stakeholders to deliver and operate secure, high-performance, and scalable software solutions

· Design and maintain complex and scalable applications using Ruby on Rails, Vue.js, and SQL

· Improve scalability, service reliability, capacity, and performance of software

· Collaborate with product managers, designers, architects, and QA to build high quality, functional and impactful products

· Participate in the full lifecycle of the software development lifecycle from ideation to delivery and production support

· Evaluate our monitoring and alerting strategies

· Committing code using Git best practices and adhering to project workflows

· Shipping code on a regular basis and deploying applications to AWS cloud services

· Applying security best practices in all technical decisions

· Daily activities include development, application maintenance, monitoring alerts, and investigating escalations

Qualifications:

· 5+ years of software development experience in Ruby on Rails

· Design and maintain complex and scalable applications using Ruby on Rails, Vue.js, and SQL

· Experience working with E Commerce and Shopify

· Experience and understanding of monoliths and microservices architectures

· Experience building scalable Ruby on Rails applications

· Experience with GraphQL

· Experience with Terraform (IAAC)

· Experience with CICD pipelines and automation testing strategies"""

get_devops_skills(description)
