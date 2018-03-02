#
# iex_dividends - Implements the IexDividends functions
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
from iex_base import IEXBase

# Logger init
the_app_logger = AppLogger("iex-extension")
logger = the_app_logger.getAppLogger()

class IEXDividends(IEXBase):
    """
    Derived class representing the IEX Dividends API. A number of
    the base class methods need to be overriden to accomodate the
    dividend period and dividend period range that is used in the
    IEX API.
    """
    def __init__(self):
        super(IEXDividends, self).__init__()
        self.time_keys = []
        self.default_range = "1y"
        logger.debug("IEXDividends initialized")

    # The dervived class must override this method
    def _get_result_for_symbol(self, symbol, period_range):
        """
        Returns a result for a given stock ticker symbol. This method
        MUST be overriden by the derived class so it gets the result
        specific to the derived class.
        :param symbol: The target stock ticker symbol.
        :return:
        """
        symbol = symbol.upper()
        cache_key = "{0}-{1}".format(symbol, period_range)
        res = self._get_cached_result(cache_key)
        if res:
            logger.debug("Dividends cache hit for %s", cache_key)
        else:
            logger.debug("Dividends cache miss for %s", cache_key)
            res = IEXStocks.get_dividends(symbol, period_range)
            if res["status_code"] == 200:
                self._cache_result(cache_key, res)
                logger.debug("Dividends cached for %s", cache_key)
        return res

    def _get_result_keys(self):
        """
        Return the list of keys in a result. The keys are taken from
        the first period in a divdend result.
        :return:
        """
        if not self.result_keys:
            res = self._get_result_for_symbol(self.template_symbol, self.default_range)
            if res["status_code"] != 200:
                return None
            # Sort keys case insensitive. Avoids randomized list of keys.
            self.result_keys = list(res["result"][0].keys())
            self.result_keys.sort(key=lambda k: k.lower())
        return self.result_keys

    def get_result_key_count(self):
        """
        Returns the number of keys in a result. The keys are taken from
        the first period in a divdend result.
        :return:
        """
        res = self._get_result_for_symbol(self.template_symbol, self.default_range)
        if res["status_code"] == 200:
            return len(res["result"][0])
        return res["error_message"]

    def get_result_result_period_count(self, symbol, period_range):
        """
        Returns the number of dividends in a result.
        :return:
        """
        res = self._get_result_for_symbol(symbol, period_range)
        if res["status_code"] == 200:
            return len(res["result"])
        return res["error_message"]

    def get_result_item(self, category, symbol, key, period, period_range):
        """
        Returns a result item (a key/value) using data provided by an IEX API call.
        :param category: URL category. Currently only used for messages. Could be
        used to refactor IEX API calls.
        :param symbol: Target stock ticker symbol.
        :param key: item key to be returned.
        :return: Key value or error message
        """
        if self._is_valid_result_key(key):
            res = self._get_result_for_symbol(symbol, period_range)
            if res["status_code"] == 200:
                # This is here for comprehensive coverage.
                # Currently, none of the result values required conversion.
                # Apply time conversion as required
                v = res["result"][period][key]
                if key in self.time_keys:
                    if v:
                        # Convert IEX timestamp value to something human readable
                        return IEXBase._get_formatted_datetime(v)
                    else:
                        return "NA"
                elif isinstance(v, int) and (v > 2147483647 or v < -2147483648):
                    # LO calc doesn't seem to handle large integers
                    return float(v)
                return v
            return res["error_message"]
        return "Invalid {0} key".format(category)

# Singleton instance of the IEXDividends class
dividends_inst = IEXDividends()

def get_dividends_key_count():
    """
    Returns the number of keys in a dividends period result.
    :return:
    """
    return dividends_inst.get_result_key_count()

def get_dividends_period_count(symbol, period_range):
    """
    Returns the number of periods in a given symbol's period range.
    :param symbol: Stock ticker symbol.
    :param period_range: 5y, 2y, 1y, ytd, 6m, 3m or 1m. See https://iextrading.com/developer/docs/#dividends
    :return: Number of periods in the period range.
    """
    return dividends_inst.get_result_result_period_count(symbol, period_range)

def get_dividends_keyx(index):
    """
    Returns the index-th key available in a time period result.
    :param index: 0 to get_dividends_key_count() - 1
    :return: The value of the index-th key.
    """
    return dividends_inst.get_result_keyx(index)

def get_dividends_item(symbol, key, period, period_range):
    """
    Returns a dividend item (a key/value) using data provided by the IEX dividends API call.
    The value is for a period within a period range where period 0 is the most recent period in
    the range. For example, a one year period range is likely to contain 4 dividends. So,
    the periods would be 0, 1, 2 and 3.
    :param symbol: Target stock ticker symbol.
    :param key: item key to be returned.
    :param period: 0 to n depending on the period range.
    :param period_range: See https://iextrading.com/developer/docs/#dividends
    :return: Key value or error message
    """
    return dividends_inst.get_result_item("dividends", symbol, key, period, period_range)

def get_dividends_ttm(symbol):
    """
    Returns the trailing twelve months dividends for a given ticker symbol.
    :param symbol: Stock ticker symbol
    :return: Trailing twelve months dividends
    """
    ttm = 0.0
    for i in range(4):
        ttm += dividends_inst.get_result_item("dividends", symbol, "amount", i, "1y")
    return ttm