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
select_posts = """SELECT * FROM WALL_POSTS
            WHERE wall_post_comm > 0
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

print("How much posts were extracted: "+str(len(post_id_list)))
print("Splitting them on portions by 20")
split_by_10 = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
splited = split_by_10(post_id_list, 20)

def replace_all(text, rep_dic):
    for i, j in rep_dic.items():
        text = text.replace(i, j)
    return text
reps = {'[':'',' ':'',']':','}

print("Request data from vk by: execute.eachPost_getComments")
print("How many iterations will be: "+str(len(splited)))
all_comments = []
item_iteration = 1
error_keys = {'execute_errors', 'error_code', 'error', 'error_msg'}
for item in splited:
    item_str = str(item)
    post_list_arg = replace_all(item_str, reps)
    r = requests.post('https://api.vk.com/method/execute.eachPost_getComments?owner_id='+owner_id+'&post_id_array_str='+post_list_arg+'&access_token='+token)
    print("Iterations were done: "+str(item_iteration)+" of "+str(len(splited)))
    response_data = r.json()
    result = [value for key, value in response_data.items() if key in error_keys]
    if not result:
        data = response_data['response']
        all_comments.append(data)
        item_iteration = item_iteration+1
    else:
        print(response_data)

all_post_comments_formatted = []
for list in all_comments:
    for element in list:
        all_post_comments_formatted.append(element)
print("All comments parsed: "+str(len(all_post_comments_formatted)))

def parsing_comments(list_of_comments):
    """
    This will parse each comment dict and make tuple for each item
    :rtype : object
    """
    parsed_comments = []
    for each in list_of_comments:
        from_the_id = each['from_id']  # 'from_id': 111612257,
        comment_id = each['id']  # 'id': 51576
        comment_date = datetime.datetime.fromtimestamp(each['date']).strftime('%Y-%m-%d')  # Format time from UNIX to normal
        comment_time = datetime.datetime.fromtimestamp(each['date']).strftime('%H:%M:%S')  # Format time from UNIX to normal
        comment_has_likes = each['likes']  # 'likes': {'can_like': 1, 'count': 1, 'user_likes': 0}
        likes_count = comment_has_likes['count']  # 'count': 1
        # Tuple index:        [0]             [1]              [2]               [3]               [4]
        parsed_comment = (str(comment_id),str(from_the_id),str(comment_date),str(comment_time),str(likes_count))
        parsed_comments.append(parsed_comment)
    print("Function has finished comments parsing and add: "+str(len(parsed_comments))+" comments into list")
    return parsed_comments

comments_tuples_list = parsing_comments(all_post_comments_formatted)
print("Adding comments into the table")
if comments_tuples_list:
    for item in comments_tuples_list:
        sql_comments = """INSERT INTO PUB_COMMENTS
                          (comment_id,comment_user_id,comment_date,comment_time,comment_likes)
                          VALUES(%s, %s, %r, %r, %s)
                          ON DUPLICATE KEY UPDATE comment_likes = VALUES(comment_likes) ;
                       """ % (item[0],item[1],item[2],item[3],item[4],)
        cursor.execute(sql_comments)
        db.commit()
    db.close()

print("Bot has finished it's work with time:")
end = time()
print(end - start)