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
  "ark": "ark",
  "xrb": "raiblocks",
  "dbc": "deepbrain-chain",
  "bnty": "bounty0x",
  "etn": "electroneum"
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

def get_eth_btc():
  client = Client(constants.API_KEY, constants.SECRET)
  res = client.get_symbol_ticker(symbol="ETHBTC")
  return float(res["price"])

def convert_eth_btc(eth):
  price = get_eth_btc()
  return eth*price


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

  client = Client(constants.API_KEY, constants.SECRET)
  res = client.get_symbol_ticker(symbol="ETHBTC")
  eth_btc = float(res["price"])
  btc_eth = 1.0 / eth_btc

  for i in range(0,len(content)):
    split_line = content[i].split(" ")
    btc_price = float(split_line[2])
    eth_price = float(split_line[3])
    btc_sold_price = float(split_line[4])
    eth_sold_price = float(split_line[5])
    eth_in_btc = eth_price * eth_btc
    btc_in_eth = btc_price * btc_eth
    btc_sold_in_eth = btc_sold_price * btc_eth

    btc_price += eth_in_btc
    eth_price += btc_in_eth
    eth_sold_price += btc_sold_in_eth
    coin_rows.append({"id": split_line[0], "full": full_names[split_line[0]], "amt": float(split_line[1]), "bought": eth_price, "sold": eth_sold_price})
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
  res = client.get_symbol_ticker(symbol="ETHBTC")
  eth_btc = float(res["price"])
  btc_eth = 1.0 / eth_btc

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
  curr_eth_price = float(prices["ETHUSDT"])

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
    elif coin == "dbc" or coin == "bnty" or coin == "xrb" or coin == "etn":
      price = float(all_tds[4].find("a").get("data-btc"))
      eth_price = btc_eth * price
    else:
      price = float(prices[coin.upper()+"BTC"])
      eth_price = float(prices[coin.upper()+"ETH"])

    usd_price = curr_eth_price
    if coin != "eth":
      usd_price = eth_price * curr_eth_price
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
