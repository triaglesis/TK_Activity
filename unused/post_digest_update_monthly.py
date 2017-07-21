# coding=utf-8
__author__ = 'danilcha'

import vk
from time import strftime
import datetime

datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')

# TODO:
# New version for Vkontakte api for module ver 2.0a4 and above
token = 'TOKEN'
# session = vk.Session(access_token=token)
vkapi = vk.API(access_token=token)
# vkapi = vk.API(session)

curr_date = strftime("%d-%m-%Y")

wall_message_text= ""


# Working groups
typical_kirovohrad = "-46631810"
scandal_kirovohrad = "-80849532"
typical_kirovohrad_boss = "13147598"

# Post the composed message to the wall:
wall_post = vkapi('wall.post',
                  owner_id=typical_kirovohrad,
                  from_group='1',
                  message=wall_message_text,
                  attachments='photo-46631810_395141048,'
                              'audio13147598_164266010,'
                              'audio14448310_120581531,'
                              'audio-92678264_361990216,'
                              'page-46631810_49912854,',
                  signed='0')
print("Message has been posted successfully!")