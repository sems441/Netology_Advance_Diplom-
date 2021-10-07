import requests
import sqlalchemy
from main import token

url = "https://api.vk.com/method/users.get?user_id=663114110&v=5.131&fields=sex,home_town,bdate,relation"
full_token = "access_token=" + token
request = requests.get(url, full_token)
print(request.text)
name = request.json()["response"][0]["first_name"]
last_name = request.json()["response"][0]["last_name"]
ids = request.json()["response"][0]["id"]
sex = request.json()["response"][0]["sex"]
bdate = request.json()["response"][0]["bdate"]
home_town = request.json()["response"][0]["home_town"]
relation = request.json()["response"][0]["relation"]
print(name)

engine = sqlalchemy.create_engine("postgresql://semadmin:1234567@localhost:5432/netology")
connection = engine.connect()

qwe = connection.execute("""SELECT name FROM album;""").fetchmany(5)
print(qwe)
connection.execute(f"""INSERT INTO vk_people VALUES (1, {ids}, '{name}', '{last_name}', {sex}, '{bdate}',
                        '{home_town}', {relation});""")
