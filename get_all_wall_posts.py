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
token = '3f18130f132411eebb3bfbdc113fc00693a09a98626e2703aea2c04b91cebad5088e2466d590d95760674'
owner_id = "-46631810"
domain = "typical_kirovohrad"

# Get all post from wall by 2000 items per iteration
posts_cnt = 1
global_offset_posts = 0
post_data = []
error_keys = {'execute_errors', 'error_code', 'error', 'error_msg'}
print("Get posts from wall from VK execute.wall_getPosts_all")
while global_offset_posts < posts_cnt:
    r = requests.post('https://api.vk.com/method/execute.wall_getPosts_all_two?owner_id='+owner_id+'&domain='+domain+'&global_offset_posts='+str(global_offset_posts)+'&access_token='+token)
    global_offset_posts = global_offset_posts + 2000
    response_data = r.json()
    result = [value for key, value in response_data.items() if key in error_keys]
    if not result:
        data = response_data['response']
        posts = data['posts']
        for posts_set in posts:
            for item in posts_set:
                post_data.append(item)
        posts_cnt = data['posts_cnt']
        run_count = data['run_count']
        iter_count = data['iter_count']
        offset_posts = data['offset_posts']
        print("Posts present: "+str(posts_cnt)+"| Runs: "+str(run_count)+"| Iters: "+str(iter_count)+"| Offset of posts is: "+str(offset_posts))

    else:
        print(result)

print("Zip lists")
wall_posts_list = list(zip(post_data[0],post_data[1],post_data[1],post_data[2],post_data[3],post_data[4],post_data[5]))
print("Insert table")
if wall_posts_list:
    for item in wall_posts_list:
        wall_post_id = item[0]
        wall_post_date = datetime.datetime.fromtimestamp(item[1]).strftime('%Y-%m-%d')
        wall_post_time = datetime.datetime.fromtimestamp(item[2]).strftime('%H:%M:%S')
        wall_post_comm = item[3]
        wall_post_like = item[4]
        wall_post_rep = item[5]
        wall_post_created_by = item[6]
        sql = """INSERT INTO WALL_POSTS(wall_post_id,
                                        wall_post_date,
                                        wall_post_time,
                                        wall_post_comm,
                                        wall_post_like,
                                        wall_post_rep,
                                        wall_post_created_by)
        VALUES (%s, %r, %r, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            wall_post_comm = VALUES(wall_post_comm),
            wall_post_like = VALUES(wall_post_like),
            wall_post_rep = VALUES(wall_post_rep) ;
                          """ % (wall_post_id,
                                 wall_post_date,
                                 wall_post_time,
                                 wall_post_comm,
                                 wall_post_like,
                                 wall_post_rep,
                                 wall_post_created_by)
        cursor.execute(sql)
    db.commit()
    db.close()
else:
    print("Nothing was extracted and added to tables")

print("Script has finished his work. Exec time:")
end = time()
print(end - start)