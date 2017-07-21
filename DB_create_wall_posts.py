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
cursor.execute("DROP TABLE IF EXISTS WALL_POSTS")
# Creation of table with name 'LIST_OF_SOMETHING' where one cell is present as 'SOMETHING'
# Then we will add into this table some data.
# From scandal_kir - 80849532
sql = """CREATE TABLE WALL_POSTS(
                      wall_post_id CHAR(20) NOT NULL PRIMARY KEY,
                      wall_post_date CHAR(20),
                      wall_post_time CHAR(20),
                      wall_post_comm CHAR(20),
                      wall_post_like CHAR(20),
                      wall_post_rep CHAR(20),
                      wall_post_created_by CHAR(20) NOT NULL
                      )"""
# Execute previous command:
cursor.execute(sql)
# disconnect from database server and close cursor!
db.close()