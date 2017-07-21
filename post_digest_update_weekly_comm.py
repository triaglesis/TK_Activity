# coding=utf-8
__author__ = 'danilcha'

import vk

token = '43accf2d6642a5d3a0202c6801a9530cc0c0784533d7e4d04e55984c129fbcf789724f8a1ff3da5d409dc'
vkapi = vk.API(access_token=token)

wall_message_text= "ТК представляет рейтинг самых активных комментаторов за неделю! \n" \
                   "Каждый комментатор из списка является претендентом на денежный приз или приз от ТК. \n" \
                   "Список победителей будет сформирован за месяц.\n " \
                   "Любишь комментировать? Получай за это призы! \n" \
                   "Подробности: https://vk.com/typical_kirovohrad?w=page-46631810_49912854\n" \
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
                              'page-46631810_49912978,',
                  signed='0')
print("Message has been posted successfully!")