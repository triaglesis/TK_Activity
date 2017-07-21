# coding=utf-8
__author__ = 'danilcha'

import vk

token = 'TOKEN'
vkapi = vk.API(access_token=token)

wall_message_text= "Денежные призы и призы от ТК в этом месяце получают самые активные авторы постов паблика @typical_kirovohrad \n\n" \
                   "Для победителей просьба связаться с администрацией.\n\n" \
                   "Не в курсе, что ТК платит?\n" \
                   "ТК запустил систему ежемесячного денежного и призового поощрения подписчиков.\n" \
                   "Подробности: https://vk.com/typical_kirovohrad?w=page-46631810_49912854\n" \
                   "Предлагаешь интересные посты в ТК? Получай за это призы!\n\n" \
                   "#ТКПлатит #ТипичныйКировоград #Кировоград #Ингульск #TypicalKirovohrad\n" \
                   "#ВождьБот Powered by #Python made by #trianglesis"

# Working groups
typical_kirovohrad = "-46631810"
typical_kirovohrad_boss = "13147598"

# Post the composed message to the wall:
wall_post = vkapi('wall.post',
                  owner_id=typical_kirovohrad,
                  from_group='1',
                  message=wall_message_text,
                  attachments='photo-46631810_395391488,'
                              'audio13147598_164266010,'
                              'audio14448310_120581531,'
                              'audio-92678264_361990216,'
                              'page-46631810_49912971,',
                  signed='0')
print("Message has been posted successfully!")