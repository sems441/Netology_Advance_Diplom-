import requests
import time
from keys import user_token
import load_to_database


def search_pair(sex, age, city):
    url = f"https://api.vk.com/method/users.search?sort=0&v=5.131&fields=sex,bdate,home_town,relation&" \
          f"count=1000&hometown={city}&sex={sex}&status=6&age_from={age}&age_to={age}"
    full_token = "access_token=" + user_token
    request = requests.get(url, full_token)
    print(request.json())
    count = len(request.json()["response"]["items"])
    for number in range(count):
        name = request.json()["response"]["items"][number]["first_name"]
        last_name = request.json()["response"]["items"][number]["last_name"]
        ids = request.json()["response"]["items"][number]["id"]
        search_sex = request.json()["response"]["items"][number]["sex"]
        birth_date = request.json()["response"]["items"][number].get("bdate")
        home_town = request.json()["response"]["items"][number].get("home_town")
        relation = request.json()["response"]["items"][number].get("relation")
        load_to_database.load_data(ids, name, last_name, search_sex, birth_date, home_town, relation)


def user_info(user):
    url = f"https://api.vk.com/method/users.get?user_id={user}&v=5.131&fields=sex,bdate,home_town, city"
    token = f"access_token={user_token}"
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
    city = request.json()["response"][0].get("home_town")
    # city = None
    return sex, age, city


if __name__ == '__main__':
    search_pair("", "", "")
