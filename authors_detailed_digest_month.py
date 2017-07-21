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
token = '43accf2d6642a5d3a0202c6801a9530cc0c0784533d7e4d04e55984c129fbcf789724f8a1ff3da5d409dc'
# session = vk.Session(access_token=token)
vkapi = vk.API(access_token=token)
# vkapi = vk.API(session)

# Get today date and date for last month - convert to strings
today = datetime.date.today()
last_date = today - datetime.timedelta(days=30)
today = str(today)
last_date = str(last_date)

select_posts = """SELECT wall_post_created_by, COUNT(*), SUM(wall_post_comm), SUM(wall_post_like), SUM(wall_post_rep)
                FROM WALL_POSTS WHERE wall_post_date between %r and %r
                GROUP BY wall_post_created_by"""%(last_date,today)

print("'Select all activity from POST table between '"+today+" and "+last_date)
posts_results = ''
try:
    cursor.execute(select_posts)
    posts_results = cursor.fetchall()
except:
    print("Error: unable to fecth data")

print("Make dicts with results")
post_dicts_list = []
if posts_results:               # if table give posts tuples: (('-80849532', 46, 397.0, 204.0, 17.0), ('112983834', 1, 0.0, 2.0, 0.0))
    for post in posts_results:  # for each item in tuple of tuples: ('-80849532', 46, 397.0, 204.0, 17.0)
        posts_rating = 0
        user_id = post[0]
        user_id = user_id.replace('-', 'public')
        post_count = int(post[1])                   # post[1] = 46
        post_comments = int(post[2])                # post[2] = 397.0
        post_likes = int(post[3])                   # post[3] = 204.0
        post_reposts = int(post[4])                 # post[4] = 17.0
        post_rate = post_count                      # post count points = post quantity = 46
        comm_rate = post_comments * 0.2             # comments points = comments quantity * 0.2 = 79.4
        like_rate = post_likes * 0.1                # likes points = likes quantity * 0.1 =  20.4
        repo_rate = post_reposts * 0.7              # reposts points = reposts quantity * 0.7 = 8.5
        posts_rating = post_rate + comm_rate + like_rate + repo_rate
        user_rating = round(posts_rating, 3)
        if user_rating > 5:
            user_dict_with_post = {'user_id':user_id,                   # -80849532
                                   'user_posts':{'posts':post_count,          # 46
                                                 'comments':post_comments,    # 397.0
                                                 'likes':post_likes,          # 204.0
                                                 'repost':post_reposts},
                                    'user_rating':user_rating}
            post_dicts_list.append(user_dict_with_post)               # this is list of users which ids were found in posts_results
        else:
            pass
else:
    print("No post results")

print("Sort all data by rating DESC order")
sorted_all_counters = sorted(post_dicts_list, key=lambda k: k['user_rating'], reverse=True)

# Wiki page tags:
wiki_table_start = "{| \n|- \n! Пользователь: \n! Посты: \n! Комменты \n! Репосты \n! Лайки \n! Рейтинг "
wiki_table_id = "\n|- \n|"
wiki_table_cell = "| "
wiki_table_end = "\n|}"

print("Compose wiki tables")
wiki_users = []
for user in sorted_all_counters:
    if user['user_posts']['posts'] > 1:
        # match = re.match('-\d+')
        if "public" not in user['user_id']:
            wiki_user_id_string = wiki_table_id+"[[id"+user['user_id']+"]] \n"
        else:
            wiki_user_id_string = wiki_table_id+"[["+user['user_id']+"]] \n"
        user_posts = user['user_posts']
        wiki_user_posts_count = wiki_table_cell+str(user_posts['posts']) + "\n"
        wiki_user_posts_comments = wiki_table_cell+str(user_posts['comments']) + "\n"
        wiki_user_posts_repost = wiki_table_cell+str(user_posts['repost']) + "\n"
        wiki_user_posts_likes = wiki_table_cell+str(user_posts['likes']) + "\n"
        wiki_user_rating = wiki_table_cell+str(user['user_rating']) + " "
        wiki_user_str = wiki_user_id_string+wiki_user_posts_count+wiki_user_posts_comments+wiki_user_posts_repost+wiki_user_posts_likes+wiki_user_rating
        wiki_users.append(wiki_user_str)
    else:
        pass

wiki_those_ids = ', '.join(wiki_users)
wiki_those_ids = wiki_those_ids.replace(',', '')
wiki_table = wiki_table_start+wiki_those_ids+wiki_table_end

print("Compose wiki markups")
wiki_msg = "[[photo-46631810_395391488|600px;noborder| ]] \n" \
           "=== Таблица авторов за месяц ===\n" \
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
# Таблица рейтинга подробная авторы (месяц)
# https://vk.com/page-46631810_49912971
page = '49912971'

print("Post data to wiki page https://vk.com/page-46631810_49912971")
wiki_page = vkapi.pages.save(text=composed_message,
                             page_id=page,
                             group_id=group,
                             user_id=user,
                             title='')