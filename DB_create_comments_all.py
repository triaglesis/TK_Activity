#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'
# Change history

import MySQLdb

db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity")

# Connection to database establish here:
# Like as vkapi
cursor = db.cursor()
# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS PUB_COMMENTS")

sql = """CREATE TABLE PUB_COMMENTS(
         comment_id CHAR(20) NOT NULL PRIMARY KEY,
         comment_user_id CHAR(20),
         comment_date CHAR(20),
         comment_time CHAR(20),
         comment_likes CHAR(20)
         )"""
# Execute previous command:
cursor.execute(sql)
# disconnect from database server and close cursor!
db.close()