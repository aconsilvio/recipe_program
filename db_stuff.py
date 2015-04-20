# How to run heroku:
# $ heroku login
# $ source venv/bin/activate
# $ foreman start
# $ pip install -r requirements.txt --allow-all-external
# $ git add .
# $ git commit -m "stuff"
# $ git push heroku master
# $ heroku open

# kill port process:
# ps -fA | grep python
# kill <number>

########################### MONGOLAB ######################################

server = 'ds061661.mongolab.com'
port = 61661
db_name = 'recipe_program_db'
username = 'anisha'
password = 'recipe' 

#url = "mongodb://"+username+":"+password+"@host:"+port+"/"+db_name 

from pymongo import MongoClient

client = MongoClient(server, port)

# Get the database
print '\nGetting database ...'
db = client[db_name] 

# Have to authenticate to get access
print '\nAuthenticating ...'
db.authenticate(username, password) 

# Get the documents
posts = db.posts
print '\nNumber of posts', posts.find().count() 

#db.friends.insert({'name': 'annabel', 'food': 'cheese'})
#db.friends.insert({'name': 'anisha', 'food': 'chocolate'})
#print db.friends
string = db.friends.find_one({'name': 'anisha'})
print string
print type(string)
#db.enemies.insert({'andrew': 'music'})
#print db.enemies
#db.enemies.remove()
#print db.enemies.find_one()
#print
#print db.posts



########################### MONGODB PYMONGO STUFF #########################

# # In terminal, run $sudo service mongod start

# import pymongo
# import datetime
# from pymongo import MongoClient
# my_client = MongoClient()
# my_db = my_client.my_test_database
# print my_db
# my_post = {"author": "Mike", "text": "My first blog post!",
#            "date": datetime.datetime.utcnow()}
# my_post2 = {"author": "Mike2", "text": "My first blog post!2",
#            "date": datetime.datetime.utcnow()}
# my_posts = my_db.posts
# print my_posts
# post_id = my_posts.insert_one(my_post).inserted_id
# print post_id
# my_posts.insert_one(my_post2)
# print
# print my_posts
# print
# print my_posts.find_one()
# print my_posts.find_one({"author": "Mike"})
# print my_posts.find_one({"author": "Mike2"})
# print my_posts.find_one({"_id": post_id})
# print
# this_post = my_posts.find_one({"author": "Mike2"})
# print this_post["text"]

# # THIS DOESNT WORK
# ##new_post = Test()
# ##my_posts.insert_one(new_post).inserted_id
