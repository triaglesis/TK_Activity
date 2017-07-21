__author__ = 'danilcha'
# Change history
# Added new func. execute.eachPost_getComments which get recursively by 20 posts comments per iteration.
# Enhance table insert method
from time import sleep, time
import datetime
import MySQLdb
import requests
start = time()
# Configuration block
# db = MySQLdb.connect("192.168.1.25","tk_activity","tk_activity","tk_activity" )
db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity" )
cursor = db.cursor()
token = '43accf2d6642a5d3a0202c6801a9530cc0c0784533d7e4d04e55984c129fbcf789724f8a1ff3da5d409dc'
owner_id = "-46631810"
today = datetime.date.today()
last_date = str(today - datetime.timedelta(days=10))
today =  str(today)
# Table extraction block
post_id_list = []
post_id_list_2 = []
select_posts = """SELECT * FROM WALL_POSTS_ID
            WHERE wall_post_comm < 100 AND wall_post_comm > 0
            AND wall_post_date between %r and %r
            """%(last_date,today)
select_posts2 = """SELECT * FROM WALL_POSTS_ID
            WHERE wall_post_comm > 100  AND wall_post_comm < 1999
            AND wall_post_date between %r and %r
            """%(last_date,today)
print("Extracting posts ids from table between "+today+" and "+last_date)
try:
    cursor.execute(select_posts)
    results = cursor.fetchall()
    for row in results:
        post_id = int(row[0])    # Get post id ['51575']
        post_id_list.append(post_id) # Making list of tuples.
except:
    print("Error: unable to fecth data")
try:
    cursor.execute(select_posts2)
    results2 = cursor.fetchall()
    for row in results2:
        post_id = int(row[0])    # Get post id ['51575']
        post_id_list_2.append(post_id) # Making list of tuples.
except:
    print("Error: unable to fecth data")

def replace_all(text, rep_dic):
    for i, j in rep_dic.items():
        text = text.replace(i, j)
    return text
reps = {'[':'',' ':'',']':','}
split_by = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

all_comments = []
if post_id_list:
    print("Start to parse all posts where comments < 100 and > 0")
    print("How much were extracted: "+str(len(post_id_list)))
    print("Splitting them on portions by 20")
    splited = split_by(post_id_list, 20)
    print("Request data from vk by: execute.eachPost_getComments")
    print("How many iterations will be: "+str(len(splited)))
    error_keys = {'execute_errors', 'error_code', 'error', 'error_msg'}
    item_iteration = 1
    for item in splited:
        item_str = str(item)
        post_list_arg = replace_all(item_str, reps)
        r = requests.post('https://api.vk.com/method/execute.wall_getComments_parsed?owner_id='+owner_id+'&post_id_array_str='+post_list_arg+'&access_token='+token)
        print("Iterations were done: "+str(item_iteration)+" of "+str(len(splited)))
        response_data = r.json()
        result = [value for key, value in response_data.items() if key in error_keys]
        # sleep(1)
        if not result:
            data = response_data['response']
            all_comments.append(data)
            item_iteration = item_iteration+1
        else:
            print(response_data)
    print("Finished extraction for all posts where comments < 100 and > 0\n")
else:
    print("No posts with < 300 and > 0 comments found in database")

if post_id_list_2:
    print("Start to parse all posts where comments > 100 AND < 1999")
    print("How much posts were extracted: "+str(len(post_id_list_2)))
    print("Splitting them on portions by 1")
    splited_2 = split_by(post_id_list_2, 1)
    print("Request data from vk by: execute.eachPost_getComments")
    print("How many iterations will be: "+str(len(splited_2)))
    error_keys = {'execute_errors', 'error_code', 'error', 'error_msg'}
    item_iteration = 1
    for item in splited_2:
        item_str = str(item)
        post_list_arg = replace_all(item_str, reps)
        r = requests.post('https://api.vk.com/method/execute.wall_getComments_parsed?owner_id='+owner_id+'&post_id_array_str='+post_list_arg+'&access_token='+token)
        print("Iterations were done: "+str(item_iteration)+" of "+str(len(splited_2)))
        response_data = r.json()
        result = [value for key, value in response_data.items() if key in error_keys]
        sleep(0.2)
        if not result:
            data = response_data['response']
            all_comments.append(data)
            item_iteration = item_iteration+1
        else:
            print(response_data)
    print("Finished extraction for all posts where comments > 100 AND < 1999\n")
else:
    print("No posts with > 300 comments found in database")

all_post_comments_formatted = []
for list_item in all_comments:
    for element in list_item:
        element_formatted = list(zip(element[0],element[1],element[2],element[3]))
        all_post_comments_formatted.append(element_formatted)

# print("How much comments were extracted: "+str(len(all_post_comments_formatted)))
print("Adding comments into the table")
items = 0
if all_post_comments_formatted:
    for list_item in all_post_comments_formatted:
        for item in list_item:
            comment_id = item[0]
            comment_user_id = item[1]
            comment_date = datetime.datetime.fromtimestamp(item[2]).strftime('%Y-%m-%d')
            comment_time = datetime.datetime.fromtimestamp(item[2]).strftime('%H:%M:%S')
            comment_likes = item[3]
            sql_comments = """INSERT INTO PUB_COMMENTS
                              (comment_id,comment_user_id,comment_date,comment_time,comment_likes)
                              VALUES(%s, %s, %r, %r, %s)
                              ON DUPLICATE KEY UPDATE comment_likes = VALUES(comment_likes) ;
                           """ % (comment_id,comment_user_id,comment_date,comment_time,comment_likes)
            cursor.execute(sql_comments)
            items = items + 1
db.commit()
db.close()

print("How many comments were added into table: "+str(items))
print("Bot has finished it's work with time:")
end = time()
print(end - start)