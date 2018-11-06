#
# iex_stocks - IEX stocks class
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

from iex_base import IEXBase
from iex_app_logger import AppLogger

# Logger init
the_app_logger = AppLogger("iex-extension")
logger = the_app_logger.getAppLogger()

class IEXStocks(IEXBase):
    def __init__(self):
        super(IEXStocks, self).__init__()
        self.time_keys = []
        logger.debug("IEXStocks initialized")

    @staticmethod
    def get_book(ticker):
        """
        Call IEX API to get book info for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "book")
        return res

    @staticmethod
    def get_company(ticker):
        """
        Call IEX API to get info for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "company")
        return res

    @staticmethod
    def get_delayed_quote(ticker):
        """
        Call IEX API to get the delayed quote for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "delayed-quote")
        return res

    @staticmethod
    def get_dividends(ticker, period_range):
        """
        Calls the IEX Stocks/Dividends API to retrieve divdend data for a given time period range.
        :param ticker: Stock symbol.
        :param period_range: See https://iextrading.com/developer/docs/#dividends
        :return: Returns a dict where the result key contains an array of dividends.
        """

        template_url = "dividends/{0}"
        url_string = template_url.format(period_range)
        res = IEXStocks.exec_stock_request(ticker, url_string)
        # logger.debug("%s %s %s", res["identifier"], res["item"], res["value"])
        return res

    @staticmethod
    def get_earnings(ticker):
        """
        Call IEX API to get the earnings for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "earnings")
        return res

    @staticmethod
    def get_financials(ticker):
        """
        Call IEX API to get financials for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "financials")
        return res

    @staticmethod
    def get_price(ticker):
        """
        Call IEX API to get current price for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "price")
        return res

    @staticmethod
    def get_quote(ticker):
        """
        Call IEX API to get current quote for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "quote")
        return res

    @staticmethod
    def get_ohlc(ticker):
        """
        Call IEX API to get open/high/low/close price for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "ohlc")
        return res

    @staticmethod
    def get_previous(ticker):
        """
        Call IEX API to get current price for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "previous")
        return res

    @staticmethod
    def get_stats(ticker):
        """
        Call IEX API to get key stats for a given ticker symbol
        :param ticker:
        :return:
        """

        res = IEXStocks.exec_stock_request(ticker, "stats")
        return res
