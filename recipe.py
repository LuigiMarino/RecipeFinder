from bs4 import BeautifulSoup
import re
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from datetime import date

#This needs cleaning up and commenting
#First run through is just to get a working program
#Second will be to organise and neaten
#Current Issues - 
#   Name only gets the first line
#   Link gets OneNote to Grab all page information in a stupid format
#   Formatting can be wonk

today = date.today()

ingredients = ""
method = ""
recipe = ""
msg = ""

#Get Website
r1 = requests.get("https://spoonacular.com/")
page1 = BeautifulSoup(r1.text, 'html.parser')

#Get Recipe Of The Day
rotdDiv = page1.find('div', attrs={'id': re.compile('recipeOfTheDay')})
rotdA = rotdDiv.findChildren('a', recursive=False)

#Cycle Through And Print href
for a in rotdA[0:1]: 
    rotdLink = ("https://spoonacular.com{}".format(a.get('href')))
    rotdName = (a.text.strip())

r2 = requests.get(rotdLink)
page2 = BeautifulSoup(r2.text, 'html.parser')

ingredientsList = page2.find_all('div', attrs={'class': 'spoonacular-ingredient-list'})

i = 1
for a in ingredientsList:
    ingredientsName = a.findChildren('div', attrs={'class' : 'spoonacular-name'})
    ingredientsAmount = a.findChildren('div', attrs={'class' : 'spoonacular-amount spoonacular-metric'})
    for b in ingredientsName:
        name = (b.text)
    for c in ingredientsAmount:
        amount = (c.text)
    ingredients += ("%s - %s\n"%(name,amount))

recipeMethod = page2.findChildren('div', attrs={'class' : 'recipeInstructions'})

for a in recipeMethod:
    method = (a.text)
    method += "\n"

recipe += rotdName + "\n\n" + rotdLink[8:] + "\n\n" + ingredients + "\n" + method
#print(recipe)

#User Details
gmail_user = 'emails@luigi-marino.com'
gmail_password = '*7gMaH1aGf31'
sent_from = gmail_user
to = ['me@onenote.com']

#Email Subject
msg = 'Subject: @Recipes' + "\n"

#Add news to email message
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
