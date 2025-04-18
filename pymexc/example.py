import time

import spot, futures

# api_key = "YOUR API KEY"
# api_secret = "YOUR API SECRET KEY"
#
# def handle_message(message):
#     # handle websocket message
#     print(message)
#
#
# # SPOT V3
# # initialize HTTP client
# spot_client = spot.HTTP(api_key = api_key, api_secret = api_secret)
# # initialize WebSocket client
# ws_spot_client = spot.WebSocket(api_key = api_key, api_secret = api_secret)
#
# # make http request to api
# print(spot_client.exchange_info())
#
# # create websocket connection to public channel (spot@public.deals.v3.api@BTCUSDT)
# # all messages will be handled by function `handle_message`
# ws_spot_client.deals_stream(handle_message, "BTCUSDT")
#

# FUTURES V1


# initialize HTTP client
futures_client = futures.HTTP(api_key="mx0vglBymZmPsaiwPk", api_secret="949305f629ba473e9111b405a409a070")


# make http request to api
b = futures_client.open_positions("ETH_USDT").get("data")
for i in b:
    print("%s %sX 持仓数量：%s" % (i.get("symbol"), i.get("leverage"), str(i.get("holdVol") / 2000)))

  # symbol:            str,
  #             price:             float,
  #             vol:               float,
  #             side:              int,
  #             type:              int,
  #             open_type:         int,
time.sleep(2)
c = futures_client.order("BTC_USDT", 10000, 0.01, 1, 1, 2)
print(c)
a = futures_client.asset("USDT")
print(a)


def handle_message(message):
    # handle websocket message
    print(message)


# api_key = "mx0vglBymZmPsaiwPk"
# api_secret = "949305f629ba473e9111b405a409a070"
# ws_futures_client = futures.WebSocket(api_key=api_key, api_secret=api_secret)
# ws_futures_client.position_stream(handle_message)
