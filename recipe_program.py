"""
Recipe Program Skeleton
Anisha, Annabel, Maggie
"""

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
    self.name = raw_input()

  def get_recipes(self):
    """Generate recipes based on fridge and pantry in RecipePuppy"""
    # Make search term


    # get all recipes
    
    # 
    pass

  
class Shelf(object):
  """ Holds a list of ingredients    
  """
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
      name = raw_input()
      if name == 'Done':
        done = True
      ingredients.append(Ingredient(name))
    return ingredients
    pass  


class Pantry(Shelf):
  def __init__(self, username):
    self.username = username
    self.ingredients = make_pantry()
    
  def make_pantry(self):
    # If exits, load
    filename = self.username + ".txt"
    if exists(filename):
      self.ingredients.append(load(open(filename, "r+")))
      self.edit_pantry()      
    else:
      self.ingredients = make_shelf()
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
    self.ingredients = make_shelf()
    

class 
Ingredient(object):
  """User input ingredients that they have"""
  def __init__(self, ingredient):
    self.name = ingredient
  ##will eventually put in quantity, allergns, etc.
  
 
  
  #################################### MAIN ############

  if __name__ == '__main__':
    current_user = User()
    current_user.get_recipes()
  
  
  
  
  
  
  
