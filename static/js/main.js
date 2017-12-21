
coins = [
  "btc",
  "eth",
  "ltc",
  "req",
  "wabi",
  "neo",
  //"icx",
  "vet",
  "qtum",
  "eng",
  "trx",
  "ost"
]

owned = {
  "btc": 0.03270468,
  "eth": 0.24861740,
  "ltc": 0.56849907,
  "req": 197.802,
  "wabi": 14.985,
  "neo": .00955,
  //"icx": 5,
  "vet": 18.966,
  "qtum": 0.00872,
  "eng": 23.976,
  "trx": 742.257,
  "ost": 123.876
}

bought = {
  "btc": 18345.99,
  "eth": 804.45,
  "ltc": 351.8,
  "req": .278,
  "wabi": 1.6,
  "neo": 69,
  //"icx": 2.05,
  "vet": 1.46,
  "qtum": 63,
  "eng": 1.19,
  "trx": 0.048807,
  "ost": .321272
}

function timeout() {
  $.get("/price", function(data) {
    var overall_profit = 0, overall = 0, overall_bought = 0;

    for (var i = 0; i < coins.length; ++i) {
      var price = data[coins[i]]["price"];
      var day_trend = data[coins[i]]["24h"];
      var hour_trend = data[coins[i]]["1h"];
      var curr_total = (price * owned[coins[i]]).toFixed(2);
      var bought_total = (bought[coins[i]] * owned[coins[i]]).toFixed(2);
      var total_profit = (curr_total - bought_total).toFixed(2);
      
      overall_profit += parseFloat(total_profit);
      overall_bought += parseFloat(bought_total);
      overall += parseFloat(curr_total);

      $("#"+coins[i]+" .price").text("$"+price);
      $("#"+coins[i]+" .24h").text(day_trend);
      $("#"+coins[i]+" .1h").text(hour_trend);

      $("#"+coins[i]+" .profit").text("$"+curr_total);
      $("#"+coins[i]+" .bought").text("$"+bought_total);
      $("#"+coins[i]+" .total_profit").text("$"+total_profit);

      if (day_trend[0] === "-") {
        $("#"+coins[i]+" .24h").css("color", "red");
      } else {
        $("#"+coins[i]+" .24h").css("color", "green");
      }
      if (hour_trend[0] === "-") {
        $("#"+coins[i]+" .1h").css("color", "red");
      } else {
        $("#"+coins[i]+" .1h").css("color", "green");
      }
      if (total_profit < 0) {
        $("#"+coins[i]+" .total_profit").css("color", "red");
      } else {
        $("#"+coins[i]+" .total_profit").css("color", "green");
      }
    }

    $("#my_total").text("$"+overall.toFixed(2));
    $("#my_bought").text("$"+overall_bought.toFixed(2));
    $("#my_profit").text("$"+overall_profit.toFixed(2));
    if (overall_profit < 0) {
      $("#my_profit").css("color", "red");
    } else {
      $("#my_profit").css("color", "green");
    }
  });
}

timeout();
setInterval(timeout, 10000);