#
# iex_quote - Implements the IexQuote function
# Copyright (C) 2018  Dave Hocker (email: Qalydon17@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE.md file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE.md file).  If not, see <http://www.gnu.org/licenses/>.
#

from iex_app_logger import AppLogger
from iex_lib import IEXStocks
from datetime import datetime, timedelta

# Logger init
the_app_logger = AppLogger("iex-extension")
logger = the_app_logger.getAppLogger()

# From https://iextrading.com/developer/docs/#quote
# This is used to validate requested item keys
quote_keys = {
    "symbol": "AAPL",
    "companyName": "Apple Inc.",
    "primaryExchange": "Nasdaq Global Select",
    "sector": "Technology",
    "calculationPrice": "tops",
    "open": 154,
    "openTime": 1506605400394,
    "close": 153.28,
    "closeTime": 1506605400394,
    "high": 154.80,
    "low": 153.25,
    "latestPrice": 158.73,
    "latestSource": "Previous close",
    "latestTime": "September 19, 2017",
    "latestUpdate": 1505779200000,
    "latestVolume": 20567140,
    "iexRealtimePrice": 158.71,
    "iexRealtimeSize": 100,
    "iexLastUpdated": 1505851198059,
    "delayedPrice": 158.71,
    "delayedPriceTime": 1505854782437,
    "previousClose": 158.73,
    "change": -1.67,
    "changePercent": -0.01158,
    "iexMarketPercent": 0.00948,
    "iexVolume": 82451,
    "avgTotalVolume": 29623234,
    "iexBidPrice": 153.01,
    "iexBidSize": 100,
    "iexAskPrice": 158.66,
    "iexAskSize": 100,
    "marketCap": 751627174400,
    "peRatio": 16.86,
    "week52High": 159.65,
    "week52Low": 93.63,
    "ytdChange": 0.3665,
}

# Cache organization
# {"ibm": {"expiration": datetime, "result": {}}}
quote_cache = {}

def _get_cached_quote(symbol):
    global quote_cache
    if (symbol in quote_cache) and (quote_cache[symbol]["expiration"] > datetime.now()):
        return quote_cache[symbol]["result"]
    return None

def _cache_quote(symbol, result):
    global quote_cache
    # Quote expires in 5 minutes. TODO Consider making this a config value.
    quote_cache[symbol] = {"expiration":datetime.now() + timedelta(minutes=5), "result":result}

def get_quote(symbol, key):
    """
    Returns a quote item using data provided by the IEX quote API call.
    :param symbol: Target stock ticker symbol.
    :param key: item key to be returned.
    :return: Key value or error message
    """
    global quote_keys

    symbol = symbol.upper()

    if key in quote_keys:
        res = _get_cached_quote(symbol)
        if res:
            logger.debug("Quote cache hit for %s %s", symbol, key)
            return res["result"][key]
        else:
            logger.debug("Quote cache miss for %s %s", symbol, key)
            res = IEXStocks.get_quote(symbol)
            if res["status_code"] == 200:
                _cache_quote(symbol, res)
                logger.debug("Quote cached for %s %s", symbol, key)
                return res["result"][key]
            return res["error_message"]
    return "Invalid quote key"

