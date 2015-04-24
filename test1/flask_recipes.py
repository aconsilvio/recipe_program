from flask import Flask, render_template, request, jsonify
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pickle import dump, load
from os.path import exists
# from recipe_program import *
from recipe_program import *

flask_recipes = Flask(__name__)

# Global vars
#users = []
#foods = []
#recipes= []
time_global = int
current_user = None

########################### MONGOLAB ##############
server = 'ds061661.mongolab.com'
port = 61661
db_name = 'recipe_program_db'
username = 'anisha'
password = 'recipe' 
import pymongo
from pymongo import MongoClient

url = "mongodb://"+username+":"+password+"@"+server+":"+str(port)+"/"+db_name 

client = MongoClient(url)
db = client[db_name] # Get the database
db.authenticate(username, password) # Authenticate
posts = db.posts # Get the things in the db


@flask_recipes.route('/')
def homepage():
  return render_template('homepage.html')

@flask_recipes.route('/_make_user') # make name
def make_user():
  names = request.args.get('names', 1, type=str)
  global db
  global current_user
  current_user = User(names, db)
  db.users.insert({"user": current_user.name, "pantry": None})
  #users.append(current_user)
  return jsonify(name=current_user.name, pantry = current_user.get_pantry())
  #return jsonify(result=names)

@flask_recipes.route('/_update_pantry') # add ingredients
def update_pantry():
  pantry_ingredients = request.args.get('pantry', '', type=str)
  global current_user
  #current_user = users[0]
  current_user.pantry.make_pantry(pantry_ingredients)
  current_user.pantry.save_pantry()
  return jsonify(pantry = pantry_ingredients);


@flask_recipes.route('/_timed_recipes') # make name
def timed_recipes():
  time = request.args.get('time', 0, type=int)
  global time_global
  time_global = time
  return jsonify(cooktime=time_global)


@flask_recipes.route('/_food_page') # add ingredients
def food_page():
  fridge_ingredients = request.args.get('b', 0, type=str)
  global current_user
  #current_user = users[0]
  current_user.fridge.make_fridge(fridge_ingredients)
  recipe_dictionaries = current_user.get_timed_recipes(time_global)
  recipe_names = []
  recipe_ids = []
  recipe_pics = []
  cooktimes = []
  new_pics = []
  for i in range(len(recipe_dictionaries)):
    recipe_names.append(recipe_dictionaries[i]['recipeName'].encode('ascii','ignore'))
    recipe_ids.append(recipe_dictionaries[i]['id'].encode('ascii','ignore'))
    recipe_pics.append(recipe_dictionaries[i]['imageUrlsBySize']['90'].encode('ascii','ignore'))
    cooktimes.append(int(recipe_dictionaries[i]['totalTimeInSeconds']/60.0))
  # return [jsonify(name = recipe_name, id = recipe_id) for recipe_name, recipe_id in zip(recipe_names, recipe_ids)]
  for i in range(len(recipe_pics)):
    ##[-4:-2]
    new_pics.append(recipe_pics[i][:len(recipe_pics[i])-4]+'250-c')  #this calls an image that is 300x300 px
  return jsonify(names = recipe_names, ids = recipe_ids, pics = new_pics, times = cooktimes);



if __name__ == '__main__':
    # users = []
    # foods = []
    # recipes= []
    # time_global = []
    # username = make_user()
    # db = 0
    # print username
    # current_user = User(username, db)
    # print current_user.name
    #print db.users.find_one()
    #db.users.remove()
    #print db.users.find_one()
    #db.recipes.remove()
    #print db.recipes.find_one({'ingredient': 'cinnamon'})
    flask_recipes.run(host="0.0.0.0",port=int("8081"),debug=True)
  # flask_recipes.run(
  #   host = "0.0.0.0",
  #   port = int("8080"),
  #   debug = True
  # )
    
  
