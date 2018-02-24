#
# iex_lib - Reusable classes and functions for accessing IEX
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

import os
import os.path
import inspect
import datetime
import json
from iex_app_logger import AppLogger
from url_helpers import setup_cacerts, exec_request

# Logger init
the_app_logger = AppLogger("iex-extension")
logger = the_app_logger.getAppLogger()

# Python2 does not have FileNotFoundError
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError
    logger.debug("FileNotFoundError defined")


class QConfiguration:
    """
    Encapsulates IEX configuration data
    """
    # Base URL for IEX services
    base_url = "https://api.iextrading.com/1.0"
    macOS = False
    file_path = ""
    full_file_path = ""
    cacerts = ""
    loglevel = "info"
    cwd = ""
    iex_conf_exists = False

    @classmethod
    def load(cls):
        """
        Load credentials from configuration file. The location of the iex.conf
        file is OS dependent. The permissions of the iex.conf file should allow
        access ONLY by the user.
        :return: None
        """
        file_name = "iex.conf"
        if os.name == "posix":
            # Linux or OS X
            cls.file_path = "{0}/libreoffice/iex/".format(os.environ["HOME"])
            cls.macOS = (os.uname()[0] == "Darwin")
        elif os.name == "nt":
            # Windows
            cls.file_path = "{0}\\libreoffice\\iex\\".format(os.environ["APPDATALOCAL"])
        cls.full_file_path = cls.file_path + file_name

        # Read iex.conf file
        try:
            cf = open(cls.full_file_path, "r")
            cfj = json.loads(cf.read())
            if "loglevel" in cfj:
                cls.loglevel = cfj["loglevel"]
                the_app_logger.set_log_level(cls.loglevel)
            cf.close()
            cls.iex_conf_exists = True
        except FileNotFoundError as ex:
            logger.error("%s was not found", cls.full_file_path)
        except Exception as ex:
            logger.error("An exception occurred while attempting to load iex.conf")
            logger.error(str(ex))

        # Set up path to certs
        cls.cwd = os.path.realpath(os.path.abspath
                                          (os.path.split(inspect.getfile
                                                         (inspect.currentframe()))[0]))
        # The embedded version of Python found in some versions of LO Calc
        # does not handle certificates. Here we compensate by using the certificate
        # package from the certifi project: https://github.com/certifi/python-certifi
        if os.name == "posix":
            cls.cacerts = "{0}/cacert.pem".format(cls.cwd)
        elif os.name == "nt":
            # This may not be necessary in Windows
            cls.cacerts = "{0}\\cacert.pem".format(cls.cwd)
        logger.debug("Path to cacert.pem: %s", cls.cacerts)
        # Attach the certs file to the URL processor
        setup_cacerts(cls.cacerts)

        # If no iex.conf file exists, create one with all defaults
        if not cls.iex_conf_exists:
            QConfiguration.save()
            # The logger defaults to debug level logging.
            # This sets the log level to whatever default was set above.
            the_app_logger.set_log_level(cls.loglevel)

    @classmethod
    def save(cls):
        """
        Save configuraton back to iex.conf
        :return:
        """

        # Make sure folders exist
        if not os.path.exists(cls.file_path):
            os.makedirs(cls.file_path)

        conf = {}
        conf["certifi"] = cls.cacerts
        conf["loglevel"] = cls.loglevel

        logger.debug("Saving configuration to %s", cls.full_file_path)
        cf = open(cls.full_file_path, "w")
        json.dump(conf, cf, indent=4)
        cf.close()

        if os.name == "posix":
            import stat
            # The user gets R/W permissions
            os.chmod(cls.full_file_path, stat.S_IRUSR | stat.S_IWUSR)
        else:
            pass

        cls.iex_conf_exists = True

    @classmethod
    def is_configured(cls):
        """
        IEX is configured if the iex.conf file exists
        :return:
        """

        return cls.iex_conf_exists

# Set up configuration
QConfiguration.load()


class IEXBase:
    @staticmethod
    def _exec_request(url_string, parms=None):
        """
         Submit https request to IEX
        :param url_string:
        :param parms:
        :return: JSON decoded dict containing results of https GET.
        The status_code key is added to return the HTTPS status code.
        """

        j = exec_request(QConfiguration.base_url + url_string, parms)
        return j

    @staticmethod
    def exec_stock_request(symbol, category, parms=None):
        url_string = "/stock/{0}/{1}".format(symbol.upper(), category)
        return IEXBase._exec_request(url_string, parms=parms)

    @staticmethod
    def status_code_message(status_code):
        """
        Return an appropriate message for a non-200 status code
        :param status_code:
        :return:
        """
        return "Unexpected status code " + str(status_code)

    @staticmethod
    def get_formatted_datetime(unix_time_ms):
        """
        Converts an IEX timestamp value to an ISO formatted date/time string
        :param unix_time_ms: Unix time in milliseconds.
        See https://github.com/iexg/IEX-API/issues/93
        :return: ISO date/time in local time
        """
        lt = float(unix_time_ms) / 1000.0
        # To local time
        dt = datetime.datetime.fromtimestamp(lt)
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


class IEXStocks(IEXBase):
    def __init__(self):
        pass

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
