# LibreOffice Calc Extension for IEX
Copyright © 2018 by Dave Hocker as Qalydon

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

## Download
Download the latest **iex.oxt** (the add-in file) from
[here](https://github.com/qalydon/iex-localc/releases).

## Installation
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

It is recommended that you always remove an existing version of the
add-in before installing an update. Othwerwise, your results may be
unpredictable.

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
categories are supported.

* Company
* Quote
* Key Stats
* Price

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
Returns the key name for the nth key in a Quote.
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
Returns the key name for the nth key in a Quote.
```
=IEXKeyStatsKeyByIndex(index)
```

index: a value in the range 0 to IEXKeyStatsKeyCount() - 1 (i.e. 0 to 49)

#### IEXKeyStatsItem
Use the IEXKeyStatsItem function to retrieve significant statistics
for a ticker symbol. See [price](https://iextrading.com/developer/docs/#key-stats)
```
=IEXKeyStatsItem(symbol, item)
```

symbol: The stock ticker symbol whose quote is to be retrieved.

item: The name of the statistic item to be retrieved.

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

## References
* [IEX Web Site](https://iextrading.com/)
* [LibreOffice Web Site](https://www.libreoffice.org/)