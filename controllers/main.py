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
  "neo": "neo",
  "icx": "icon",
  "iota": "iota",
  "vet": "vechain",
  "qtum": "qtum",
  "eng": "enigma-project",
  "snm": "sonm",
  "trx": "tron",
  "ost": "simple-token",
  "lend": "ethlend",
  "powr": "power-ledger",
  "ven": "vechain",
  "elf": "aelf",
  "ada": "cardano",
  "btg": "bitcoin-gold",
  "brd": "bread",
  "gvt": "genesis-vision",
  "xmr": "monero",
  "omg": "omisego",
  "mod": "modum",
  "poe": "poet",
  "ark": "ark"
}

pre_url = "/home/zhecht/bitcoin/"
#pre_url = ""

def get_owned(who):

  first_letter = who[0].upper()
  coin_rows = []
  with open(pre_url+"static/%s/coins.txt" % who) as f:
    content = f.readlines()
  content = [x.strip() for x in content]

  for i in range(0,len(content)):
    split_line = content[i].split(" ")
    coin_rows.append(split_line[0])
  return coin_rows

def convert_eth_btc(eth):
  client = Client(constants.API_KEY, constants.SECRET)
  res = client.get_symbol_ticker(symbol="ETHBTC")
  return eth*float(res["price"])

def convert_btc_eth(btc):
  client = Client(constants.API_KEY, constants.SECRET)
  res = client.get_symbol_ticker(symbol="BTCETH")
  return btc*float(res["price"])

def get_row_amts(who):
  #who is zack,jimmy,nick
  first_letter = who[0].upper()
  coin_rows = []
  with open(pre_url+"static/%s/coins.txt" % who) as f:
    content = f.readlines()
  content = [x.strip() for x in content]

  for i in range(0,len(content)):
    split_line = content[i].split(" ")
    coin_rows.append({"id": split_line[0], "amt": float(split_line[1])})
  return coin_rows

def get_rows(who):
  #who is zack,jimmy,nick
  first_letter = who[0].upper()
  coin_rows = []
  with open(pre_url+"static/%s/coins.txt" % who) as f:
    content = f.readlines()
  content = [x.strip() for x in content]

  for i in range(0,len(content)):
    split_line = content[i].split(" ")
    btc_price = float(split_line[2])
    eth_price = float(split_line[3])
    eth_in_btc = convert_eth_btc(eth_price)
    btc_in_eth = convert_btc_eth(btc_price)

    btc_price += eth_in_btc
    eth_price += btc_in_eth
    coin_rows.append({"id": split_line[0], "amt": float(split_line[1]), "bought": eth_price})
  return coin_rows

def get_price_dict(price_list):
  price_dict = {}
  for price in price_list:
    price_dict[price["symbol"]] = price["price"]
  return price_dict 

@main.route('/<name>')
def main_route(name):
  if name == "rhcp_favicon.png":
    return
  if name == "":
    name = "zack"
  coin_rows = get_rows(name)
  return render_template("main.html",coin_rows=coin_rows)

@main.route('/<name>/arrays')
def array_route(name):
  coin_rows = get_rows(name)
  return jsonify(coin_rows)

@main.route('/<name>/price')
def price_route(name):
  if name == "rhcp_favicon.png":
    return
  client = Client(constants.API_KEY, constants.SECRET)
  prices = get_price_dict(client.get_all_tickers())

  owned = get_owned(name)
  coin_rows = get_rows(name)
  arr = {}
  url = "https://coinmarketcap.com/all/views/all/"
  soup = BS(urllib.urlopen(url).read(), "lxml")

  #print(owned)
  #row = soup.find("tr", {"id": "id-bitcoin"})
  #val = row.find("a", class_="price")
  #eth_row = soup.find("tr", {"id": "id-ethereum"})
  #eth = eth_row.find("a", class_="price")
  btc_price = float(prices["BTCUSDT"])
  eth_usdt_price = float(prices["ETHUSDT"])

  #btc_price = float(val.text[1:])
  #eth_price = float(val.text[1:])
  for coin in owned:
    full_id = "id-"+full_names[coin]
    row = soup.find("tr", {"id": full_id})
    val = row.find("a", class_="price")
    all_tds = row.find_all("td")
    market_cap = all_tds[3].text.strip()
    inc_dec = all_tds[-2].text
    inc_dec_1h = all_tds[-3].text
    inc_dec_7d = all_tds[-1].text
    
    
    key = coin.upper()+"BTC"
    if coin == "btc":
      price = float(val.text[1:])
    elif coin == "eth":
      price = float(prices[coin.upper()+"BTC"])
    elif coin == "vet":
      price = float(prices["VENBTC"])
      eth_price = float(prices["VENETH"])
    else:
      price = float(prices[coin.upper()+"BTC"])
      eth_price = float(prices[coin.upper()+"ETH"])

    usd_price = btc_price
    if coin != "btc":
      usd_price = price * btc_price
    arr[coin] = {
      "curr_btc_price": float("{0:.4f}".format(btc_price)),
      "curr_eth_price": float("{0:.4f}".format(curr_eth_price)),
      "price": float("{0:.4f}".format(usd_price)),
      "eth_price": float("{0:.8f}".format(eth_price)),
      "btc_price": float("{0:.8f}".format(price)),
      "cap": market_cap,
      "24h": inc_dec,
      "1h": inc_dec_1h,
      "7d": inc_dec_7d
    }

  #print(arr)
  return jsonify(arr)
