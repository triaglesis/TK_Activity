#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'
# Change history

import vk
from time import strftime
import datetime
import MySQLdb
import math

db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity")
cursor = db.cursor()

# TODO:
# New version for Vkontakte api for module ver 2.0a4 and above
token = 'TOKEN'
# session = vk.Session(access_token=token)
vkapi = vk.API(access_token=token)
# vkapi = vk.API(session)

# Get today date and date for last month - convert to strings
today = datetime.date.today()
last_date = today - datetime.timedelta(days=30)
today = str(today)
last_date = str(last_date)

# TODO: Select all comment items where date between today and minus 7 days
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
# This is user rating dictionary where each user's activity will be added.
# If now activity - counter will have value = 0
user_id = 0
comm_count = 0
likes_count = 0
post_count = 0
post_reposts = 0
post_comments = 0
post_likes = 0
repost_count = 0
user_rating = 0
user_ratings_dict = {'user_id':user_id,                         # vk unique user id
                     'user_comments':comm_count,                # how much user left comments
                     'user_likes':likes_count,                  # how much user's comments get likes
                     'user_posts':{'posts':post_count,          # how much user make posts
                                   'comments':post_comments,    # how much user's post get comments
                                   'likes':post_likes,          # how much user's post get likes
                                   'repost':post_reposts        # how much user's post get reposts
                                   },
                     'user_reposts':repost_count,               # how much user did reposts
                     'user_rating':user_rating}                 # user's rating based ion prev counters

print("Make spare dicts and count the ratings")
# At first this loop will parse all elements extracted from database from table of comments
# It will add each comment counters like as: likes, comments count, to one dictionary with unique user id
# user id is id of user who left comment
# Then it will parse all elements extracted from database table of posts
# It will add each post counters like as: reposts, likes, comments under this post, to one dictionary with unique user id
# user id is id of user who made this post
all_dicts_list = []
post_dicts_list = []
user_ratings_dict_with_post = []
if comments_results:                                    # if table give comment tuples: (('-80849532', 14, 7.0), ('100072457', 1, 0.0))
    for item in comments_results:                       # For each item in tuple of tuples: ('-80849532', 14, 7.0)
        user_id = item[0]                               # item[0] = '-80849532'
        comm_count = item[1]                            # item[1] = 14
        comm_int = int(comm_count) * 0.1                # make comments count int for sure and mult by 0.5
        likes_count = item[2]                           # item[2] = 7.0
        likes_int = int(likes_count) * 1              # make likes count int and mult by 0.2
        user_id = user_id.replace('-', 'public')        # replace "-" for public id with "public"
        user_rating = likes_int + comm_int              # user rating is sum of comments int and likes int
        user_rating = round(user_rating, 3)
        user_ratings_dict = {'user_id':user_id,                         # -80849532
                             'user_comments':comm_count,                # comments points = comments quantity * 0.5 = 8.5
                             'user_likes':likes_count,                  # likes points = likes quantity * 0.2 =  1.4
                             'user_posts':{'posts':post_count,          # 0
                                           'comments':post_comments,    # 0
                                           'likes':post_likes,          # 0
                                           'repost':post_reposts        # 0
                                           },
                             'user_reposts':repost_count,               # 0
                             'user_rating':user_rating}                 # 8.4
        # If post result were extracted and it have items - this will update prev items with same user id or add new, if author left no comments
        if posts_results:               # if table give posts tuples: (('-80849532', 46, 397.0, 204.0, 17.0), ('112983834', 1, 0.0, 2.0, 0.0))
            for post in posts_results:  # for each item in tuple of tuples: ('-80849532', 46, 397.0, 204.0, 17.0)
                post_by_id = post[0]                            # post[0] = -80849532
                post_by_id = post_by_id.replace('-', 'public')  # replace "-" for public id with "public"
                if post_by_id in user_ratings_dict['user_id']:  # if id "-80849532" found in "user_ratings_dict" where key 'user_id' has value = -80849532
                    posts_rating = 0
                    post_count = int(post[1])                   # post[1] = 46
                    post_comments = int(post[2])                # post[2] = 397.0
                    post_likes = int(post[3])                   # post[3] = 204.0
                    post_reposts = int(post[4])                 # post[4] = 17.0
                    post_rate = post_count                      # post count points = post quantity = 46
                    comm_rate = post_comments * 0.2             # comments points = comments quantity * 0.2 = 79.4
                    like_rate = post_likes * 0.1                # likes points = likes quantity * 0.1 =  20.4
                    repo_rate = post_reposts * 0.7              # reposts points = reposts quantity * 0.7 = 8.5
                    posts_rating = post_rate + comm_rate + like_rate + repo_rate
                    user_rating = (user_ratings_dict['user_rating'] + posts_rating)
                    user_rating = round(user_rating, 3)
                    user_ratings_dict_with_post = {'user_id':user_id,                             # -80849532
                                             'user_comments':comm_count,                # 14
                                             'user_likes':likes_count,                  # 7.0
                                             'user_posts':{'posts':post_count,          # 46
                                                           'comments':post_comments,    # 397.0
                                                           'likes':post_likes,          # 204.0
                                                           'repost':post_reposts        # 17.0
                                                           },
                                             'user_reposts':repost_count,               # 0
                                             'user_rating':user_rating}                 # 166.1
                    # post_dicts_list.append(user_ratings_dict)               # this is list of users which ids were found in posts_results
                # if somebody do post but left no comment at all
                # TODO: Make it work! Now it just make 99 dubles with one ID
                else: # if id "-80849532" NOT found in "user_ratings_dict" where key 'user_id' has value = -80849532
                    null_posts = user_ratings_dict['user_posts']
                    # print(post)
                    # post_count = null_posts['posts']
                    # post_comments = null_posts['comments']
                    # post_likes = null_posts['likes']
                    # post_reposts = null_posts['repost']
                    user_ratings_dict_with_post = {'user_id':user_id,                             # -80849532
                                             'user_comments':comm_count,                # 14
                                             'user_likes':likes_count,                  # 7.0
                                             'user_posts':{'posts':post_count,
                                                           'comments':post_comments,
                                                           'likes':post_likes,
                                                           'repost':post_reposts
                                                           },
                                             'user_reposts':repost_count,               # 0
                                             'user_rating':user_rating}                 #

                # break # run as much times as missed item found
        else:
            print("No post results")
        if user_rating > 10:
            all_dicts_list.append(user_ratings_dict_with_post)                                     # this is list  with all users and all refreshed dicts
        else:
            pass
        # break #will return only first user_id
else:
    print("No comments_results")

print("Sort all data by rating DESC order")
sorted_all_counters = sorted(all_dicts_list, key=lambda k: k['user_rating'], reverse=True)

# Wiki page tags:
# wiki_table_start = "{| \n|- \n! Пользователь: \n! Комменты \n! Лайки \n! Посты: \n! Комменты \n! Лайки \n! Репосты \n! Рейтинг "
wiki_table_start = "{| \n|- \n! Пользователь: \n! Рейтинг (посты+лайки+репосты): "
wiki_table_id = "\n|- \n|"
wiki_table_cell = "| "
wiki_table_end = "\n|}"

print("Compose wiki tables")
wiki_users = []
for user in sorted_all_counters:
    # match = re.match('-\d+')
    if "public" not in user['user_id']:
        wiki_user_id_string = wiki_table_id+"[[id"+user['user_id']+"]] \n"
    else:
        wiki_user_id_string = wiki_table_id+"[["+user['user_id']+"]] \n"
    # wiki_user_comments = wiki_table_cell+str(user['user_comments']) + "\n"
    # wiki_user_likes = wiki_table_cell+str(user['user_likes']) + "\n"
    # user_posts = user['user_posts']
    # wiki_user_posts_count = wiki_table_cell+str(user_posts['posts']) + "\n"
    # wiki_user_posts_comments = wiki_table_cell+str(user_posts['comments']) + "\n"
    # wiki_user_posts_repost = wiki_table_cell+str(user_posts['repost']) + "\n"
    # wiki_user_posts_likes = wiki_table_cell+str(user_posts['likes']) + "\n"
    wiki_user_rating = wiki_table_cell+str(user['user_rating']) + " "
    wiki_user_str = wiki_user_id_string+wiki_user_rating
    # wiki_user_str = wiki_user_id_string+wiki_user_comments+wiki_user_likes+wiki_user_posts_count+\
    #                 wiki_user_posts_comments+wiki_user_posts_repost+wiki_user_posts_likes+wiki_user_rating
    wiki_users.append(wiki_user_str)

print("Compose wiki markups")
wiki_those_ids = ', '.join(wiki_users)
wiki_those_ids = wiki_those_ids.replace(',', '')
wiki_table = wiki_table_start+wiki_those_ids+wiki_table_end

wiki_msg = "=== Таблица рейтинга за месяц ===\n" \
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
# Таблица рейтинга общая (месяц)
# https://vk.com/page-46631810_49898050
page = '49898050'
print("Post data to wiki page https://vk.com/page-46631810_49898050")
wiki_page = vkapi.pages.save(text=composed_message,
                             page_id=page,
                             group_id=group,
                             user_id=user,
                             title='')