# LibreOffice Calc Extension for IEX
Copyright © 2018, 2019 by Dave Hocker as Qalydon

# DEPRECATED
Unfortunately, IEX has terminated the APIs that were used by this
LOCalc extension. Therefore, it has been deprecated.

## Overview
This project implements a LibreOffice Calc (LOCalc) addin extension that can
retrieve data from the Investor's Exchange (IEX) service.
Currently, only functions that are publicly available for free have been
implemented.

The LOCalc addin works on the Windows, macOS and Ubuntu versions of
[LibreOffice (version >= 5.0)](https://www.libreoffice.org/).

## Attribution
By using this extension, you agree to the
[IEX terms of service](https://iextrading.com/api-exhibit-a).

Data provided for free by [IEX](https://iextrading.com/developer).

## License
GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007. Refer to the
[LICENSE.md](https://github.com/qalydon/iex-localc/blob/master/README.md)
file for complete details.

## Before Installing

LibreOffice runs on multiple operating systems. For unknown reasons, the content of a LibreOffice install is
different depending on the operating system. In particular, LibreOffice ships with an embedded version of
Python and the configuration of the embedded version varies significantly.

### Windows

The IEX extension uses Sqlite3 to cache retrieved data. Unfortunately, the Windows version
of LibreOffice does not come with Sqlite3. If you want to use the IEX extension on Windows, you will
need to install a version of Python 3 that matches the Python version that comes
embedded in LibreOffice. After installing the full version of Python 3, 
set up PYTHONPATH according to your installation. See the prerequisite installation
instructions below.

### macOS

Some of the web services used by the IEX extension require secure connections through HTTPS.
The urllib package in the embedded version of Python does not recognize or use the CA certificates
installed under macOS. To compensate for this issue, the IEX extension includes the cacert.pem file from the
[certifi package](https://github.com/certifi/python-certifi).

## Installation

There are two major steps for installation.

1. Install/setup prerequisites.
1. Install the extension under LibreOffice

### Install and Setup Prerequisites

#### Windows

If you want to run the SMF Extension under Windows,
you need to install the full version of 
[Python 3](https://www.python.org/ftp/python/3.5.4/python-3.5.4-amd64.exe)
that is used with LibreOffice. For LibreOffice 6.2.8, Python 3.5.4
is required.
Be sure to note where you install it. For simplicity, you might consider
installing to C:\python35. **Be sure to install the 
x86_64 version (aka the 64-bit version).**

After you install Python 3.5.4, go to the Control Panel and set up the
PYTHONPATH variable. Open the menu and type **environment variables**.
This should lead you to the System Properties dialog box. Click on the
**Environment Variables** button.

Create a new **user** variable named PYTHONPATH. Set the value to the following.
```
c:\python35;c:\python35\Lib;c:\python35\Lib\site-packages;c:\python35\Lib\sqlite3;c:\python35\DLLs
```
This assumes you installed Python 3.5.4 to C:\python35. If you installed to a
different directory, adjust PYTHONPATH accordingly.

**After completing the Python installation and setup, it is strongly recommended 
that you reboot Windows.**

#### macOS

None.

### Install IEX Extension

1. Download the latest **iex.oxt** (the add-in file) from
[here](https://github.com/qalydon/iex-localc/releases).
1. Start LibreOffice or LibreOffice Calc.
1. From the Tools menu, open the Extension Manager.
1. Look through the list of installed add-ins for IEX.
If you find it, click the Remove button to remove it.
For best results, **remove an existing IEX
add-in first**.
1. Click the Add button.
1. Navigate to the location where you downloaded **iex.oxt**.
Select it.
1. Choose if you want the add-in installed for you or everyone.
1. Click the Close button.
1. If LibreOffice asks to restart, do so.

**It is recommended that you always remove an existing version of the
add-in before installing an update. Othwerwise, your results may be
unpredictable.**

## Example Files
You can find a number of example files in the
[examples folder](https://github.com/qalydon/iex-localc/tree/master/examples).
These files show you how most of the LOCalc Extension functions
can be used.

## LOCalc Functions
The addin provides a number of functions for retrieving data from
the IEX service. The IEX service organizes its API functions in
a number of categories. Each [API category](https://iextrading.com/developer/docs/#stocks)
contains a number of data items that are identified by name. The following
categories are currently supported.

* Company
* Quote
* Key Stats
* Dividends
* Earnings
* Price
* Chart (historical data)

The LOCalc addin generally provides three
functions for each category (there are some exceptions).

* A function to return the number of item keys that are available for
a given category.
* A function to return the item key name for each available item.
* A function to return the value of an item.

This model of operation enables you to first determine how many values
are available, then determine the key name of each value and finally,
retrieve the value of each key. Thus you can discover what data is
available without looking at the documentation on the IEX site.

For example, the [Company](https://iextrading.com/developer/docs/#company)
category contains 9 items and looks something like this.

```
{
  "symbol": "AAPL",
  "companyName": "Apple Inc.",
  "exchange": "Nasdaq Global Select",
  "industry": "Computer Hardware",
  "website": "http://www.apple.com",
  "description": "Apple Inc...",
  "CEO": "Timothy D. Cook",
  "issueType": "cs",
  "sector": "Technology",
}
```

### Company
Reference: [Company](https://iextrading.com/developer/docs/#company).
#### IEXCompanyKeyCount
Returns the number of item keys in the Company category.
```
=IEXCompanyKeyCount()
```
#### IEXCompanyKeyByIndex
Returns the key name for the nth key in a Company.
```
=IEXCompanyKeyByIndex(index)
```

index: a value in the range 0 to IEXCompanyKeyCount() - 1 (i.e. 0 to 8)

#### IEXCompanyItem
Use the IEXCompanyItem function to retrieve company information for a ticker
symbol. See [Company](https://iextrading.com/developer/docs/#company)
```
=IEXCompanyItem(symbol, item)
```

symbol: The stock ticker symbol whose company information is to be retrieved.

item: The name of the company item to be retrieved.

### Quote
Reference: [Quote](https://iextrading.com/developer/docs/#quote).
#### IEXQuoteKeyCount
Returns the number of item keys in the Quote category.
```
=IEXQuoteKeyCount()
```
#### IEXQuoteKeyByIndex
Returns the key name for the nth key in a Quote.
```
=IEXQuoteKeyByIndex(index)
```

index: a value in the range 0 to IEXQuoteKeyCount() - 1 (i.e. 0 to 35)

#### IEXQuoteItem
Use the IEXQuoteItem function to retrieve quote information for a ticker
symbol. See [Quote](https://iextrading.com/developer/docs/#quote)
```
=IEXQuoteItem(symbol, item)
```

symbol: The stock ticker symbol whose quote is to be retrieved.

item: The name of the quote item to be retrieved.

### Key Stats
Reference: [Stats](https://iextrading.com/developer/docs/#key-stats).
#### IEXKeyStatsKeyCount
Returns the number of item keys in the Key Stats category.
```
=IEXKeyStatsKeyCount()
```
#### IEXKeyStatsKeyByIndex
Returns the key name for the nth key in a Key Stats.
```
=IEXKeyStatsKeyByIndex(index)
```

index: a value in the range 0 to IEXKeyStatsKeyCount() - 1 (i.e. 0 to 49)

#### IEXKeyStatsItem
Use the IEXKeyStatsItem function to retrieve significant statistics
for a ticker symbol. See [key stats](https://iextrading.com/developer/docs/#key-stats)
```
=IEXKeyStatsItem(symbol, item)
```

symbol: The stock ticker symbol whose key stats are to be retrieved.

item: The name of the statistic item to be retrieved.

### Dividends
Reference: [Dividends](https://iextrading.com/developer/docs/#dividends).

#### IEXDividendsKeyCount
Returns the number of item keys in the Dividends category.
```
=IEXDividendsKeyCount()
```

#### IEXDividendsPeriodCount
Returns the number of periods in the period range.
```
=IEXDividendsPeriodCount(symbol, periodrange)
```

symbol: The stock ticker symbol whose dividends are to be retrieved.

periodrange: The time range of interest. See
[Dividends](https://iextrading.com/developer/docs/#dividends). The period
range is a string value. Current period ranges are: 5y, 2y, 1y, ytd,
6m, 3m, 1m.

#### IEXDividendsKeyByIndex
Returns the key name for the nth key in a Dividends period.
```
=IEXDividendsKeyByIndex(index)
```

index: a value in the range 0 to IEXDividendsKeyCount() - 1 (i.e. 0 to 8)

#### IEXDividendsItem
Use the IEXDividendsItem function to retrieve information about dividends
for a ticker symbol. See [Dividends](https://iextrading.com/developer/docs/#dividends).
```
=IEXDividendsItem(symbol, item, period, periodrange)
```

symbol: The stock ticker symbol whose dividends are to be retrieved.

item: The name of the dividend item to be retrieved.

period: The period within the period range. Periods are numbered 0-n
where period 0 is the most recent period.

periodrange: The time range of interest. See
[Dividends](https://iextrading.com/developer/docs/#dividends). The period
range is a string value. Current period ranges are: 5y, 2y, 1y, ytd,
6m, 3m, 1m.

#### IEXDividendsTTM
Use the IEXDividendsTTM function to retrieve the trailing twelve months
dividends for a ticker symbol. This function simplifies the task of
determining a full twelve months of dividends.
```
=IEXDividendsTTM(symbol [, asofdate])
```

symbol: The stock ticker symbol whose dividends are to be retrieved.

asofdate: The end date of the 12 month period as a string (YYYY-MM-DD) 
or LOCalc date type (=date(YYYY,MM,DD)). For example, if you specified
2019-02-28 you would get the total dividends from the period 2018-03-01
to 2019-02-28. 
If the date is omitted, the current date is used.

Since historical data of this nature is static, it is persistently 
cached in an SQLite database. This limits the calls to the IEX service.

### Earnings
Reference: [Earnings](https://iextrading.com/developer/docs/#earnings).

#### IEXEarningsKeyCount
Returns the number of item keys in the Earnings category.
```
=IEXEarningsKeyCount()
```

#### IEXEarningsKeyByIndex
Returns the key name for the nth key in an Earnings period.
```
=IEXEarningsKeyByIndex(index)
```

index: a value in the range 0 to IEXEarningsKeyCount() - 1 (i.e. 0 to 8)

#### IEXEarningsItem
Use the IEXEarningsItem function to retrieve information about earnings
for a ticker symbol. See [Earnings](https://iextrading.com/developer/docs/#earnings).
```
=IEXEarningsItem(symbol, item, period)
```

symbol: The stock ticker symbol whose earnings are to be retrieved.

item: The name of the earnings item to be retrieved.

period: The period within the period range. Periods are numbered 0-3
where period 0 is the most recent period.

symbol: The stock ticker symbol whose earnings are to be retrieved.

### Price
Reference: [Price](https://iextrading.com/developer/docs/#price).
#### IEXPrice
Use the IEXPrice function to retrieve the current price for a ticker
symbol. Note that this function does not follow the typcial three
function model.
```
=IEXPrice(symbol)
```

symbol: The stock ticker symbol whose price is to be retrieved.

### Chart
Reference: [Chart](https://iextrading.com/developer/docs/#chart).

The chart category appears to be designed for constructing historical
charts. However, it can be useful for a number of historical data queries.

#### IEXHistoricalQuote
Use the IEXHistoricalQuote function to retrieve the closing price quote for a ticker
symbol on a given date. Note that this function does not follow the typcial three
function model.
```
=IEXHistoricalQuote(symbol, fordate)
```

symbol: The stock ticker symbol whose price is to be retrieved.

fordate: The desired date as a string (YYYY-MM-DD) or LOCalc date type
(=date(YYYY,MM,DD)).

Since historical price quotes do not change, they are persistently cached in an
SQLite database. This limits the calls to the IEX service.

## References
* [IEX Web Site](https://iextrading.com/)
* [Developer Docs](https://iextrading.com/developer/docs/)
* [LibreOffice Web Site](https://www.libreoffice.org/)