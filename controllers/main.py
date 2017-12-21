from flask import *
import json
from bs4 import BeautifulSoup as BS
try:
  import urllib2 as urllib
except:
  import urllib.request as urllib

main = Blueprint('main', __name__, template_folder='views')

owned = [
  "btc", 0.03270468,
  "eth", 0.24861740,
  "ltc", 0.56849907,
  "req", 197.802,
  #"wabi", 14.985,
  "xrp", 41.958,
  #"neo", .00955,
  #"icx", 5,
  #"vet", 18.966,
  #"qtum", 0.00872,
  #"eng", 23.976,
  "trx", 999.999,
  "ost", 164.835
]

owned_dict = {
  "btc": 0.03270468,
  "eth": 0.24861740,
  "ltc": 0.56849907,
  "req": 197.802,
  #"wabi": 14.985,
  "xrp": 41.958,
  #"neo": .00955,
  #"icx": 5,
  #"vet": 18.966,
  #"qtum": 0.00872,
  #"eng": 23.976,
  "trx": 999.999,
  "ost": 164.835
}

full_names = {
  "btc": "bitcoin",
  "eth": "ethereum",
  "ltc": "litecoin",
  "req": "request-network",
  #"wabi": "wabi",
  "xrp": "ripple",
  #"neo": "neo",
  #"icx": "icon",
  #"vet": "vechain",
  #"qtum": "qtum",
  #"eng": "enigma-project",
  "trx": "tron",
  "ost": "simple-token"
}


@main.route('/')
def main_route():
  coin_row = []
  for coin in owned_dict:
    #print(i, owned[i])
    coin_row.append({"id": coin, "amt": owned_dict[coin]})
  return render_template("main.html",owned=owned_dict,coin_rows=coin_row)

@main.route('/price')
def price_route():
  arr = {}
  url = "https://coinmarketcap.com/all/views/all/"
  soup = BS(urllib.urlopen(url).read(), "lxml")

  for coin in owned_dict:
    full_id = "id-"+full_names[coin]
    row = soup.find("tr", {"id": full_id})
    #row = coin.find_all("tr", id=full_id)
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