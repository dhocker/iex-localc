#
# iex_price - Implements the IexPrice function
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

# Logger init
the_app_logger = AppLogger("iex-extension")
logger = the_app_logger.getAppLogger()

def get_price(symbol):
    """
    Returns the current price for a stock symbol using the IEX price API call.
    :param symbol: Target stock ticker symbol.
    :return: Price or error message
    """
    res = IEXStocks.get_price(symbol)
    if res["status_code"] == 200:
        return float(res["result"])
    return res["error_message"]
