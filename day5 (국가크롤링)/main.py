import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

countries = []
max_index = 0

# save crawled data in countries array
for tr in soup.find_all("tr"):
  # country array has to be ---> [ max_index, country_name, currency, code, number ]
  # country_name has to be capitalize 
  country = tr.text.split("\n")
  if country[3] != "":
    country = country[:-1]
    country[0] = max_index
    country[1] = country[1].lower().capitalize()   
    countries.append(country)
    max_index = max_index + 1
countries = countries[1:]

# print all countries
print("Hello! Please choose select a country by number:")
for country in countries:
  print("#",country[0],country[1])

# print datas
flag=True
while(flag):
  try:
    choosenNumber = int(input("#: "))
    if (choosenNumber > 0) and (choosenNumber < max_index):
      choosenCountry = choosenNumber-1
      print("You choose",countries[choosenCountry][1])
      print("The currency code is",countries[choosenCountry][3])
      flag=False
    else:
      print("Choose a number from the list.")
  except:   
    print("That wasn't a number.")
