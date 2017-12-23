var url = "/zack/";

function timeout() {

  $.get(url+"price", function(data) {
    var overall_profit = 0, overall = 0, overall_bought = 0;

    for (var i = 0; i < coins.length; ++i) {
      var curr_btc_price = data[coins[i]]["curr_btc_price"];
      var price = data[coins[i]]["price"];
      var btc_price = (data[coins[i]]["btc_price"] * parseFloat($("#"+coins[i]+" .owned").text())).toFixed(8);
      var day_trend = data[coins[i]]["24h"];
      var hour_trend = data[coins[i]]["1h"];
      var curr_total = (price * owned[coins[i]]).toFixed(2);
      //var bought_total = (bought[coins[i]] * owned[coins[i]]).toFixed(2);
      var bought_total = bought[coins[i]];
      var total_profit = ((btc_price - bought_total) * curr_btc_price).toFixed(2);
      
      overall_profit += parseFloat(total_profit);
      overall_bought += parseFloat(bought_total);
      overall += parseFloat(btc_price);


      $("#"+coins[i]+" .price").text("$"+price);
      $("#"+coins[i]+" .24h").text(day_trend);
      $("#"+coins[i]+" .1h").text(hour_trend);

      $("#"+coins[i]+" .profit").text(btc_price);
      $("#"+coins[i]+" .bought").text(bought_total);
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

    $("#my_total").text(overall.toFixed(8));
    $("#my_bought").text(overall_bought.toFixed(8));
    $("#my_profit").text("$"+overall_profit.toFixed(2));
    if (overall_profit < 0) {
      $("#my_profit").css("color", "red");
    } else {
      $("#my_profit").css("color", "green");
    }
  });
}
$(window).on('load', function() {
  if (window.location.pathname == "/nick") {
    url = "/nick/";
  } else if (window.location.pathname == "/jimmy") {
    url = "/jimmy/";
  }
  $.get(url+"arrays", function(data){
    for (var i = 0; i < data.length; ++i) {
      bought[data[i]["id"]] = data[i]["bought"].toFixed(8);
    }
  });
  timeout();
  setInterval(timeout, 10000);
});
