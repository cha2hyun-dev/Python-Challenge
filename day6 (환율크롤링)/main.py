import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

url = "https://www.iban.com/currency-codes"
countries = []

request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")[1:]
for row in rows:
  items = row.find_all("td")
  name = items[0].text
  code =items[2].text
  if name and code:
    if name != "No universal currency":
      country = {
        'name':name.capitalize(),
        'code': code
      }
      countries.append(country)

# I couldnt scrape converted value because it is rendered by js so i did it as 2 way
# First scrape rate and multiple with sourceCurrency.
def convert(sourceCurrency, targetCurrency, sendAmount):
  apiurl = "https://transferwise.com/gb/currency-converter/{0}-to-{1}-rate?amount={2}".format(sourceCurrency, targetCurrency, sendAmount)
  request = requests.get(apiurl)
  soup = BeautifulSoup(request.text, "html.parser")
  currency_rate = float(soup.find("span", attrs={"class":"text-success"}).get_text())
  convertedAmount = sendAmount * currency_rate
  sendAmount = format(sendAmount, ",.2f")
  convertedAmount = format_currency(convertedAmount, "KRW", locale="ko_KR")
  print("{0}{1} is {2}".format(sourceCurrency, sendAmount, convertedAmount))
  
  
# Second hit the api directly and received value as json.
def convertWithJson(sourceCurrency, targetCurrency, sendAmount):
  apiurl = "https://api.transferwise.com/v3/comparisons?sourceCurrency={0}&targetCurrency={1}&sendAmount={2}".format(sourceCurrency, targetCurrency, sendAmount)
  request = requests.get(apiurl)
  result = request.text
  print(result)
  

def ask():
  try:
    choice = int(input("#: "))
    if choice > len(countries):
      print("Choose a number from the list.")
      ask()
    else:
      country = countries[choice]
      print(country['name'],"\n")
      return country['code']
  except ValueError:
    print("That wasn't a number.")
    ask()


print("Welcome to CurrencyConvert PRO 2000\n")
for index, country in enumerate(countries):
  print(f"#{index} {country['name']}")

print("\nWhere are you frome? Choose a country by number.\n")
sourceCurrency = ask()

print("Now choose another country.\n")
targetCurrency = ask()

print(f"How many {sourceCurrency} do you want to convert to {targetCurrency} ?")
sendAmount = int(input())

convert(sourceCurrency, targetCurrency, sendAmount)
#convertWithJson(sourceCurrency, targetCurrency, sendAmount)

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

