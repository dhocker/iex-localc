#
# iex_test - test harness for exercising LO extension functions outside
# of LO. LO does not provide any sort of debugging aids for Python based
# extensions, so this is used to compensate.
# Copyright © 2018  Dave Hocker (email: Qalydon17@gmail.com)
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
from iex_price import get_price
from iex_quote import get_quote
# import datetime
# import time
# import json
# Logger init

the_app_logger = AppLogger("iex-extension")
logger = the_app_logger.getAppLogger()

# print("Price")
# logger.info("Testing iex_price.get_price()")
# j = get_price("aapl")
# print ("Price for aapl:", j)

print("Quote")
logger.info("Testing iex_quote.get_quote()")
# v = get_quote("ibm", "latestPrice")
# print ("latestPrice for IBM:", v)
# v = get_quote("ibm", "change")
# print ("change for IBM:", v)
# v = get_quote("mmm", "latestPrice")
# print ("latestPrice for MMM:", v)
# v = get_quote("mmm", "change")
# print ("change for MMM:", v)

from iex_quote import quote_keys
for key in iter(quote_keys):
    v = get_quote("mmm", key)
    print (key, ":", v)
