from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import keys

vk = vk_api.VkApi(token=keys.group_token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


mens_prefix = ("м", "М", "муж", "Муж", "МУЖ")
women_prefix = ("ж", "Ж", "Жен", "ЖЕН", "жен")


def add_data(user_id, message):
    info_msg = False
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if not info_msg:
                write_msg(user_id, message)
                info_msg = True
            msg = event.text
            if event.to_me and msg.startswith(mens_prefix):
                return 2
            elif event.to_me and msg.startswith(women_prefix):
                return 1
            elif event.to_me and msg.isdigit():
                return msg
            elif event.to_me and msg.isalpha():
                return msg


if __name__ == '__main__':
    add_data("", "")
