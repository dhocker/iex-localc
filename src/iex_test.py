#
# The IEX API appears to be most useful for current, relatively real time data.
# It is not very useful for obtaining data that is more than about 30 days old (particularly prices).
# It can obtain historical dividend data for the last 5 years.
# It can also be useful for obtaining relatively static company information.
# See https://iextrading.com/developer/docs/
#

# Candidate LibreOffice function signatures
# IEXStocksCompany(ticker, key)
# IEXStocksDividends(ticker, dividendrange, key)
# IEXStocksEarnings(ticker, index, key)

from url_helpers import exec_request, setup_cacerts
from iex_lib import IEXStocks
import datetime
import time
import json

# print ("Company info")
# j = IEXStocks.get_company("SO")
# print (j["status_code"])
# print(j["result"])

# print("Delayed Quote")
# j = IEXStocks.get_delayed_quote("aapl")
# print (j["status_code"])
# print(json.dumps(j["result"], indent=4))
# tv = float(j["result"]["delayedPriceTime"])
# # To local time
# dt = IEXStocks.get_formatted_datetime(tv)
# print ("Delayed price time:", dt)

# print("Dividends")
# j = IEXStocks.get_dividends("SO", "1y")
# print (j["status_code"])
# print(j["result"])

# print("Financials")
# j = IEXStocks.get_financials("SO")
# print (j["status_code"])
# print(j["result"])

# print("Quote")
# j = IEXStocks.get_quote("IBM")
# print (j["status_code"])
# print(j["result"])
#
# # Time is unix time in milliseconds
# # See https://github.com/iexg/IEX-API/issues/93
# tv = float(j["result"]["latestUpdate"])
# # To local time
# dt = IEXStocks.get_formatted_datetime(tv)
# print (dt)

# print("Previous")
# j = IEXStocks.get_previous("IBM")
# print (j["status_code"])
# print(j["result"])

# print("Key Stats")
# j = IEXStocks.get_stats("aapl")
# print (j["status_code"])
# print(json.dumps(j["result"], indent=4))

print("Earnings")
j = IEXStocks.get_earnings("aapl")
print (j["status_code"])
print(json.dumps(j["result"], indent=4))
