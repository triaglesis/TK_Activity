# coding=utf-8
__author__ = 'danilcha'

import vk

token = '43accf2d6642a5d3a0202c6801a9530cc0c0784533d7e4d04e55984c129fbcf789724f8a1ff3da5d409dc'
vkapi = vk.API(access_token=token)

wall_message_text= "Денежные призы и призы от ТК в этом месяце получают самые активные комментаторы паблика @typical_kirovohrad.\n" \
                   "Для победителей просьба связаться с администрацией.\n" \
                   "Не в курсе, что ТК платит?\n" \
                   "ТК запустил систему ежемесячного денежного и призового поощрения подписчиков.\n" \
                   "Подробности: https://vk.com/typical_kirovohrad?w=page-46631810_49912854\n" \
                   "Комментируешь ТК? Получи за это приз!\n" \
                   "#ВождьБот Powered by #Python made by #trianglesis"

# Working groups
typical_kirovohrad = "-46631810"
typical_kirovohrad_boss = "13147598"

# Post the composed message to the wall:
wall_post = vkapi('wall.post',
                  owner_id=typical_kirovohrad,
                  from_group='1',
                  message=wall_message_text,
                  attachments='photo-46631810_395391493,'
                              'audio13147598_164266010,'
                              'audio14448310_120581531,'
                              'audio-92678264_361990216,'
                              'page-46631810_49912969,',
                  signed='0')
print("Message has been posted successfully!")