import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
from pickle import dump, load
from os.path import exists
from pprint import pprint


data = {"title":"Recipe Puppy","version":0.1,"href":"http:\/\/www.recipepuppy.com\/","results":[{"title":"Homemade Chicken Nuggets \r\n\t\t\n","href":"http:\/\/www.kraftfoods.com\/kf\/recipes\/homemade-chicken-nuggets-52664.aspx","ingredients":"chicken, chicken","thumbnail":"http:\/\/img.recipepuppy.com\/602473.jpg"},{"title":"Chicken Fingers \r\n\t\t\n","href":"http:\/\/www.kraftfoods.com\/kf\/recipes\/chicken-fingers-106219.aspx","ingredients":"chicken, chicken","thumbnail":"http:\/\/img.recipepuppy.com\/603792.jpg"},{"title":"Roast Chicken \r\n\t\t\r\n\t\r\n\t\t\r\n\t\r\n\t\r\n\r\n","href":"http:\/\/www.kraftfoods.com\/kf\/recipes\/roast-chicken-66318.aspx","ingredients":"chicken, chicken","thumbnail":"http:\/\/img.recipepuppy.com\/632814.jpg"},{"title":"Homemade Chicken Nuggets \r\n\t\t\n","href":"http:\/\/www.kraftfoods.com\/kf\/recipes\/homemade-chicken-nuggets-52664.aspx?cm_re=1-_-1-_-RecipeAlsoEnjoy","ingredients":"chicken, chicken","thumbnail":"http:\/\/img.recipepuppy.com\/664229.jpg"},{"title":"Charcoal Grilled Chicken Breast","href":"http:\/\/www.recipezaar.com\/Charcoal-Grilled-Chicken-Breast-322478","ingredients":"chicken","thumbnail":"http:\/\/img.recipepuppy.com\/286695.jpg"},{"title":"Cheesy Tomato Basil Chicken Breasts","href":"http:\/\/www.recipezaar.com\/Cheesy-Tomato-Basil-Chicken-Breasts-54133","ingredients":"chicken","thumbnail":"http:\/\/img.recipepuppy.com\/290542.jpg"},{"title":"Chicken Supreme Kiev-Style","href":"http:\/\/www.recipezaar.com\/Chicken-Supreme-Kiev-Style-175757","ingredients":"chicken","thumbnail":"http:\/\/img.recipepuppy.com\/299077.jpg"},{"title":"Chicken Thighs in a Mango Curry Marinade","href":"http:\/\/www.recipezaar.com\/Chicken-Thighs-in-a-Mango-Curry-Marinade-310062","ingredients":"chicken","thumbnail":"http:\/\/img.recipepuppy.com\/299300.jpg"},{"title":"Chicken Thighs in Asian Tangerine Marinade","href":"http:\/\/www.recipezaar.com\/Chicken-Thighs-in-Asian-Tangerine-Marinade-215200","ingredients":"chicken","thumbnail":"http:\/\/img.recipepuppy.com\/299358.jpg"},{"title":"Chicken Tikka Masala","href":"http:\/\/www.recipezaar.com\/Chicken-Tikka-Masala-236996","ingredients":"chicken","thumbnail":"http:\/\/img.recipepuppy.com\/299449.jpg"}]}


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)  #opens url
    response_text = f.read()  #reads through url
    response_data = json.loads(response_text)  #converts data to json
    results = response_data["results"]
    return results


print get_json("http://www.recipepuppy.com/api/?i=chicken&p=1")