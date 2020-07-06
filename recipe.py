from bs4 import BeautifulSoup
import re
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from datetime import date

#This needs cleaning up and commenting

#Get Todays Date
today = date.today()

#String Variables
name = ""
ingredients = ""
method = ""
nutrition = ""
recipe = ""
msg = ""

#Get Website Homepage
r1 = requests.get("https://spoonacular.com/")
page1 = BeautifulSoup(r1.text, 'html.parser')

#Get Recipe Of The Day and Link
rotdDiv = page1.find('div', attrs={'id': re.compile('recipeOfTheDay')})
rotdA = rotdDiv.findChildren('a', recursive=False)
for a in rotdA[0:1]: 
    rotdLink = ("https://spoonacular.com{}".format(a.get('href')))

#Get ROTD Page
r2 = requests.get(rotdLink)
page2 = BeautifulSoup(r2.text, 'html.parser')

#Get ROTD Page Information
rotdName = page2.title.string
recipeIngredients = page2.find_all('div', attrs={'class': 'spoonacular-ingredient-list'})
recipeMethod = page2.findChildren('div', attrs={'class' : 'recipeInstructions'})
recipeNutrition = page2.findChildren('div', attrs={'class' : 'spoonacular-quickview'})

#Get Ingredients List
for a in recipeIngredients:
    ingredientsName = a.findChildren('div', attrs={'class' : 'spoonacular-name'})
    ingredientsAmount = a.findChildren('div', attrs={'class' : 'spoonacular-amount spoonacular-metric'})
    for b in ingredientsName:
        name = (b.text)
    for c in ingredientsAmount:
        amount = (c.text)
    ingredients += ("%s - %s\n"%(name,amount))

#Get Instructions List
for a in recipeMethod:
    method = (a.text)
    method += "\n"

for a in recipeNutrition:
    nutrition += ((a.text)+'\n')

#Combine All Parts Into Recipe
recipe += rotdName + "\n\n" + rotdLink[8:] + "\n\n" + ingredients + "\n" + method + "\n" + nutrition

#User Details
gmail_user = 'emails@luigi-marino.com'
gmail_password = '*7gMaH1aGf31'
sent_from = gmail_user
to = ['me@onenote.com']

#Email Subject
msg = 'Subject: @Recipes' + "\n"

#Add Recipe to email message
msg += recipe

#Try block for sending email
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, msg)
    server.close

    print ('Email Sent!')
except:
    print ('Something went wrong')
