class Test(object):
    def __init__(self):
        self.a = 1

# In terminal, run $sudo service mongod start

import pymongo
import datetime
from pymongo import MongoClient
my_client = MongoClient()
my_db = my_client.my_test_database
print my_db
my_post = {"author": "Mike", "text": "My first blog post!",
           "date": datetime.datetime.utcnow()}
my_post2 = {"author": "Mike2", "text": "My first blog post!2",
           "date": datetime.datetime.utcnow()}
my_posts = my_db.posts
print my_posts
post_id = my_posts.insert_one(my_post).inserted_id
print post_id
my_posts.insert_one(my_post2)
print
print my_posts
print
print my_posts.find_one()
print my_posts.find_one({"author": "Mike"})
print my_posts.find_one({"author": "Mike2"})
print my_posts.find_one({"_id": post_id})
print
this_post = my_posts.find_one({"author": "Mike2"})
print this_post["text"]

# THIS DOESNT WORK
##new_post = Test()
##my_posts.insert_one(new_post).inserted_id
