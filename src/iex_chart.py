#
# iex_chart - Implements the IexChart function
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
from iex_base import IEXBase
from cache_db import CacheDB
from extn_helper import normalize_date
from datetime import datetime

# Logger init
the_app_logger = AppLogger("iex-extension")
logger = the_app_logger.getAppLogger()

class IEXChart(IEXBase):
    """

    """
    def __init__(self):
        super(IEXChart, self).__init__()
        self.time_keys = []
        logger.debug("IEXChart initialized")

    @staticmethod
    def get_closing_price_for_date(symbol, for_date):
        """
        Call IEX API to get the closing price for a given symbol on
        a given date. This method uses the IEX chart URL to fetch
        daily chart data for the smallest period containing the for_date.
        The maximum is 5 years.
        :param ticker:
        :return:
        """

        # Try for cache hit first
        r = CacheDB.lookup_closing_price_by_date(symbol.upper(), for_date)
        if r:
            price = r["Close"]
            logger.debug("Closing price cache hit for %s %s %f", symbol.upper(), for_date, price)
            return price

        # Determine the width of the chart data based on the for_date
        # This can be 1m, 3m, 6m, 1y, 2y or 5y
        diff = datetime.now() - datetime.strptime(for_date, "%Y-%m-%d")
        if diff.days <= 30:
            period = "1m"
        elif diff.days <= 90:
            period = "3m"
        elif diff.days <= 180:
            period = "6m"
        elif diff.days <= 365:
            period = "1y"
        elif diff.days <= (365 * 2):
            period = "2y"
        else:
            period = "5y"

        url_string = "/stock/{0}/chart/{1}".format(symbol.upper(), period)
        res = IEXBase._exec_request(url_string, parms=None)

        # There are other more sophisticated ways to search a list.
        # This one has the advantage of stopping as soon as a match is found.
        for day in res["result"]:
            if day["date"] == for_date:
                # Cache the closing price
                price = float(day["close"])
                CacheDB.insert_closing_price(symbol.upper(), for_date, price)
                logger.debug("Closing price cached for %s %s %f", symbol.upper(), for_date, price)
                return price
        logger.error("Chart data for {0} on date {1} was not found".format(symbol.upper(), for_date))
        return "Not found"

# Singleton instance of the IEXChart class
# chart_inst = IEXChart()

def get_closing_price(symbol, for_date):
    # Resolve date. It can be a LibreCalc date as a float or a string date
    try:
        eff_date = normalize_date(for_date)
    except ValueError as ex:
        logger.error(str(ex))
        return "Invalid date format"

    return IEXChart.get_closing_price_for_date(symbol, eff_date)
