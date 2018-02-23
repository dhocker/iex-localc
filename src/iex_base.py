#
# iex_base - Base clase for IEX API classes
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
from datetime import datetime, timedelta

# Logger init
the_app_logger = AppLogger("iex-extension")
logger = the_app_logger.getAppLogger()

class IEXBase:
    """
    
    """
    def __init__(self):
        # This list is used to validate requested item keys
        self.result_keys = None
        # Cache organization
        # {"ticker": {"expiration": datetime, "result": {}}}
        self.result_cache = {}
        # Keys that require time conversion
        self.time_keys = []
        logger.debug("IEXBase initialized")
        # Ticker symbol to use as a template
        self.template_symbol = "ibm"

    @staticmethod
    def _get_formatted_datetime(unix_time_ms):
        """
        Converts an IEX timestamp value to an ISO formatted date/time string
        :param unix_time_ms: Unix time in milliseconds.
        See https://github.com/iexg/IEX-API/issues/93
        :return: ISO date/time in local time
        """
        lt = float(unix_time_ms) / 1000.0
        # To local time
        dt = datetime.fromtimestamp(lt)
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")

    def _get_cached_result(self, symbol):
        """
        Returns a cached result for a given stock ticker symbol.
        :param symbol: The target stock ticker symbol.
        :return: Returns None if no cached result is available.
        """
        if (symbol in self.result_cache) and (self.result_cache[symbol]["expiration"] > datetime.now()):
            return self.result_cache[symbol]["result"]
        return None
    
    def _cache_result(self, result):
        """
        Add a result to the cache. An existing result for a symbol is replaced.
        A cached quote has a "time-to-live" (TTL) value after which it is considered
        invalid.
        :param result:
        :return:
        """
        # Quote expires in 5 minutes. TODO Consider making this a config value.
        self.result_cache[result["result"]["symbol"]] = {"expiration":datetime.now() + timedelta(minutes=5), "result":result}

    # TODO The dervived class must override this method
    def _get_result_for_symbol(self, symbol):
        """
        Returns a result for a given stock ticker symbol. This method
        MUST be overriden by the derived class so it gets the result
        specific to the derived class.
        :param symbol: The target stock ticker symbol.
        :return:
        """
        logger.debug("_get_result_for_symbol was not overriden")
        return None
    
    def _get_result_keys(self):
        """
        Return the list of keys in a result.
        :return:
        """
        if not self.result_keys:
            res = self._get_result_for_symbol(self.template_symbol)
            if res["status_code"] != 200:
                return None
            # Sort keys case insensitive. Avoids randomized list of keys.
            self.result_keys = list(res["result"].keys())
            self.result_keys.sort(key=lambda k: k.lower())
        return self.result_keys
    
    def _is_valid_result_key(self, key):
        """
        Answers the question: Is key valid for this result?
        :param key:
        :return:
        """
        keys = self._get_result_keys()
        return key in keys

    def get_result_key_count(self):
        """
        Returns the number of keys in a result.
        :return:
        """
        res = self._get_result_for_symbol(self.template_symbol)
        if res["status_code"] == 200:
            return len(res["result"])
        return res["error_message"]

    def get_result_keyx(self, index):
        """
        Returns the index-th key available in a result.
        :param index: 0 to quote_key_count() - 1
        :return: The value of the index-th key.
        """
        keys = self._get_result_keys()
        if keys:
            if len(keys) > index:
                return keys[index]
            return "Index out of range"
        return "Keys not available"

    def get_result_item(self, category, symbol, key):
        """
        Returns a result item (a key/value) using data provided by an IEX API call.
        :param category: URL category. Currently only used for messages. Could be
        used to refactor IEX API calls.
        :param symbol: Target stock ticker symbol.
        :param key: item key to be returned.
        :return: Key value or error message
        """
        if self._is_valid_result_key(key):
            res = self._get_result_for_symbol(symbol)
            if res["status_code"] == 200:
                # Apply time conversion as required
                v = res["result"][key]
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
