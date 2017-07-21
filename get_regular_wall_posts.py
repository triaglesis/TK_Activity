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
tk_owner_id = "-46631810"
tk_domain = "typical_kirovohrad"

# Get all post from wall by 2000 items per iteration
posts_cnt = 1
wall_posts_list = []
error_keys = {'execute_errors', 'error_code', 'error', 'error_msg'}
print("Get posts from wall from VK execute.get_wallPost_regular")
# This will get last 500 posts from the wall
r = requests.post('https://api.vk.com/method/execute.get_wallPost_regular?owner_id='+tk_owner_id+'&domain='+tk_domain+'&access_token='+token)
response_data = r.json()
result = [value for key, value in response_data.items() if key in error_keys]
if not result:
    data = response_data['response']
    posts = data['posts']
    for posts_set in posts:
        for item in posts_set:
            wall_posts_list.append(item)
    posts_cnt = data['posts_cnt']
    run_count = data['run_count']
    iter_count = data['iter_count']
    offset_posts = data['offset_posts']
    print("Posts present: "+str(posts_cnt)+"| Runs: "+str(run_count)+"| Iters: "+str(iter_count)+"| Offset of posts is: "+str(offset_posts))
else:
    print(result)

print("All posts parsed: "+str(len(wall_posts_list)))
print("Will parse gathered data and insert in into tables")

parsed_posts_list =[]
if wall_posts_list:
    for post in wall_posts_list:
        wall_post_id = post['id']                       # id: 426479,
        date = post['date']                             # date: 1438687277,
        # Date convert in human readable
        wall_post_date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
        wall_post_date = str(wall_post_date)
        wall_post_time = datetime.datetime.fromtimestamp(date).strftime('%H:%M:%S')
        wall_post_time = str(wall_post_time)
        # Who is the author?
        if 'created_by' in post:
            wall_post_created_by = post['created_by']   # created_by: 15782913,
        elif 'signer_id' in post:
            wall_post_created_by = post['signer_id']    # signer_id: 13147598,
        else:
            wall_post_created_by = post['from_id']      # from_id: -80849532,
        comments = post['comments']                     # comments: { count: 12950,can_post: 1}
        wall_post_comm = comments['count']              # count: 12950
        likes = post['likes']                           # likes: {count: 37496,user_likes: 0,can_like: 1,can_publish: 1},
        wall_post_like = likes['count']                 # count: 37496
        reposts = post['reposts']                       # reposts: {count: 276,user_reposted: 0}
        wall_post_rep = reposts['count']                # count: 276
        # INSERT into table each found post IF post EXIST - update values
        # Tuple index: [0]          [1]            [2]            [3]            [4]            [5]           [6]
        parsed_post = (str(wall_post_id),str(wall_post_date),str(wall_post_time),str(wall_post_comm),str(wall_post_like),str(wall_post_rep),str(wall_post_created_by))
        parsed_posts_list.append(parsed_post)


print("There are: "+str(len(parsed_posts_list))+" parsed posts in list")
print("Adding each parsed post from list to tables")
print("Example of first item in list: "+str(parsed_posts_list[0]))

if parsed_posts_list:
    for item in parsed_posts_list:
        # print(item[0],item[1],item[2],item[3],item[4],item[5],item[6])
        # break
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
                          """ % (item[0],item[1],item[2],item[3],item[4],item[5],item[6])
        cursor.execute(sql)
        db.commit()
    db.close()
else:
    print("Nothing was extracted and added to tables")

print("Script has finished his work. Exec time:")
end = time()
print(end - start)