from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import keys
import find_pair_search

vk = vk_api.VkApi(token=keys.group_token)
longpoll = VkLongPoll(vk)

open_chats = []
welcome_prefix = ("прив", "Прив", "Добр", "добр", "Здра", "здра")
mens_prefix = ("м", "М", "муж", "Муж", "МУЖ")
women_prefix = ("ж", "Ж", "Жен", "ЖЕН", "жен")


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


def add_data(user_id, message):
    info_msg = False
    for question in longpoll.listen():
        if question.type == VkEventType.MESSAGE_NEW:
            if not info_msg:
                write_msg(user_id, message)
                info_msg = True
            msg = question.text
            if question.to_me and msg.startswith(mens_prefix):
                return 2
            elif question.to_me and msg.startswith(women_prefix):
                return 1
            elif question.to_me and msg.isdigit():
                return msg
            elif question.to_me and msg.isalpha():
                return msg


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            if event.user_id not in open_chats and request.startswith(welcome_prefix):
                write_msg(event.user_id, "Добрый день")
                open_chats.append(event.user_id)
            answer = find_pair_search.user_info(event.user_id)
            sex = answer[0]
            if sex is None:
                sex = add_data(event.user_id, "Введите пол поиска м/ж")
            age = answer[1]
            if age is None:
                age = add_data(event.user_id, "Укажите возраст")
            city = answer[2]
            if city is None:
                city = add_data(event.user_id, "Укажите город")
            find_pair_search.search_pair(sex, age, city)
            write_msg(event.user_id, "Данные успешно записаны в БД")
        elif event.text.lower() == "пока":
            write_msg(event.user_id, "До свидания")
            open_chats.pop(event.user_id)
        else:
            write_msg(event.user_id, "Не поняла вашего ответа...")
