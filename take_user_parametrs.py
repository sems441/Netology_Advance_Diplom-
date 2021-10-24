import requests
from keys import users_key
import time


def user_info(user):
    url = f"https://api.vk.com/method/users.get?user_id={user}&v=5.131&fields=sex,bdate,home_town, city"
    token = f"access_token={users_key[user]}"
    request = requests.get(url, token)
    sex = request.json()["response"][0].get("sex")
    if sex == 1:
        sex = 2
    else:
        sex = 1
    # sex = None
    age = request.json()["response"][0].get("bdate")
    current_data = time.strftime("%Y")
    age = int(current_data)-int(age[-4:])
    # age = None
    # city = request.json()["response"][0].get("home_town")
    city = None
    return sex, age, city


if __name__ == '__main__':
    user_info("")
