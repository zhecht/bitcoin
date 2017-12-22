from flask import *
import json
from bs4 import BeautifulSoup as BS
try:
  import urllib2 as urllib
except:
  import urllib.request as urllib

main = Blueprint('main', __name__, template_folder='views')

owned = [
  "btc", 0.01845468,
  "eth", 0.24861740,
  "ltc", 0.56849907,
  "req", 197.802,
  "wabi", 29.956,
  "xrp", 81.93,
  #"neo", .00955,
  #"icx", 5,
  "vet", 34.932,
  #"qtum", 0.00872,
  #"eng", 23.976,
  "trx", 999.999,
  "ost", 164.835
]

owned_dict = {
  "btc": 0.01845468,
  "eth": 0.24861740,
  "ltc": 0.56849907,
  "req": 197.802,
  "wabi": 29.956,
  "xrp": 81.93,
  #"neo": .00955,
  #"icx": 5,
  "vet": 34.932,
  #"qtum": 0.00872,
  #"eng": 23.976,
  "trx": 999.999,
  "ost": 164.835
}

nick_owned_dict = {
  "trx": 397.602,
  "xrp": 23.976
}

full_names = {
  "btc": "bitcoin",
  "eth": "ethereum",
  "ltc": "litecoin",
  "req": "request-network",
  "wabi": "wabi",
  "xrp": "ripple",
  #"neo": "neo",
  #"icx": "icon",
  "iota": "iota",
  "vet": "vechain",
  #"qtum": "qtum",
  #"eng": "enigma-project",
  "trx": "tron",
  "ost": "simple-token"
}

def get_owned(who):
  first_letter = who[0].upper()
  coin_rows = []
  with open("coins.txt") as f:
    content = f.readlines()
  content = [x.strip() for x in content]

  for i in range(0,len(content)):
    split_line = content[i].split(" ")
    if split_line[0] == first_letter:
      total_coins = int(split_line[1])
      for j in range(0,total_coins):
        split_line = content[i+1+j].split(" ")

        coin_rows.append(split_line[0])
      return coin_rows
  return coin_rows

def get_rows(who):
  #who is zack,jimmy,nick
  first_letter = who[0].upper()
  coin_rows = []
  with open("coins.txt") as f:
    content = f.readlines()
  content = [x.strip() for x in content]

  for i in range(0,len(content)):
    split_line = content[i].split(" ")
    if split_line[0] == first_letter:
      total_coins = int(split_line[1])
      for j in range(0,total_coins):
        split_line = content[i+1+j].split(" ")
        if who == "jimmy":
          bought = 0
        else:
          print(split_line)
          bought = float(split_line[2])

        coin_rows.append({"id": split_line[0], "amt": float(split_line[1]), "bought": bought})
      return coin_rows
  return coin_rows

@main.route('/<name>')
def main_route(name):
  if name == "":
    name = "zack"
  coin_rows = get_rows(name)
  return render_template("main.html",owned=owned_dict,coin_rows=coin_rows)


@main.route('/<name>/price')
def price_route(name):
  owned = get_owned(name)
  arr = {}
  url = "https://coinmarketcap.com/all/views/all/"
  soup = BS(urllib.urlopen(url).read(), "lxml")

  #print(owned)
  for coin in owned:
    full_id = "id-"+full_names[coin]
    row = soup.find("tr", {"id": full_id})
    val = row.find("a", class_="price")
    inc_dec = row.find("td", class_="percent-24h").text
    inc_dec_1h = row.find("td", class_="percent-1h").text
    arr[coin] = {
      "price": float(val.text[1:]),
      "24h": inc_dec,
      "1h": inc_dec_1h,
    }

  #print(arr)
  return jsonify(arr)
