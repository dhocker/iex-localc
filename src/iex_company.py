#
# iex_company - Implements the IexCompany function
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

class IEXCompany(IEXBase):
    """

    """
    def __init__(self):
        super(IEXCompany, self).__init__()
        self.time_keys = []
        logger.debug("IEXCompany initialized")

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
            logger.debug("Company cache hit for %s", symbol)
        else:
            logger.debug("Company cache miss for %s", symbol)
            res = IEXStocks.get_company(symbol)
            if res["status_code"] == 200:
                self._cache_result(symbol, res)
                logger.debug("Company cached for %s", symbol)
        return res

# Singleton instance of the IEXQuote class
company_inst = IEXCompany()

def get_company_key_count():
    """
    Returns the number of keys in a quote.
    :return:
    """
    return company_inst.get_result_key_count()

def get_company_keyx(index):
    """
    Returns the index-th key available in a quote.
    :param index: 0 to quote_key_count() - 1
    :return: The value of the index-th key.
    """
    return company_inst.get_result_keyx(index)

def get_company_item(symbol, key):
    """
    Returns a quote item (a key/value) using data provided by the IEX quote API call.
    :param symbol: Target stock ticker symbol.
    :param key: item key to be returned.
    :return: Key value or error message
    """
    # This is a temporary solution for items that are Unix timestamps.
    return company_inst.get_result_item("company", symbol, key)
