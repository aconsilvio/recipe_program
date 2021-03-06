"""
Recipe Program Back-end
Contains class structure including User, Shelf, Fridge, Pantry, Ingredients
User class has functions to search recipe database
File to be called from flask_recipes.py program

Authors: Anisha, Annabel, Maggie
"""

############################ IMPORT LIBRARIES #####################

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pymongo import MongoClient
import ast # This allows for convertion between str to list

############################ CLASSES ##############################

class User(object):
  """ Class that defines a user
      name: username (a string), the identifier
      pantry: new empty pantry object
      fridge: new empty fridge object
      db: the database that stores users and recipes
  """
  def __init__(self, name, db):
    self.name = name
    self.pantry = Pantry(name, db)
    self.fridge = Fridge()
    self.db = db
    
  def __str__(self):
    """ Returns the user's name """
    return self.name

  def get_pantry(self):
    """ Return the pantry if it exists, or an empty string """
    # Look for the user in the database
    users = self.db.users
    user = users.find_one({"user": self.name})

    # If the user does not exist in the database, make a new entry
    if user == None: 
      users.insert({"user": self.name, "pantry": None})
      return ""
    # If the user exists but the pantry does not, return an empty strign
    elif user["pantry"] == None:
      return ""
    # Otherwise, the user exists. Build up and return the pantry from the db
    else:
      ingredients = ast.literal_eval(user["pantry"]) # Convert str to list
      ingredient_list = [] # Empty list to store ingredient objects
      for i in ingredients:
        # Add ingredients as ingredient objects to the pantry
        ingredient_list.append(Ingredient(i))
      # Update the pantry attribute with the existing (stored) pantry
      self.pantry.ingredients = ingredient_list
      return str(self.pantry)

  def get_useful_recipes(self):
    """ Generate recipes based on fridge and pantry with yummly API
        returns a list of recipes that do not contain any ingredients
        that are not in the users fridge or pantry
    """
    # Build up a list of all recipes that contain at least one ingredient
    all_recipes = []
    All_Ingredients = self.fridge.ingredients + self.pantry.ingredients
    for ingredient in All_Ingredients:
      all_recipes += (self.get_all_recipes(ingredient))

    # Only save recipes where you have all the ingredients
    recipe_copy = [] # empty list, will append good recipes
    for i in range(len(all_recipes)): # loop through all recipes
      good_recipe = True
      # Get list of all ingredients necessary to make the recipe
      required_ingredients = all_recipes[i][u'ingredients']
      for element in required_ingredients:
        element = element.encode('utf-8') #format string
        good_ingredient = False
        # See if the user has the correct ingredients for this
        for my_ingredient in All_Ingredients:
          name = my_ingredient.name
          if name in element:
            good_ingredient = True
        # If the user doesn't have one of the ingredients, its not a good recipe
        if not good_ingredient:
          good_recipe = False
          break # In that case, just break
      # Save a copy of the good recipe to recipe_copy
      if good_recipe:
        if all_recipes[i] not in recipe_copy:
          recipe_copy.append(all_recipes[i])
    return recipe_copy


  def get_timed_recipes(self, time):
    """ Returns recipes with a parameter of under a given cooktime """
    recipes = self.get_useful_recipes()
    timed_recipes = []
    for i in range(len(recipes)):
      if recipes[i]['totalTimeInSeconds'] <= int(time)*60:
        timed_recipes.append(recipes[i])
    return timed_recipes
  
  def get_url(self, ingredient):
    """ Format url for yummly api call """
    for letter in ingredient.name:
      formatted = ingredient.name.replace(' ',"%20")
    url = "http://api.yummly.com/v1/api/recipes?_app_id=c95876fa&requirePictures=true&_app_key=ef0c2016540a55876cffbabe427d6d83&allowedIngredient[]=%s" % (formatted)
    return url

  def get_json(self, url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)  #opens url
    response_text = f.read()  #reads through url
    response_data = json.loads(response_text)  #converts data to json
    return response_data
  
  def get_all_recipes(self, ingredient):
    """ Gets a list of all recipes for a given ingredient """
    recipes = self.db.recipes
    recipe = recipes.find_one({"ingredient": str(ingredient)})
    # Check to see if the list has been memoized, and read it from the db
    if recipe != None:
      return recipe["recipe_list"]
    # Otherwise call url
    elif str(ingredient) == "":
      return []
    else:
      empty_page = 0
      recipe_list = []
      url = self.get_url(ingredient)
      contents_all = self.get_json(url)
      if contents_all['totalMatchCount'] == empty_page:
        print "There is nothing here for ", ingredient.name
      else:
        contents = contents_all['matches']
        recipe_list += contents

      # add list to db and return
      recipes.insert({"ingredient": str(ingredient), 'recipe_list': recipe_list})
      return recipe_list
  
class Ingredient(object):
  """User input ingredients that they have"""
  def __init__(self, ingredient):
    self.name = ingredient

  def __str__(self):
    """ Returns a string of the name """
    return self.name

  
class Shelf(object):
  """ Holds a list of ingredients"""
  def __init__(self):
    self.ingredients = []  #list of ingredient objects
  
  def __str__(self):
    """ Returns a list of the ingredients as a string """
    ingredients = []
    for i in self.ingredients:
        ingredients.append(str(i))
    return str(ingredients)
    
  def make_shelf(self, string):
    """ Adds ingredients to the ingredient list
        Takes in a string of ingredient names separated by commas
        Returns a list of ingredient objects
    """
    ingredients = []
    ingredients_list = string.lower().split(",")
    for name in ingredients_list:
        new_ingredient = Ingredient(name.strip())
        ingredients.append(new_ingredient)
    return ingredients


class Pantry(Shelf):
  """ Extends shelf, is saved for each user """
  def __init__(self, username, db):
    self.username = username
    self.db = db # the database
    self.ingredients = []
    
  def make_pantry(self, ingredients_string):
    """ Call parent function to build pantry """
    self.ingredients = self.make_shelf(ingredients_string)
    
  def save_pantry(self):
    """ Save the Pantry to a database """
    ingredient_info = []
    for ingredient in self.ingredients:
      ingredient_info.append(ingredient.name)
    # Format pantry as json string, so that it can be stored in a database
    user = {"user": self.username, "pantry": str(ingredient_info)}
    users = self.db.users
    # Remove the previously saved pantry, if it exists
    users.remove({"user": self.username})
    users.insert_one(user)
    
class Fridge(Shelf):
  """ List of ingredients that is temporary, not saved with the user """
  def __init__(self):
    self.ingredients = None
    
  def make_fridge(self, ingredients_string):
    """ Call parent function to build fridge """
    self.ingredients = self.make_shelf(ingredients_string)
  
 

#################################### MAIN ############

if __name__ == '__main__':
  # Initialize MongoDB
  # client = MongoClient()
  # db = client.users
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
  
  # Make a new user and pantry
  # current_user = User('bob', db)
  # print current_user.name + "'s saved pantry: ", current_user.get_pantry()
  # current_user.pantry.make_pantry("flour, egg, milk, sugar, salt, butter")
  # current_user.pantry.save_pantry()
  # print current_user.name + "'s new pantry:   ",current_user.pantry
  # print type(current_user.pantry)
  # print type(str(current_user.pantry))

  # Get recipes
  # current_user.fridge.make_fridge("pineapple, flour, butter, milk, salt, eggs, sugar, vanilla, water, chicken, oil, baking soda, baking powder, chocolate, corn starch, corn, chips, brown sugar, coffee, carrots, potatoes, steak, fish, salmon")
  # print current_user.fridge
  # print current_user.get_useful_recipes()

  # Show that databases work
  # new_user = User('bob', db)
  # print new_user.name + "'s saved pantry: ", new_user.get_pantry()

  
  
  
  
  
  
  
