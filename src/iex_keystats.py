#
# iex_keystats - Implements the IexKeyStats function
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

class IEXKeyStats(IEXBase):
    """

    """
    def __init__(self):
        super(IEXKeyStats, self).__init__()
        self.time_keys = []
        logger.debug("IEXKeyStats initialized")

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
        res = self._get_cached_result(symbol)
        if res:
            logger.debug("KyeStats cache hit for %s", symbol)
        else:
            logger.debug("KeyStats cache miss for %s", symbol)
            res = IEXStocks.get_stats(symbol)
            if res["status_code"] == 200:
                self._cache_result(symbol, res)
                logger.debug("KeyStats cached for %s", symbol)
        return res

# Singleton instance of the IEXKeyStats class
keystats_inst = IEXKeyStats()

def get_keystats_key_count():
    """
    Returns the number of keys in a key stats result.
    :return:
    """
    return keystats_inst.get_result_key_count()

def get_keystats_keyx(index):
    """
    Returns the index-th key available in a key stats result.
    :param index: 0 to get_keystats_key_count() - 1
    :return: The value of the index-th key.
    """
    return keystats_inst.get_result_keyx(index)

def get_keystats_item(symbol, key):
    """
    Returns a key stats item (a key/value) using data provided by the IEX key stats API call.
    :param symbol: Target stock ticker symbol.
    :param key: item key to be returned.
    :return: Key value or error message
    """
    # This is a temporary solution for items that are Unix timestamps.
    return keystats_inst.get_result_item("stats", symbol, key)
