from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import keys
import take_user_parametrs
import find_pair_search
import missing_data

vk = vk_api.VkApi(token=keys.group_token)
longpoll = VkLongPoll(vk)

open_chats = [663114110]


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me and event.user_id not in open_chats:
            write_msg(event.user_id, "Добрый день, введите токен")
            open_chats.append(event.user_id)

        if event.to_me and event.user_id in open_chats and len(event.text) == 85:
            print(event.text)
            keys.users_key[event.user_id] = event.text
            answer = take_user_parametrs.user_info(event.user_id)
            sex = answer[0]
            if sex is None:
                sex = missing_data.add_data(event.user_id, "Введите пол поиска м/ж")
            age = answer[1]
            if age is None:
                age = missing_data.add_data(event.user_id, "Укажите возраст")
            city = answer[2]
            if city is None:
                city = missing_data.add_data(event.user_id, "Укажите город")

            find_pair_search.search_pair(sex, age, city, event.user_id)
            write_msg(event.user_id, "Данные успешно записаны в БД")

        elif event.text.lower() == "пока":
            write_msg(event.user_id, "До свидания")
            open_chats.pop(event.user_id)
            # else:
            #     write_msg(event.user_id, "Не поняла вашего ответа...")
