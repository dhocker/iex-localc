#
# IEX extension main interface to LO Calc
# Copyright (C) 2017  Dave Hocker (email: qalydon17@gmail.com)
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
# References
# https://wiki.openoffice.org/wiki/Calc/Add-In/Python_How-To
# http://www.biochemfusion.com/doc/Calc_addin_howto.html
# https://github.com/madsailor/SMF-Extension
#

try:
    import os
    import sys
    import inspect
    import threading
    import unohelper
    from com.iex.api.localc import XIex

    # Add current directory to path to import local modules
    cmd_folder = os.path.realpath(os.path.abspath
                                  (os.path.split(inspect.getfile
                                                 ( inspect.currentframe() ))[0]))
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)

    # Local imports go here
    from iex_app_logger import AppLogger
    import xml.etree.ElementTree as etree

    # Logger init
    the_app_logger = AppLogger("iex-extension")
    logger = the_app_logger.getAppLogger()
    # Extract version from description.xml
    tree = etree.parse(cmd_folder + "/description.xml")
    root = tree.getroot()
    nodes = root.findall('{http://openoffice.org/extensions/description/2006}version')
    logger.info("IEX-LOCalc Version: %s", nodes[0].attrib["value"])
    # After logger
    from iex_price import get_price
    from iex_quote import get_quote_key_count, get_quote_keyx, get_quote_item
    from iex_company import get_company_key_count, get_company_keyx, get_company_item
    from iex_keystats import get_keystats_key_count, get_keystats_keyx, get_keystats_item
    from iex_dividends import get_dividends_key_count, get_dividends_period_count, get_dividends_keyx, \
        get_dividends_item, get_dividends_ttm
    from iex_earnings import get_earnings_key_count, get_earnings_keyx, get_earnings_item
    from iex_chart import get_closing_price
except Exception as ex:
    # Emergency debugging to cover for the fact that LibreOffice is terrible at debugging...
    from iex_lib import QConfiguration
    fh = open(QConfiguration.home_data_path() + "error_report.txt", "a")
    fh.write(ex)
    fh.write(str(ex))
    fh.close()
    exit(666)

class IexImpl(unohelper.Base, XIex ):
    """Define the main class for the IEX LO Calc extension """
    def __init__( self, ctx ):
        self.ctx = ctx
        logger.debug("IexImpl initialized")
        logger.debug("self: %s", str(self))
        logger.debug("ctx: %s", str(ctx))

    def IexPrice(self, symbol):
        logger.debug("IexPrice called %s", symbol)
        return get_price(symbol)

    def IexQuoteKeyCount(self):
        logger.debug("IexQuoteKeyCount called")
        return get_quote_key_count()

    def IexQuoteKeyByIndex(self, index):
        logger.debug("IexQuoteKeyByIndex called %d", index)
        return get_quote_keyx(index)

    def IexQuoteItem(self, symbol, key):
        logger.debug("IexQuoteItem called %s %s", symbol, key)
        return get_quote_item(symbol, key)

    def IexCompanyKeyCount(self):
        logger.debug("IexCompanyKeyCount called")
        return get_company_key_count()

    def IexCompanyKeyByIndex(self, index):
        logger.debug("IexCompanyKeyByIndex called %d", index)
        return get_company_keyx(index)

    def IexCompanyItem(self, symbol, key):
        logger.debug("IexCompanyItem called %s %s", symbol, key)
        return get_company_item(symbol, key)

    def IexKeyStatsKeyCount(self):
        logger.debug("IexKeyStatsKeyCount called")
        return get_keystats_key_count()

    def IexKeyStatsKeyByIndex(self, index):
        logger.debug("IexKeyStatsKeyByIndex called %d", index)
        return get_keystats_keyx(index)

    def IexKeyStatsItem(self, symbol, key):
        logger.debug("IexKeyStatsItem called %s %s", symbol, key)
        return get_keystats_item(symbol, key)

    def IexDividendsKeyCount(self):
        logger.debug("IexDividendsKeyCount called")
        return get_dividends_key_count()

    def IexDividendsPeriodCount(self, symbol, periodrange):
        logger.debug("IexDividendsPeriodCount called")
        return get_dividends_period_count(symbol, periodrange)

    def IexDividendsKeyByIndex(self, index):
        logger.debug("IexDividendsKeyByIndex called %d", index)
        return get_dividends_keyx(index)

    def IexDividendsItem(self, symbol, key, period, periodrange):
        logger.debug("IexDividendsItem called %s %s %d %s", symbol, key, period, periodrange)
        return get_dividends_item(symbol, key, period, periodrange)

    def IexDividendsTTM(self, symbol):
        logger.debug("IexDividendsTTM called %s", symbol)
        return get_dividends_ttm(symbol)

    def IexEarningsKeyCount(self):
        logger.debug("IexEarningsKeyCount called")
        return get_earnings_key_count()

    def IexEarningsKeyByIndex(self, index):
        logger.debug("IexEarningsKeyByIndex called %d", index)
        return get_earnings_keyx(index)

    def IexEarningsItem(self, symbol, key, period):
        logger.debug("IexEarningsItem called %s %s %d", symbol, key, period)
        return get_earnings_item(symbol, key, period)

    def IexHistoricalQuote(self, symbol, fordate):
        logger.debug("IexHistoricalQuote called %s %s", symbol, fordate)
        return get_closing_price(symbol, fordate)


# Configuration lock. Used to deal with the fact that sometimes
# LO Calc makes concurrent calls into the extension.
# dialog_lock = threading.Lock()
#
# def _check_configuration():
#     """
#     Force Intrinio configuration. Even if the configuration attempt
#     fails, we'll continue on because the request might hit cache.
#     Only if we need to call Intrinio will we fail the request.
#     :return: Returns True if Intrinio is configured. Otherwise,
#     returns False.
#     """
#     configured = QConfiguration.is_configured()
#
#     if not configured:
#         # Do not ask again is an automatic "not configured"
#         if QConfiguration.do_not_ask_again:
#             logger.debug("Configuration is not initialized and do not ask again is set")
#             return False
#
#         try:
#             if dialog_lock.acquire(blocking=False):
#                 logger.debug("Calling intrinio_login()")
#                 res = intrinio_login()
#                 logger.debug("Returned from intrinio_login()")
#                 if res[0]:
#                     # The return value is a tuple (True, username, password)
#                     QConfiguration.save(res[1], res[2])
#                 else:
#                     # The return value is a tuple (False, DoNotAskAgain)
#                     logger.error("intrinio_login() returned false")
#                     if res[1]:
#                         QConfiguration.do_not_ask_again = True
#                 configured = QConfiguration.is_configured()
#             else:
#                 logger.warn("Intrinio configuration dialog is already active")
#         except Exception as ex:
#             logger.error("Exception occurred trying to create configuraton: %s", str(ex))
#         finally:
#             dialog_lock.release()
#
#     return configured

#
# Boiler plate code for adding an instance of the extension
#

def createInstance( ctx ):
    return IexImpl( ctx )

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
    createInstance,"com.iex.api.localc.python.IexImpl",
        ("com.sun.star.sheet.AddIn",),)
