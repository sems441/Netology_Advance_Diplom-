import requests
import sqlalchemy
from keys import users_key, sql_pass, sql_login


def search_pair(sex, age, city, user):
    engine = sqlalchemy.create_engine(f"postgresql://{sql_login}:{sql_pass}@localhost:5432/netology")
    connection = engine.connect()
    url = f"https://api.vk.com/method/users.search?sort=0&v=5.131&fields=sex,bdate,home_town,relation&" \
          f"count=1000&hometown={city}&sex={sex}&status=6&age_from={age}&age_to={age}"
    full_token = "access_token=" + users_key[user]
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
        connection.execute(f"""INSERT INTO vk_people VALUES ({number}, {ids}, '{name}', '{last_name}', {search_sex},
                               '{birth_date}','{home_town}', '{relation}');""")


if __name__ == '__main__':
    search_pair("", "", "", "")
