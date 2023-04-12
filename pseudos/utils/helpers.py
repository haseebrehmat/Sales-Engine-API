

def validate_skill_data(data):
    valid_skill_keys = ["name", 'level']
    data = [i if valid_keys == list(i.keys()) else False for i in data]
    if False not in data:
        if "level" in valid_keys:
            check = [5 <= x["level"] >= 1 for x in data]
            return data if False not in check else False
        return data
    return False


print(validate_skill_data(skills))
