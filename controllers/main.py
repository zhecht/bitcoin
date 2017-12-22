from flask import *
import json
from bs4 import BeautifulSoup as BS
from binance.client import Client
try:
  import controllers.constants as constants
except:
  import constants
try:
  import urllib2 as urllib
except:
  import urllib.request as urllib

main = Blueprint('main', __name__, template_folder='views')

#eth 0.24861740 804.45

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
  "snm": "sonm",
  "trx": "tron",
  "ost": "simple-token"
}

pre_url = "/home/zhecht/bitcoin/"
#pre_url = ""

def get_owned(who):
  first_letter = who[0].upper()
  coin_rows = []
  with open(pre_url+"coins.txt") as f:
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
  with open(pre_url+"coins.txt") as f:
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

def get_price_dict(price_list):
  price_dict = {}
  for price in price_list:
    price_dict[price["symbol"]] = price["price"]
  return price_dict 

@main.route('/<name>')
def main_route(name):
  if name == "":
    name = "zack"
  coin_rows = get_rows(name)
  return render_template("main.html",coin_rows=coin_rows)


@main.route('/<name>/price')
def price_route(name):
  client = Client(constants.API_KEY, constants.SECRET)
  prices = get_price_dict(client.get_all_tickers())

  owned = get_owned(name)
  arr = {}
  url = "https://coinmarketcap.com/all/views/all/"
  soup = BS(urllib.urlopen(url).read(), "lxml")

  #print(owned)
  row = soup.find("tr", {"id": "id-bitcoin"})
  val = row.find("a", class_="price")
  btc_price = float(val.text[1:])
  for coin in owned:
    full_id = "id-"+full_names[coin]
    row = soup.find("tr", {"id": full_id})
    val = row.find("a", class_="price")
    inc_dec = row.find("td", class_="percent-24h").text
    inc_dec_1h = row.find("td", class_="percent-1h").text
    key = coin.upper()+"BTC"
    if coin == "btc":
      price = float(val.text[1:])
    elif coin == "eth":
      price = float(prices[coin.upper()+"BTC"])*btc_price
    elif coin == "vet":
      price = float(prices["VENBTC"])*btc_price
    else:
      price = float(prices[coin.upper()+"BTC"])*btc_price
    arr[coin] = {
      "price": float("{0:.4f}".format(price)),
      "24h": inc_dec,
      "1h": inc_dec_1h,
    }

  #print(arr)
  return jsonify(arr)
