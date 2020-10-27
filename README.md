# Origin 
Forked from [NoMod-Programming](https://github.com/NoMod-Programming/PearsonEbookDownloader)

# Usage

## Part 1 : Javascript
To use this utility, first log into the pearson website and access the E-Book. After about 10 seconds (or once the eText is loaded), copy the bookID parameter (anywhere from 5-6 digits long) and download it either using using the online downloader ("index.html" in this repository, and also available at https://NoMod-Programming.github.io/PearsonEbookDownloader/).
The first two boxes will be filled with information, while the third one sadly fails. 

- The leftmost one should be copied to a file, saved as ``bookInfo.json``
- The second one (middle) should be copied to a file, saved as ``pageinfo.json``

Now go to ``scripts/pasteToBrowser.js`` and copy the entire file. This should then be pasted into the developer console, with the following changes:

- ``list`` should be set to the entire content of the file ``pageinfo.json``
- ``bookId`` should be set to the field ``globalBookID`` from the file ``bookinfo.json``  

The file which is then downloaded should then be copied to this root folder, with the other json files, and be named ``pages.json``

## Part 2 : Python
*Pre-requisite:* Python 3.x with the package PyPDF2 installed (``pip install pypdf2``)

Run the python script ``python downloader.py``, which should then read the files, and compile a .pdf

The output pdf will then be saved into the current directory.

**NOTE** the fully automated downloader no longer works. This means that it is no longer possible to download a book you have not paid for - which is as it should be.

Also note that this technically is no longer a downloader, as the script in itself no longer downloads the book from the server.

This tool should only be used to obtain a readable version of the book, as the online reading version is still horrible. While possible, a pdf created using this code should never be shared.

## Donation
This is just an attempt at patching the original work - please consider supporting the original author:

*One more thing: If you found this script helpful, please recommend it to others or [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=epedemont%40protonmail.ch&currency_code=USD&source=url). I'd really appreciate it.*
