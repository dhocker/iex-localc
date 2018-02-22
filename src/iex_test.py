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
from iex_company import get_company_item, get_company_keyx, get_company_key_count
from iex_keystats import get_keystats_key_count, get_keystats_keyx, get_keystats_item
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

# print("Quote")
# logger.info("Testing iex_quote.get_quote()")
# v = get_quote("ibm", "latestPrice")
# print ("latestPrice for IBM:", v)
# v = get_quote("ibm", "change")
# print ("change for IBM:", v)
# v = get_quote("mmm", "latestPrice")
# print ("latestPrice for MMM:", v)
# v = get_quote("mmm", "change")
# print ("change for MMM:", v)

# quote_key_count = get_quote_key_count()
# print("Quote key count:", quote_key_count)
# print("Quote Key/Value pair test")
# for x in range(0, quote_key_count):
#     key = get_quote_keyx(x)
#     v = get_quote_item("mmm", key)
#     print (key, ":", v)
# print("Key index out of range test")
# key = get_quote_keyx(quote_key_count + 1)
# print(key)
# print("Invalid key test")
# v = get_quote_item("mmm", "invalid_key")
# print(v)

# company_key_count = get_company_key_count()
# print("Company key count:", company_key_count)
# print("Company Key/Value pair test")
# for x in range(0, company_key_count):
#     key = get_company_keyx(x)
#     v = get_company_item("mmm", key)
#     print (key, ":", v)
# print("Key index out of range test")
# key = get_company_keyx(company_key_count + 1)
# print(key)
# print("Invalid key test")
# v = get_company_item("mmm", "invalid_key")
# print(v)

key_count = get_keystats_key_count()
print("KeyStats key count:", key_count)
print("KyeStats Key/Value pair test")
for x in range(0, key_count):
    key = get_keystats_keyx(x)
    v = get_keystats_item("mmm", key)
    print (key, ":", v)
print("Key index out of range test")
key = get_quote_keyx(key_count + 1)
print(key)
print("Invalid key test")
v = get_quote_item("mmm", "invalid_key")
print(v)
