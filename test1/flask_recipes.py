from flask import Flask, render_template, request, jsonify
from recipe_with_yummly import *
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pickle import dump, load
from os.path import exists

flask_recipes = Flask(__name__)

def test_printing_foods():
  print "foods are ", foods

@flask_recipes.route('/')
def homepage():
  return render_template('homepage.html')

@flask_recipes.route('/_food_page') # add ingredients
def food_page():
  a = request.args.get('a', 0, type=str)
  foods.append(a)
  test_printing_foods()
  return jsonify(result=a)

# def get_ingredient_strings(food):
#   #food is a long string of ingredients
#   food_list = food.split(", ")
#   return food_list

# def get_url(ingredient):
#   """Format url for api call"""
#   for letter in ingredient:
#     formatted = ingredient.replace(' ',"%20")
#   url = "http://api.yummly.com/v1/api/recipes?_app_id=c95876fa&_app_key=ef0c2016540a55876cffbabe427d6d83&allowedIngredient[]=%s" % (formatted)
#   return url

# def get_json(url):
#   """
#   Given a properly formatted URL for a JSON web API request, return
#   a Python JSON object containing the response to that request.
#   """
#   f = urllib2.urlopen(url)  #opens url
#   response_text = f.read()  #reads through url
#   response_data = json.loads(response_text)  #converts data to json
#   return response_data
  
# def get_all_recipes(ingredients):
#   """ Gets a list of all recipes for a list of ingredients """
#   empty_page = 0
#   recipe_list = []
#   for ingredient in ingredients:
#     url = get_url(ingredient)
#     contents_all = get_json(url)
#     if contents_all['totalMatchCount'] == empty_page:
#       print "There is nothing here for ", ingredient
#     else:
#       contents = contents_all['matches']
#       recipe_list += contents
#   return recipe_list

# def food_page():
#     food = request.args.get('food', 0, type = str)
#     return jsonify(food)


if __name__ == '__main__':
    foods = []
    flask_recipes.run(host="0.0.0.0",port=int("8080"),debug=True)
  # flask_recipes.run(
  #   host = "0.0.0.0",
  #   port = int("8080"),
  #   debug = True
  # )
  