#
# iex_earnings - Implements the IexEarnings functions
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
from iex_stocks import IEXStocks
from iex_base import IEXBase

# Logger init
the_app_logger = AppLogger("iex-extension")
logger = the_app_logger.getAppLogger()

class IEXEarnings(IEXBase):
    """
    Derived class representing the IEX Earnings API. A number of
    the base class methods need to be overriden to accommodate the
    earnings period used in the IEX API.
    """
    def __init__(self):
        super(IEXEarnings, self).__init__()
        self.time_keys = []
        logger.debug("IEXEarnings initialized")

    # The dervived class must override this method
    def _get_result_for_symbol(self, symbol):
        """
        Returns a result for a given stock ticker symbol. This method
        MUST be overriden by the derived class so it gets the result
        specific to the derived class.
        :param symbol: The target stock ticker symbol.
        :return:
        """
        symbol = symbol.upper()
        cache_key = symbol
        res = self._get_cached_result(cache_key)
        if res:
            logger.debug("Earnings cache hit for %s", cache_key)
        else:
            logger.debug("Earnings cache miss for %s", cache_key)
            res = IEXStocks.get_earnings(symbol)
            if res["status_code"] == 200:
                self._cache_result(cache_key, res)
                logger.debug("Earnings cached for %s", cache_key)
        return res

    def _get_result_keys(self):
        """
        Return the list of keys in a result. The keys are taken from
        the first period in a divdend result.
        :return:
        """
        if not self.result_keys:
            res = self._get_result_for_symbol(self.template_symbol)
            if res["status_code"] != 200:
                return None
            # Sort keys case insensitive. Avoids randomized list of keys.
            self.result_keys = list(res["result"]["earnings"][0].keys())
            self.result_keys.sort(key=lambda k: k.lower())
        return self.result_keys

    def get_result_key_count(self):
        """
        Returns the number of keys in a result. The keys are taken from
        the first period in a divdend result.
        :return:
        """
        res = self._get_result_for_symbol(self.template_symbol)
        if res["status_code"] == 200:
            return len(res["result"]["earnings"][0])
        return res["error_message"]

    def get_result_item(self, category, symbol, key, period):
        """
        Returns a result item (a key/value) using data provided by an IEX API call.
        :param category: URL category. Currently only used for messages. Could be
        used to refactor IEX API calls.
        :param symbol: Target stock ticker symbol.
        :param key: item key to be returned.
        :param period: 0-3
        :return: Key value or error message
        """
        if self._is_valid_result_key(key):
            res = self._get_result_for_symbol(symbol)
            if res["status_code"] == 200:
                # This is here for comprehensive coverage.
                # Currently, none of the result values required conversion.
                # Apply time conversion as required
                v = res["result"]["earnings"][period][key]
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

# Singleton instance of the IEXEarnings class
earnings_inst = IEXEarnings()

def get_earnings_key_count():
    """
    Returns the number of keys in a earnings period result.
    :return:
    """
    return earnings_inst.get_result_key_count()

def get_earnings_keyx(index):
    """
    Returns the index-th key available in a time period result.
    :param index: 0 to get_earnings_key_count() - 1 (i.e. 0-8)
    :return: The value of the index-th key.
    """
    return earnings_inst.get_result_keyx(index)

def get_earnings_item(symbol, key, period):
    """
    Returns an earnings item (a key/value) using data provided by the IEX Earnings API call.
    The value is for a period within a period range 0-3 where period 0 is the most recent period in
    the range. So, the periods would be 0, 1, 2 and 3.
    :param symbol: Target stock ticker symbol.
    :param key: item key to be returned.
    :param period: 0 to 3.
    :return: Key value or error message
    """
    return earnings_inst.get_result_item("earnings", symbol, key, period)
