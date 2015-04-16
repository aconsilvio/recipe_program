from flask import Flask, render_template, request, jsonify
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pickle import dump, load
from os.path import exists
# from recipe_program import *
from recipe_program import *

flask_recipes = Flask(__name__)

@flask_recipes.route('/')
def homepage():
  return render_template('homepage.html')

@flask_recipes.route('/_make_user') # make name
def make_user():
  names = request.args.get('names', 1, type=str)
  current_user = User(names, 0)
  users.append(current_user)
  return jsonify(result=current_user.name)


@flask_recipes.route('/_food_page') # add ingredients
def food_page():
  fridge_ingredients = request.args.get('b', 0, type=str)
  current_user = users[0]
  current_user.fridge.make_fridge(fridge_ingredients)
  recipe_dictionaries = current_user.get_useful_recipes()
  recipe_names = []
  recipe_ids = []
  for i in range(len(recipe_dictionaries)):
    recipe_names.append(recipe_dictionaries[i]['recipeName'].encode('ascii','ignore'))
    recipe_ids.append(recipe_dictionaries[i]['id'].encode('ascii','ignore'))
  # return [jsonify(name = recipe_name, id = recipe_id) for recipe_name, recipe_id in zip(recipe_names, recipe_ids)]
  return jsonify(names = recipe_names, ids = recipe_ids);


  # get_useful_recipes(ingredients_list)


if __name__ == '__main__':
    users = []
    foods = []
    recipes= []
    # username = make_user()
    # db = 0
    # print username
    # current_user = User(username, db)
    # print current_user.name
    flask_recipes.run(host="0.0.0.0",port=int("8080"),debug=True)
  # flask_recipes.run(
  #   host = "0.0.0.0",
  #   port = int("8080"),
  #   debug = True
  # )
    
  