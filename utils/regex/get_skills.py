import re


def get_skills(description, regex_arr):
    skills = []
    for regex in regex_arr:
        pattern = re.compile(regex['exp'])
        if pattern.search(description):
            skills.append(regex['tech_stack'])
    return skills
