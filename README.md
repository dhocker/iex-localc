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
the IEX service.

### Function
Use function to retrieve information about
```
=Function(category, item)
```

## References
* [IEX Web Site](https://iextrading.com/)
* [LibreOffice Web Site](https://www.libreoffice.org/)