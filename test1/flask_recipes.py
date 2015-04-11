from flask import Flask, render_template, request, jsonify
from recipe_with_yummly import *
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pickle import dump, load
from os.path import exists
from recipe_program import *

flask_recipes = Flask(__name__)

def return_foods():
  return foods

def get_recipes():
  return recipes

@flask_recipes.route('/')
def homepage():
  return render_template('homepage.html')

@flask_recipes.route('/_food_page') # add ingredients
def food_page():
  a = request.args.get('a', 0, type=str)
  foods.append(a)
  print return_foods()
  return jsonify(result=a)

@flask_recipes.route('/_return_recipes') # add ingredients
def return_recipes():
  b = request.args.get('b', 0, type=str)
  current_user = User()
  recipes.append(current_user.get_useful_recipes(b))
  print recipes
  return jsonify(result2=b)


  # get_useful_recipes(ingredients_list)


if __name__ == '__main__':
    foods = []
    recipes= []
    flask_recipes.run(host="0.0.0.0",port=int("8080"),debug=True)
  # flask_recipes.run(
  #   host = "0.0.0.0",
  #   port = int("8080"),
  #   debug = True
  # )
  