#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'
# Change history

import vk
from time import strftime
import datetime
import MySQLdb
import math

db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity" )
cursor = db.cursor()

# TODO:
# New version for Vkontakte api for module ver 2.0a4 and above
token = 'TOKEN'
# session = vk.Session(access_token=token)
vkapi = vk.API(access_token=token)
# vkapi = vk.API(session)

# Get today date and date for last month - convert to strings
today = datetime.date.today()
last_date = today - datetime.timedelta(days=7)
today = str(today)
last_date = str(last_date)

select_comments = """SELECT comment_user_id, COUNT(*), SUM(comment_likes)
                    FROM PUB_COMMENTS WHERE comment_date between %r and %r
                    GROUP BY comment_user_id"""%(last_date,today)

print("'Select all activity from COMMENTS table between '"+today+" and "+last_date)
comments_results = ''
try:
    cursor.execute(select_comments)
    comments_results = cursor.fetchall()
except:
    print("Error: unable to fecth data")

print("Make dicts with results")
all_dicts_list = []
if comments_results:                                    # if table give comment tuples: (('-80849532', 14, 7.0), ('100072457', 1, 0.0))
    for item in comments_results:                       # For each item in tuple of tuples: ('-80849532', 14, 7.0)
        user_id = item[0]                               # item[0] = '-80849532'
        user_id = user_id.replace('-', 'public')        # replace "-" for public id with "public"
        comm_count = int(item[1])                       # item[1] = 14
        likes_count = int(item[2])                           # item[2] = 7.0
        if likes_count > 0:
            comm_int = (comm_count * 0.07)                  # make comments count int for sure and mult by 0.07
            likes_int = (likes_count / 2)                   # make likes count int and mult by 0.2
            likes_q = (likes_count/comm_count)              # user rating is sum of comments int and likes int)
            user_rating = (((comm_int+likes_int)*(likes_q/likes_count))*10)
            user_rating = round(user_rating, 3)
            if user_rating and comm_count > 1:
                user_comments_dict = {'user_id':user_id,                         # -80849532
                                     'user_comments':comm_count,                # comments points = comments quantity * 0.5 = 8.5
                                     'user_likes':likes_count,               # 0
                                     'user_rating':user_rating}                 # 8.4
                all_dicts_list.append(user_comments_dict)
            else:
                pass
        else:
            pass
else:
    print("No comments_results")

print("Sort all data by rating DESC order")
sorted_all_counters = sorted(all_dicts_list, key=lambda k: k['user_rating'], reverse=True)
# print(sorted_all_counters)

# Wiki page tags:
wiki_table_start = "{| \n|- \n! Пользователь: \n! Комменты \n! Лайки \n! Рейтинг "
wiki_table_id = "\n|- \n|"
wiki_table_cell = "| "
wiki_table_end = "\n|}"

print("Compose wiki tables")
wiki_users = []
for user in sorted_all_counters:
    if "public" not in user['user_id']:
        wiki_user_id_string = wiki_table_id+"[[id"+user['user_id']+"]] \n"
    else:
        wiki_user_id_string = wiki_table_id+"[["+user['user_id']+"]] \n"
    wiki_user_comments = wiki_table_cell+str(user['user_comments']) + "\n"
    wiki_user_likes = wiki_table_cell+str(user['user_likes']) + "\n"
    wiki_user_rating = wiki_table_cell+str(user['user_rating']) + " "
    wiki_user_str = wiki_user_id_string+wiki_user_comments+wiki_user_likes+wiki_user_rating
    wiki_users.append(wiki_user_str)

wiki_those_ids = ', '.join(wiki_users)
wiki_those_ids = wiki_those_ids.replace(',', '')
wiki_table = wiki_table_start+wiki_those_ids+wiki_table_end

print("Compose wiki markups")
wiki_msg = "[[photo-46631810_395391493|600px;noborder| ]] \n" \
           "=== Таблица комментаторов за неделю ===\n" \
           "от: "+last_date+" по: "+today+\
           "\n\n"
wiki_footer = "\n\n" \
              "== Правила и условия: == \n" \
              "*[[page-46631810_49912854|Для ленивых!]]\n"\
              "*[[page-46631810_49897830|Условия акции ТК платит!]]\n"\
              "*[[page-46631810_49898043|Меню статистики и советы администрации]]\n\n"\
              "== TOP за неделю: ==\n"\
              "*[[page-46631810_49912978|TOP комментаторы неделя]]\n"\
              "*[[page-46631810_49912979|TOP авторы неделя]]\n\n"\
              "== TOP за месяц: ==\n"\
              "*[[page-46631810_49912969|TOP комментаторы месяц]]\n"\
              "*[[page-46631810_49912971|TOP авторы месяц]]\n\n" \
              "== Общая статистика == \n" \
              "*[[page-46631810_49898046|Таблица рейтинга общая неделя]]\n"\
              "*[[page-46631810_49898050|Таблица рейтинга общая месяц]]\n"\
              "\n\n" \
              "\n\n #ВождьБот Powered by Python made by #trianglesis"
composed_message = wiki_msg+wiki_table+wiki_footer

# Post composed message to the wiki-page
user = '13147598'
# https://vk.com/scandal_kir
group = '46631810'
# Таблица рейтинга подробная комментаторы (неделя)
# https://vk.com/page-46631810_49912978
page = '49912978'

print("Post data to wiki page https://vk.com/page-46631810_49912978")
wiki_page = vkapi.pages.save(text=composed_message,
                             page_id=page,
                             group_id=group,
                             user_id=user,
                             title='')