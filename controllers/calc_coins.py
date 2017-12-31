
import sys

pre_url = "/home/zhecht/bitcoin/"
pre_url = ""

if __name__ == '__main__':
  who = "zack"
  if len(sys.argv) > 1:
    who = sys.argv[1]

  with open(pre_url+"static/%s/OrderHistory.csv" % who) as f:
    content = f.readlines()
  content = [x.strip() for x in content]
  
  all_coins = {}
  all_coins["eth"] = {"id": "eth", "amt": 0, "btc_price": 0, "eth_price": 0}
  all_coins["btc"] = {"id": "btc", "amt": 0, "btc_price": 0, "eth_price": 0}
  for line in content[1:]:
    split_line = line.split(",")
    if split_line[-1] == "Filled" and split_line[0] != "":
      altcoin = split_line[1][:-3]
      base_coin = split_line[1][-3:]
      buy_sell = split_line[2]
      price = float(split_line[-2])
      amt = float(split_line[4])
      if altcoin.lower() not in all_coins:
        all_coins[altcoin.lower()] = {
          "id": altcoin.lower(),
          "amt": 0.0,
          "btc_price": 0.0,
          "eth_price": 0.0,
          "btc_sold_price": 0.0,
          "eth_sold_price": 0.0
        }
      if buy_sell == "BUY":
        all_coins[altcoin.lower()]["amt"] += amt
        all_coins[altcoin.lower()][base_coin.lower()+"_price"] += price
      else:
        all_coins[altcoin.lower()]["amt"] -= amt
        #all_coins[altcoin.lower()][base_coin.lower()+"_sold_price"] += price
        all_coins[altcoin.lower()][base_coin.lower()+"_price"] -= price
  
  #end content
  f = open(pre_url+"static/%s/coins.txt" % who, "w")
  for coin in all_coins:
    if who == "zack" and (coin == "btc" or coin == "icx" or coin == "xvg" or coin == "ada" or coin == "ltc" or coin == "trx"):
      nothing = 0
    else:
      amt = str(all_coins[coin]["amt"])
      btc = str(all_coins[coin]["btc_price"])
      eth = str(all_coins[coin]["eth_price"])
      btc_sold = str(all_coins[coin]["btc_price"])
      eth_sold = str(all_coins[coin]["eth_price"])
      f.write(coin+' '+amt+' '+btc+' '+eth+' '+btc_sold+' '+eth_sold+'\n')
  f.close()




