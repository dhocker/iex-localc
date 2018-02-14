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
    from iex_price import get_price
    # from iex_lib import QConfiguration
    # from intrinio_access import intrinio_login, is_valid_identifier, get_data_point, \
    #     get_historical_prices, get_historical_data, get_news, get_fundamentals_data, get_tags, \
    #     get_financials_data, get_reported_fundamentals_data, get_reported_tags, get_reported_financials_data, \
    #     get_usage
    # from iex_cache import UsageDataCache
    # from intrinio_indices import get_indices_by_query_count, get_indices_by_query, get_indices_by_query_tag_count, \
    #     get_indices_by_query_tag, get_index_by_identifier_tag_count, get_index_by_identifier_tag, \
    #     get_index_by_identifier
    # from intrinio_companies import get_companies_by_query, get_companies_by_query_count, get_companies_by_query_tag_count, \
    #     get_companies_by_query_tag, get_company_by_identifier, get_company_by_identifier_tag_count, \
    #     get_company_by_identifier_tag
    # from intrinio_securities import get_securities_by_query, get_securities_by_query_count, \
    #     get_securities_by_query_tag_count, get_securities_by_query_tag, get_security_by_identifier, \
    #     get_security_identifier_tag_count, get_security_identifier_tag
    # from intrinio_company_sec_filings import get_company_sec_filings, get_company_sec_filings_count, \
    #     get_company_sec_filings_tag_count, get_company_sec_filings_tag
    # from extn_helper import date_str_to_float
    import xml.etree.ElementTree as etree

    # Logger init
    the_app_logger = AppLogger("iex-extension")
    logger = the_app_logger.getAppLogger()
    # Extract version from description.xml
    tree = etree.parse(cmd_folder + "/description.xml")
    root = tree.getroot()
    nodes = root.findall('{http://openoffice.org/extensions/description/2006}version')
    logger.info("Iex-LOCalc Version: %s", nodes[0].attrib["value"])
except Exception as ex:
    # Emergency debugging to cover for the fact that LibreOffice is terrible at debugging...
    fh = open("/Volumes/Z77ExtremeDataSSD/dhocker/libreoffice/iex/error_report.txt", "w")
    fh.write(ex)
    fh.write(str(ex))
    fh.close()
    exit(666)

class IexImpl(unohelper.Base, XIex ):
    """Define the main class for the Intrinio LO Calc extension """
    def __init__( self, ctx ):
        self.ctx = ctx
        logger.debug("IexImpl initialized")
        logger.debug("self: %s", str(self))
        logger.debug("ctx: %s", str(ctx))

    def IexPrice(self, symbol):
        logger.debug("IexPrice called")
        return get_price(symbol)


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
