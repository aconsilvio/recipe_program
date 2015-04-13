"""
Recipe Program Skeleton
Anisha, Annabel, Maggie
"""
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pickle import dump, load
from os.path import exists
import pymongo
from pymongo import MongoClient
import ast # This allows for convertion between str to list

class User(object):
  """Class that defines a user with a specific pantry and fridge"""
  def __init__(self, name, db):
    self.name = name
    self.pantry = Pantry(name, db)
    self.fridge = Fridge()
    self.db = db
    
  def __str__(self):
    """Returns the pantry and fridge of user"""
    return self.pantry, self.fridge
  
  def get_name(self):
    print "What is your name?"
    return raw_input()

  def get_pantry(self):
    """ Return the pantry if it exists, or an empty string """
    users = self.db.posts
    user = users.find_one({"user": self.name})
    if user == None:
      # If the pantry is not stored, build it
      return ""
    else:
      # Otherwise, return the pantry
      ingredients = ast.literal_eval(user["ingredients"])
      ingredient_list = []
      for i in ingredients:
          ingredient_list.append(Ingredient(i))
      self.pantry.ingredients = ingredient_list
      return self.pantry

  def get_useful_recipes(self):
    """Generate recipes based on fridge and pantry in RecipePuppy"""

    all_recipes = []
    all_ingredient_names = []
    All_Ingredients = self.fridge.ingredients# + self.pantry.ingredients
    for ingredient in All_Ingredients:
      print ingredient
      all_recipes += (self.get_all_recipes(ingredient))
      all_ingredient_names.append(ingredient.name)

    ##recipe is a dictionary
    recipe_copy = []
    for i in range(len(all_recipes)):
      good_recipe = True
      ingredients = all_recipes[i][u'ingredients']
      for element in ingredients:
        element = element.encode('utf-8')
        good_ingredient = False
        for my_ingredient in all_ingredient_names:
          if my_ingredient in element:
            good_ingredient = True
        if not good_ingredient:
          good_recipe = False
          break
      if good_recipe:
        if all_recipes[i] not in recipe_copy:
          recipe_copy.append(all_recipes[i])
    print recipe_copy
    return recipe_copy

  
  def get_url(self, ingredient):
    """Format url for api call"""
    for letter in ingredient.name:
      formatted = ingredient.name.replace(' ',"%20")
    url = "http://api.yummly.com/v1/api/recipes?_app_id=c95876fa&_app_key=ef0c2016540a55876cffbabe427d6d83&allowedIngredient[]=%s" % (formatted)
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
    empty_page = 0
    recipe_list = []
    url = self.get_url(ingredient)
    contents_all = self.get_json(url)
    if contents_all['totalMatchCount'] == empty_page:
      print "There is nothing here for ", ingredient.name
    else:
      contents = contents_all['matches']
      recipe_list += contents
    return recipe_list  
  
class Ingredient(object):
  """User input ingredients that they have"""
  def __init__(self, ingredient):
    self.name = ingredient
  ##will eventually put in quantity, allergns, etc.

  def __str__(self):
    """ Returns a string of the name """
    return self.name

  
class Shelf(object):
  """ Holds a list of ingredients"""
  def __init__(self):
    self.ingredients = []  #list of ingredient objects
  
  def __str__(self):
    """ Returns a list of the ingredients """
    ingredients = []
    for i in self.ingredients:
        ingredients.append(str(i))
    return str(ingredients)
    
  def make_shelf(self, string):
    """ Adds an Ingredient object to the ingredient list """
##    done = False
##    ingredients = []
##    while not done:
##      print "Add an ingredient. If done, type 'Done'. "
##      name = raw_input().lower()
##      if name == 'done':
##        done = True
##        return ingredients 
##      new_ingredient = Ingredient(name)
##      ingredients.append(new_ingredient)
    ingredients = []
    ingredients_list = string.lower().split(",")
    for name in ingredients_list:
        new_ingredient = Ingredient(name.strip())
        ingredients.append(new_ingredient)
    return ingredients


class Pantry(Shelf):
  def __init__(self, username, db):
    self.username = username
    self.db = db
    self.ingredients = []
    #self.save_pantry()
    
  def make_pantry(self, ingredients_string):
    self.ingredients = self.make_shelf(ingredients_string)
##    # If exits, load
##    filename = self.username + ".txt"
##    if exists(filename):
##      self.ingredients.append(load(open(filename, "r+")))
##      self.edit_pantry()      
##    else:
##      print "Add ingredients to your pantry"
##      return self.make_shelf()
##    # otherwise make new
      
##    users = self.db.posts
##    user = users.find_one({"user": self.username})
##    # If the pantry is not stored, build it
##    if user == None:
##      return self.make_shelf()
##    # Otherwise, load it and ask to update
##    else:
##      # Add the existing pantry
##      #self.ingredients.append(user["ingredients"])
##      # Edit the existing pantry
##      return self.edit_pantry(user["ingredients"])
      
  
##  def make_pantry(self):
##    print "Current Pantry: "
##    print self.ingredients
##    
##    # Make sure response is valid
##    valid_response = False
##    while not valid_response:
##      print "Do you want to edit your pantry? Yes/No"
##      response = raw_input().lower()
##      if response == 'yes' or response == 'no':
##        valid_response = True
##      else:
##        print "Not a valid response. Please type Yes or No."
##    
##    if response == "yes":
##      print "re-enter all ingredients"
##      return self.make_shelf()
##    elif response == "no":
##      return self.ingredients
    
  def save_pantry(self):
    """ Save the Pantry to a database """
    ingredient_info = []
    for ingredient in self.ingredients:
      ingredient_info.append(ingredient.name)
    user = {"user": self.username, "ingredients": str(ingredient_info)}
    users = self.db.posts
    users.remove({"user": self.username})
    users.insert_one(user)
    
    
class Fridge(Shelf):
  def __init__(self):
    self.ingredients = None #self.make_fridge()
    
  def make_fridge(self, ingredients_string):
    #print "Add ingredients to your fridge"
    self.ingredients = self.make_shelf(ingredients_string)
  
 

#################################### MAIN ############

if __name__ == '__main__':
  # Initialize MongoDB
  client = MongoClient()
  db = client.users
  
  # Do user program stuff
  current_user = User('bob', db)
  print current_user.get_pantry()
  current_user.pantry.make_pantry("flour, egg, milk, sugar, salt, butter")
  current_user.pantry.save_pantry()
  print current_user.pantry

  bob = User('bob', db)
  print bob.get_pantry()
  current_user.fridge.make_fridge("flour, egg, milk, sugar, salt, butter")
  current_user.fridge.make_fridge("pineapple, flour, butter, milk, salt, eggs, sugar, vanilla, water, chicken, oil, baking soda, baking powder, chocolate, corn startch, corn, chips, brown sugar, coffee, carrots, potatoes, steak, fish, salmon")
  print current_user.fridge
  #current_user.pantry.make_pantry()
  print current_user.get_useful_recipes()
  
  
  
  
  
  
  
