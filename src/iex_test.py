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
from iex_quote import get_quote_item, get_quote_key_count, get_quote_keyx
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

quote_key_count = get_quote_key_count()
print("Quote key count:", quote_key_count)
print("Quote Key/Value pair test")
for x in range(0, quote_key_count):
    key = get_quote_keyx(x)
    v = get_quote_item("mmm", key)
    print (key, ":", v)
print("Key index out of range test")
key = get_quote_keyx(quote_key_count + 1)
print(key)
print("Invalid key test")
v = get_quote_item("mmm", "invalid_key")
print(v)
