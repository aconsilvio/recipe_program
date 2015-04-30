"""Python/Flask prgram to integrate recipe_program.py with GUI (homepage.html)"""
from flask import Flask, render_template, request, jsonify
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pickle import dump, load
from os.path import exists
from recipe_program import *
import ast

flask_recipes = Flask(__name__)

time_global = int
current_user = None

########################### MONGOLAB ##############
# Sets up server
server = 'ds061661.mongolab.com'
port = 61661
db_name = 'recipe_program_db'
username = 'anisha'
password = 'recipe' 
import pymongo
from pymongo import MongoClient

url = "mongodb://"+username+":"+password+"@"+server+":"+str(port)+"/"+db_name 

# Initializes Database
client = MongoClient(url)
db = client[db_name] # Get the database
db.authenticate(username, password) # Authenticate
posts = db.posts # Get the things in the db


@flask_recipes.route('/')
def homepage():
  """Renders inital HTML page"""
  return render_template('homepage.html')

@flask_recipes.route('/_make_user') # make name
def make_user():
  """Creates a User based on input from HTML page, returns a confirmation of their login and 
  what is currently in their pantry."""
  names = request.args.get('names', 1, type=str)  #raw text input from HTML page
  global db
  global current_user
  current_user = User(names, db)
  # Adding the user to the db occurs in the user class,
  # only in the get_pantry method
  str_pantry = current_user.get_pantry()
  if str_pantry == "":  #if current user doesn't have  pantry, return a string that states this
    return jsonify(name=current_user.name, pantry = " No Pantry")
  list_ingredients = ast.literal_eval(str_pantry) # Convert str to list
  str_pantry = " Pantry: " + list_ingredients[0] 
  for i in range(1, len(list_ingredients)):
    str_pantry += ", " + list_ingredients[i]
  return jsonify(name=current_user.name, pantry = str_pantry) #returns name and list of ingredients in pantry to HTML page

@flask_recipes.route('/_update_pantry') # add ingredients
def update_pantry():
  """Given a list of ingredients, adds these ingredients to current user's pantry."""
  pantry_ingredients = request.args.get('pantry', '', type=str) #raw input from HTML page of ingredients
  global current_user
  current_user.pantry.make_pantry(pantry_ingredients) #calls recipe_program function make_pantry()
  current_user.pantry.save_pantry()
  return jsonify(pantry = pantry_ingredients); #returns list of new pantry ingredients to HTML page


@flask_recipes.route('/_timed_recipes') # make name
def timed_recipes():
  """Given the max total cook time from html, returns a confirmation of this time, and sets global time variable"""
  time = request.args.get('time', 0, type=int)  #raw input from HTML page
  global time_global
  time_global = time #sets global time to inputted time, for use in search function
  return jsonify(cooktime=time_global)  #returns a confirmation of the input tiime


@flask_recipes.route('/_food_page') # add ingredients
def food_page():
  """Given a list of ingredients from HTML form, searches for recipes that contain only these ingredients"""
  fridge_ingredients = request.args.get('b', 0, type=str)  #raw input from HTML form
  global current_user
  current_user.fridge.make_fridge(fridge_ingredients) #uses function imported from recipe_program
  recipe_dictionaries = current_user.get_timed_recipes(time_global) #uses function imported from recipe_program, time global set in timed_recipes()
  #initalizing lists
  recipe_names = []
  recipe_ids = []
  recipe_pics = []
  cooktimes = []
  new_pics = []
  for i in range(len(recipe_dictionaries)):  #created lists of current recipe links, title, pictures, etc
    recipe_names.append(recipe_dictionaries[i]['recipeName'].encode('ascii','ignore')) #recipe name list
    recipe_ids.append(recipe_dictionaries[i]['id'].encode('ascii','ignore')) #recipe id list to generate links
    recipe_pics.append(recipe_dictionaries[i]['imageUrlsBySize']['90'].encode('ascii','ignore')) #recipe image links
    cooktimes.append(int(recipe_dictionaries[i]['totalTimeInSeconds']/60.0)) #recipe cooktime list
  for i in range(len(recipe_pics)):
    new_pics.append(recipe_pics[i][:len(recipe_pics[i])-4]+'250-c')  #this calls an image that is 300x300 px
  return jsonify(names = recipe_names, ids = recipe_ids, pics = new_pics, times = cooktimes);  #returns lists used to generate html page



if __name__ == '__main__':
    flask_recipes.run(host="0.0.0.0",port=int("8081"),debug=True)
    
  
