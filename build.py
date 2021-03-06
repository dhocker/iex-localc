#! /usr/local/bin/python3
#
# Package extension files into an .oxt file
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
# How to run a build:
#
# python3 build.py [next]
#
# where:
#   next option causes the build number to be incremented. This updates the src/description.xml file.
#

import os
import sys
import subprocess
import shutil
from xcu_file import XCUFile
import xml.etree.ElementTree as etree

# Set up environment vars
if sys.platform == 'darwin':
    # macOS
    os.environ["PATH"] = os.environ["PATH"] + ":/usr/lib/ure/bin/"
    os.environ["PATH"] = os.environ["PATH"] + ":/Users/dhocker/LibreOffice5.4_SDK/bin"
    os.environ["DYLD_LIBRARY_PATH"] = os.environ["OO_SDK_URE_LIB_DIR"]
else:
    # TODO figure out how to build on other OSes
    print ("Platform {0} is not supported by this build script".format(sys.platform))
    exit(1)
#subprocess.call("env")
#print (os.environ["DYLD_LIBRARY_PATH"])

# Recognized command line args
incr_version = len(sys.argv) == 2 and sys.argv[1].lower() == "next"

# Extract version from description.xml
tree = etree.parse("src/description.xml")
root = tree.getroot()
# There should only be one version node
nodes = root.findall('{http://openoffice.org/extensions/description/2006}version')
build_version = nodes[0].attrib["value"]

# Update build number as required
if incr_version:
    parts = build_version.split(".")
    build_num = parts[len(parts) - 1]
    build_num = str(int(build_num) + 1)
    parts[len(parts) - 1] = build_num
    build_version = str.join(".", parts)
    nodes[0].attrib["value"] = build_version
    # Note that this will rewrite the entire file and the results will likely
    # look substantially different.
    tree.write("src/description.xml", xml_declaration=False, encoding="utf-8",)
    print("Build number incremented")

print ("=============================")
print ("Building Version:", build_version)
print ("=============================")

# Clean build folder
print ("Cleaning build folder...")
shutil.rmtree("build")

# Create required build folders
if not os.path.exists("build"):
    print ("Creating new build folder")
    os.mkdir("build")
if not os.path.exists("build/META-INF"):
    print ("Creating build/META-INF folder")
    os.mkdir("build/META-INF")

# Compile idl
subprocess.run(["idlc", "-w", "idl/xiex.idl"], stdout=sys.stdout, stderr=sys.stderr)
subprocess.run(["regmerge", "-v", "build/xiex.rdb", "UCR", "idl/xiex.urd"])
os.remove("idl/xiex.urd")

# Copy all required files to build folder
print ("Copying files to build folder")
shutil.copy("src/manifest.xml", "build/META-INF/")
shutil.copy("src/description-en-US.txt", "build/")
shutil.copy("src/description.xml", "build/")
shutil.copy("src/iex_impl.py", "build/")
shutil.copy("src/iex_app_logger.py", "build/")
shutil.copy("src/iex_lib.py", "build/")
shutil.copy("src/iex_base.py", "build/")
shutil.copy("src/iex_stocks.py", "build/")
shutil.copy("src/iex_price.py", "build/")
shutil.copy("src/iex_quote.py", "build/")
shutil.copy("src/iex_company.py", "build/")
shutil.copy("src/iex_keystats.py", "build/")
shutil.copy("src/iex_dividends.py", "build/")
shutil.copy("src/iex_earnings.py", "build/")
shutil.copy("src/iex_chart.py", "build/")
shutil.copy("src/extn_helper.py", "build/")
shutil.copy("src/url_helpers.py", "build/")
shutil.copy("src/cache_db.py", "build/")
shutil.copy("certifi/cacert.pem", "build/")

# Generate the XCU file
print ("Generating iex.xcu")
xcu = XCUFile("com.iex.api.localc.python.IexImpl", "XIex")
#
# Note: DO NOT use underscores in parameter names. LO does not accept them.
# Note: Be careful using any special characters in descriptions and comments.
# This stuff ends up in an XML file and hence has all of the same restrictions.
# The xcu_file class escapes all descriptions in an attemp to avoid problems.
#
xcu.add_function("IexPrice", "Get stock price",
                 [
                     ('symbol', 'The stock ticker symbol.')
                 ])
xcu.add_function("IexQuoteKeyCount", "Get count of keys in a quote",
                 [
                 ])
xcu.add_function("IexQuoteKeyByIndex", "Get a quote key by its index",
                 [
                     ('keyindex', 'The key index where index < key count')
                 ])
xcu.add_function("IexQuoteItem", "Get a quote item by its key",
                 [
                     ('symbol', 'The stock ticker symbol for the quote'),
                     ('itemkey', 'The item key')
                 ])
xcu.add_function("IexCompanyKeyCount", "Get count of keys in a company",
                 [
                 ])
xcu.add_function("IexCompanyKeyByIndex", "Get a company key by its index",
                 [
                     ('keyindex', 'The key index where index < key count')
                 ])
xcu.add_function("IexCompanyItem", "Get a company item by its key",
                 [
                     ('symbol', 'The stock ticker symbol for the quote'),
                     ('itemkey', 'The item key')
                 ])
xcu.add_function("IexKeyStatsKeyCount", "Get count of keys in a key stats result",
                 [
                 ])
xcu.add_function("IexKeyStatsKeyByIndex", "Get a key stats key by its index",
                 [
                     ('keyindex', 'The key index where index < key count')
                 ])
xcu.add_function("IexKeyStatsItem", "Get a key stats item by its key",
                 [
                     ('symbol', 'The stock ticker symbol for the dividends'),
                     ('itemkey', 'The item key')
                 ])
xcu.add_function("IexDividendsKeyCount", "Get count of keys in a dividend period result",
                 [
                     ('symbol', 'The stock ticker symbol for the dividends'),
                     ('periodrange', 'See https://iextrading.com/developer/docs/#dividends')
                 ])
xcu.add_function("IexDividendsPeriodKeyCount", "Get count of periods in a period range",
                 [
                 ])
xcu.add_function("IexDividendsKeyByIndex", "Get a dividends key by its index",
                 [
                     ('keyindex', 'The key index where index < key count')
                 ])
xcu.add_function("IexDividendsItem", "Get a dividends item by its key",
                 [
                     ('symbol', 'The stock ticker symbol for the dividends'),
                     ('itemkey', 'The item key'),
                     ('period', 'The period within the period range, 0 to period count - 1'),
                     ('periodrange', 'See https://iextrading.com/developer/docs/#dividends')
                 ])
xcu.add_function("IexDividendsTTM", "Get trailing twelve months dividends",
                 [
                     ('symbol', 'The stock ticker symbol for the dividends'),
                     ('asofdate', 'As-of-date for TTM dividends')
                 ])
xcu.add_function("IexEarningsKeyCount", "Get count of keys in an earnings period result",
                 [
                     ('symbol', 'The stock ticker symbol for the earnings')
                 ])
xcu.add_function("IexEarningsKeyByIndex", "Get an earnings key by its index",
                 [
                     ('keyindex', 'The key index where index < key count')
                 ])
xcu.add_function("IexEarningsItem", "Get an earnings item by its key",
                 [
                     ('symbol', 'The stock ticker symbol for the quote'),
                     ('itemkey', 'The item key'),
                     ('period', 'The period within the period range, 0 to 3')
                 ])
xcu.add_function("IexHistoricalQuote", "Get a closing quote for a date",
                 [
                     ('symbol', 'The stock ticker symbol for the quote'),
                     ('fordate', 'The date YYYY-MM-DD')
                 ])

xcu.generate("build/iex.xcu")
xcu.dump_functions()

# Zip contents of build folder and rename it to .oxt
print ("Zipping build files into iex.oxt file")
os.chdir("build/")
for f in os.listdir("./"):
    if os.path.isfile(f) or os.path.isdir(f):
        subprocess.run(["zip", "-r", "iex.zip", f])
os.chdir("..")
shutil.move("build/iex.zip", "iex.oxt")
print ("Extension file iex.oxt created")

print ("============================================")
print ("Build complete for Version:", build_version)
print ("============================================")
