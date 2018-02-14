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
    os.environ["PATH"] = os.environ["PATH"] + ":/Users/dhocker/LibreOffice5.3_SDK/bin"
    os.environ["DYLD_LIBRARY_PATH"] = os.environ["OO_SDK_URE_LIB_DIR"]
else:
    print ("Platform {0} is not supported by this build script".format(sys.platform))
    exit(1)
#subprocess.call("env")
#print (os.environ["DYLD_LIBRARY_PATH"])

# Extract version from description.xml
tree = etree.parse("src/description.xml")
root = tree.getroot()
nodes = root.findall('{http://openoffice.org/extensions/description/2006}version')
build_version = nodes[0].attrib["value"]
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
shutil.copy("src/iex_cache.py", "build/")
shutil.copy("src/extn_helper.py", "build/")
shutil.copy("src/url_helpers.py", "build/")
shutil.copy("certifi/cacert.pem", "build/")

# Generate the XCU file
print ("Generating iex.xcu")
xcu = XCUFile("com.iex.api.localc.python.IexImpl", "XIex")
#
# Note: DO NOT use underscores in parameter names. LO does not accept them.
#
xcu.add_function("IexPrice", "Get stock price",
                 [
                     ('symbol', 'The stock ticker symbol.')
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
print ("Build complete for version:", build_version)
print ("============================================")
