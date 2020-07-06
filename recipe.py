from bs4 import BeautifulSoup
import re
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from datetime import date

today = date.today()

recipe = ""

#Get Website
r1 = requests.get("https://spoonacular.com/")
page = BeautifulSoup(r1.text, 'html.parser')

#Get Recipe Of The Day
rotd = page.find('div', attrs={'id': re.compile('recipeOfTheDay')})
children = rotd.findChildren('a', recursive=False)

#Cycle Through And Print href
for a in children[0:1]: 
    print("https://spoonacular.com{}".format(a.get('href')))
