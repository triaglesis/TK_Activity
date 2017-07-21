#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'
# Change history
# Added new func. execute.wall_getPosts_all which get recursively by 2000 posts per iteration.
# Enhance table insert method

from time import time
import datetime
import MySQLdb
import requests

start = time()
print("Bot has started it's work")
# Configuration block
# db = MySQLdb.connect("192.168.1.25","tk_activity","tk_activity","tk_activity" )
db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity" )
cursor = db.cursor()
token = 'TOKEN'
owner_id = "-46631810"
domain = "typical_kirovohrad"

# Get all post from wall by 2000 items per iteration
posts_cnt = 1
global_offset_posts = 0
post_data = []
posts_list = []
error_keys = {'execute_errors', 'error_code', 'error', 'error_msg'}
print("Get just 2000 last posts from wall from VK execute.wall_getPosts_all_two")
r = requests.post('https://api.vk.com/method/execute.wall_getPosts_all_two?owner_id='+owner_id+'&domain='+domain+'&global_offset_posts='+str(global_offset_posts)+'&access_token='+token)
if r:
    response_data = r.json()
    result = [value for key, value in response_data.items() if key in error_keys]
    if not result:
        data = response_data['response']
        posts = data['posts']
        for posts_set in posts:
            # post_format = [(post_id),(post_date),(post_comments_cnt),(post_likes_cnt),(post_repost_cnt),(post_from_id)];
            posts_list_zip = list(zip(posts_set[0],posts_set[1],posts_set[1],posts_set[2]))
            posts_list.append(posts_list_zip)
        # global_offset_posts = global_offset_posts + 2000
    else:
        print(result)
else:
    print("VK is not responding")

wall_posts_list = []
for lists in posts_list:
    for element in lists:
        wall_posts_list.append(element)
print(len(wall_posts_list))

# DROP DATABASE!!! This is ti wipe old IDs
print("Drop database WALL_POSTS_ID")
cursor.execute("DROP TABLE IF EXISTS WALL_POSTS_ID")
sql_create = """CREATE TABLE WALL_POSTS_ID(
                      wall_post_id CHAR(20) NOT NULL PRIMARY KEY,
                      wall_post_date CHAR(20),
                      wall_post_time CHAR(20),
                      wall_post_comm CHAR(20)
                      )"""
cursor.execute(sql_create)
# db.close()

if wall_posts_list:
    for item in wall_posts_list:
        wall_post_id = item[0]
        wall_post_date = datetime.datetime.fromtimestamp(item[1]).strftime('%Y-%m-%d')
        wall_post_time = datetime.datetime.fromtimestamp(item[2]).strftime('%H:%M:%S')
        wall_post_comm = item[3]
        sql_add = """INSERT INTO WALL_POSTS_ID(wall_post_id,
                                               wall_post_date,
                                               wall_post_time,
                                               wall_post_comm)
        VALUES (%s, %r, %r, %s);
                          """ % (wall_post_id,
                                 wall_post_date,
                                 wall_post_time,
                                 wall_post_comm)
        cursor.execute(sql_add)
else:
    print("Nothing was extracted and added to tables")

db.commit()
db.close()

print("Script has finished his work. Exec time:")
end = time()
print(end - start)