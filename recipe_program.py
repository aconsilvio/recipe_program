"""
Recipe Program Skeleton
Anisha, Annabel, Maggie
"""
import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pickle import dump, load
from os.path import exists

class User(object):
  """Class that defines a user with a specific pantry and fridge"""
  def __init__(self):
    self.name = self.get_name()
    self.pantry = Pantry(self.name)
    self.fridge = Fridge()
    
  def __str__(self):
    """Returns the pantry and fridge of user"""
    return self.pantry, self.fridge
  
  def get_name(self):
    print "What is your name?"
    return raw_input()

  def get_useful_recipes(self):
    """Generate recipes based on fridge and pantry in RecipePuppy"""
   #  # Make search term
   #  # get all recipes
   #  # Format url
   #  url = self.get_url()

   # # Call list
   #  recipe_list = self.get_recipe_list(url)
   #  # Get rid of bad recipes
   #  good_recipes = self.filter_recipes(recipe_list)
   #  pass
    all_recipes = []
    all_ingredient_names = []
    All_Ingredients = self.fridge.ingredients + self.pantry.ingredients
    for ingredient in All_Ingredients:
      all_recipes += (self.get_all_recipes(ingredient))
      all_ingredient_names.append(ingredient.name)

    ##recipe is a dictionary
    recipe_copy = []
    #recipe_copy.extend(all_recipes)
    for i in range(len(all_recipes)):
      good_recipe = True
      ingredients = all_recipes[i][u'ingredients']
      print ingredients
      for element in ingredients:
        element = element.encode('utf-8')
        if element not in all_ingredient_names:
          print element
          good_recipe = False
          #recipe_copy.remove(all_recipes[i])
          break  #after recipe is removed, stop searching ingredient list
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
      print "There is nothing here for ", ingredient
    else:
      contents = contents_all['matches']
      print contents
      recipe_list += contents
    return recipe_list

  
  
class Ingredient(object):
  """User input ingredients that they have"""
  def __init__(self, ingredient):
    self.name = ingredient
  ##will eventually put in quantity, allergns, etc.

  
class Shelf(object):
  """ Holds a list of ingredients"""
  def __init__(self):
    self.ingredients = []  #list of ingredient objects
  
  def __str__(self):
    """ Returns a list of the ingredients """
    return self.ingredients
    
  def make_shelf(self):
    """ Adds an Ingredient object to the ingredient list """
    done = False
    ingredients = []
    while not done:
      print "Add an ingredient. If done, type 'Done'. "
      name = raw_input().lower()
      if name == 'done':
        done = True
        return ingredients 
      new_ingredient = Ingredient(name)
      ingredients.append(new_ingredient)


class Pantry(Shelf):
  def __init__(self, username):
    self.username = username
    self.ingredients = self.make_pantry()
    
  def make_pantry(self):
    # If exits, load
    filename = self.username + ".txt"
    if exists(filename):
      self.ingredients.append(load(open(filename, "r+")))
      self.edit_pantry()      
    else:
      print "Add ingredients to your pantry"
      return self.make_shelf()
    # otherwise make new
  
  def edit_pantry(self):
    print "Current Pantry: "
    print self.ingredients
    
    # Make sure response is valid
    valid_response = False
    while not valid_response:
      print "Do you want to edit your pantry? Yes/No"
      response = raw_input().lower()
      if response == 'yes' or response == 'no':
        valid_response = True
    
    if response == "yes":
      self.make_shelf()
    elif response == "no":
      return
    else:
      print "Not a valid response. Please type Yes or No."

    
class Fridge(Shelf):
  def __init__(self):
    self.ingredients = self.make_fridge()
    
  def make_fridge(self):
    print "Add ingredients to your fridge"
    return self.make_shelf()
  
 
  
  #################################### MAIN ############

if __name__ == '__main__':
  current_user = User()
  current_user.get_useful_recipes()
  
  
  
  
  
  
  
