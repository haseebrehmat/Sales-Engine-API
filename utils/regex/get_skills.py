import re
from utils.helpers import saveLogs
from utils.regex.devops import devops_skill_regex, devops_regex


def get_skills(description, regex_arr, tech):
    try:
        pattern = r"[^\w\s\\+#/]"
        skills = []
        for regex in regex_arr:
            #print(regex['tech_stack'])
            pattern = re.compile(regex['exp'])
            if pattern.search(description):
                skills.append(regex['tech_stack'])
        description = re.sub(pattern, "", description.replace(" ", ""))
        for x in tech:
            if x in description:
                skills.append(x)
        return list(set(skills))
    except Exception as e:
        print("Error in getting skills", str(e))
        saveLogs(e)
        return False
