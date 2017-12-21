
coins = [
  "btc",
  "eth",
  "ltc",
  "req",
  "wabi",
  "xrp",
  //"neo",
  //"icx",
  "vet",
  //"qtum",
  //"eng",
  "trx",
  "ost"
];

owned = {
  "btc": 0.01845468,
  "eth": 0.24861740,
  "ltc": 0.56849907,
  "req": 197.802,
  "wabi": 29.956,
  "xrp": 61.95,
  //"neo": .00955,
  //"icx": 5,
  "vet": 34.932,
  //"qtum": 0.00872,
  //"eng": 23.976,
  "trx": 999.999,
  "ost": 164.835
};

bought = {
  "btc": 18345.99,
  "eth": 804.45,
  "ltc": 351.8,
  "req": .278,
  "wabi": 1.77,
  "xrp": 1.05,
  //"neo": 69,
  //"icx": 2.05,
  "vet": 1.50,
  //"qtum": 63,
  //"eng": 1.19,
  "trx": 0.048807,
  "ost": .321272
};


nick_coins = [
  "trx", "xrp"
];

nick_owned = {
  "trx": 397.602,
  "xrp": 23.976
};

nick_bought = {
  "trx": .04,
  "xrp": .96
}

function timeout() {
  var url = "/price";
  var coin_arr = coins;
  var which_owned = owned;
  var which_bought = bought;
  if (window.location.pathname == "/nick") {
    url = "/nickprice";
    coin_arr = nick_coins;
    which_owned = nick_owned;
    which_bought = nick_bought;
  }

  $.get(url, function(data) {
    var overall_profit = 0, overall = 0, overall_bought = 0;

    for (var i = 0; i < coin_arr.length; ++i) {
      var price = data[coin_arr[i]]["price"];
      var day_trend = data[coin_arr[i]]["24h"];
      var hour_trend = data[coin_arr[i]]["1h"];
      var curr_total = (price * which_owned[coin_arr[i]]).toFixed(2);
      var bought_total = (which_bought[coin_arr[i]] * which_owned[coin_arr[i]]).toFixed(2);
      var total_profit = (curr_total - bought_total).toFixed(2);
      
      overall_profit += parseFloat(total_profit);
      overall_bought += parseFloat(bought_total);
      overall += parseFloat(curr_total);

      $("#"+coin_arr[i]+" .price").text("$"+price);
      $("#"+coin_arr[i]+" .24h").text(day_trend);
      $("#"+coin_arr[i]+" .1h").text(hour_trend);

      $("#"+coin_arr[i]+" .profit").text("$"+curr_total);
      $("#"+coin_arr[i]+" .bought").text("$"+bought_total);
      $("#"+coin_arr[i]+" .total_profit").text("$"+total_profit);

      if (day_trend[0] === "-") {
        $("#"+coin_arr[i]+" .24h").css("color", "red");
      } else {
        $("#"+coin_arr[i]+" .24h").css("color", "green");
      }
      if (hour_trend[0] === "-") {
        $("#"+coin_arr[i]+" .1h").css("color", "red");
      } else {
        $("#"+coin_arr[i]+" .1h").css("color", "green");
      }
      if (total_profit < 0) {
        $("#"+coin_arr[i]+" .total_profit").css("color", "red");
      } else {
        $("#"+coin_arr[i]+" .total_profit").css("color", "green");
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