# modules/utils.py

HERO_MALE = ["IronMan", "Batman", "Spiderman", "Hulk", "Thor", "Wolverine", "DrStrange"]
HERO_FEMALE = ["WonderWoman", "CaptainMarvel", "BlackWidow", "ScarletWitch", "Storm", "Gamora", "JeanGrey"]


import random

def get_avatar_url(name, gender):
    if gender == "M":
        seed = random.choice(HERO_MALE) + name.replace(" ", "")
        style = "croodles-neutral"  # or 'pixel-art'
    elif gender == "F":
        seed = random.choice(HERO_FEMALE) + name.replace(" ", "")
        style = "adventurer"  # or 'big-ears'
    else:
        seed = "Hero" + name.replace(" ", "")
        style = "bottts"

    return f"https://api.dicebear.com/7.x/{style}/svg?seed={seed}"
