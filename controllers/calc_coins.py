
import sys

pre_url = "/home/zhecht/bitcoin/"
pre_url = ""
ranks = {
  "xrb": 0,
  "xmr": 1,
  "ven": 2,
  "wabi": 3,
  "xrp": 4,
  "lend": 5,
  "poe": 6,
  "etn": 7,
  "neo": 8,
  "eng": 9,
  "req": 10,
  "ark": 11,
  "bnty": 12,
  "dbc": 13,
  "gvt": 14,
  "omg": 15,
  "mod": 16,
  "snm": 17,
  "powr": 18,
  "qtum": 19,
  "ost": 20,
  "btg": 21,
  "brd": 22,
  "eth": 23
}


def get_arr():
  all_coins = []
  for coin in ranks:
    all_coins.append({"id": coin, "amt": 0, "btc_price": 0, "eth_price": 0, "btc_sold_price": 0, "eth_sold_price": 0})
  return all_coins

if __name__ == '__main__':
  who = "zack"
  if len(sys.argv) > 1:
    who = sys.argv[1]

  with open(pre_url+"static/%s/OrderHistory.csv" % who) as f:
    content = f.readlines()
  content = [x.strip() for x in content]
  
  all_coins = get_arr()
  #all_coins[ranks["eth"]]["id"] = "eth"
  #all_coins["eth"] = {"id": "eth", "amt": 0, "btc_price": 0, "eth_price": 0}
  #all_coins["btc"] = {"id": "btc", "amt": 0, "btc_price": 0, "eth_price": 0}
  for line in content[1:]:
    split_line = line.split(",")
    if split_line[-1] == "Filled" and split_line[0] != "":
      altcoin = split_line[1][:-3]
      base_coin = split_line[1][-3:]
      buy_sell = split_line[2]
      price = float(split_line[-2])
      amt = float(split_line[4])
      try:
        #all_coins[ranks[altcoin.lower()]]["id"] = altcoin.lower()
        if buy_sell == "BUY":
          all_coins[ranks[altcoin.lower()]]["amt"] += amt
          all_coins[ranks[altcoin.lower()]][base_coin.lower()+"_price"] += price
        else:
          all_coins[ranks[altcoin.lower()]]["amt"] -= amt
          all_coins[ranks[altcoin.lower()]][base_coin.lower()+"_sold_price"] += price
           #all_coins[altcoin.lower()][base_coin.lower()+"_price"] -= price
      except:
        nothing = 0
      
       
  
  #end content
  f = open(pre_url+"static/%s/coins1.txt" % who, "w")
  for coin in all_coins:
    name = coin["id"]
    rank = ranks[name]
    if who == "zack" and (name == "btc" or name == "icx" or name == "xvg" or name == "ada" or name == "ltc" or name == "trx"):
      nothing = 0
    else:
      amt = str(all_coins[rank]["amt"])
      btc = str(all_coins[rank]["btc_price"])
      eth = str(all_coins[rank]["eth_price"])
      btc_sold = str(all_coins[rank]["btc_sold_price"])
      eth_sold = str(all_coins[rank]["eth_sold_price"])
      f.write(name+' '+amt+' '+btc+' '+eth+' '+btc_sold+' '+eth_sold+'\n')
  f.close()




