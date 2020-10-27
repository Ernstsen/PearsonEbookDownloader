# Origin 
Forked from [NoMod-Programming](https://github.com/NoMod-Programming/PearsonEbookDownloader)

# Usage

**TODO** Update this description. Project was forked as this no longer works

To use this utility, first log into the pearson website and access the E-Book. After about 10 seconds (or once the eText is loaded), copy the bookID parameter (anywhere from 5-6 digits long) and download it either using using the online downloader ("index.html" in this repository, and also available at https://NoMod-Programming.github.io/PearsonEbookDownloader/) or manually using python.


To use the python version, run this utility as follows:

	python3 downloader.py <bookid>

Where python3 points to the location of a python interpreter with the PyPDF2 module available (`pip install pypdf2`).

This will take a few minutes, downloading each individual page of the PDF (thanks, Pearson, for using *individual* pdf files for each page a thousand page book!) to a temporary directory, then merging them into a final PDF.

The output pdf will be saved into the current directory as `out.pdf`

**NOTE** the fully automated downloader no longer works. This means that it is no longer possible to download a book you have not paid for - as it should be.

This tool should only be used to obtain a readable version of the book, as the online reading version is still horrible. While possible, a pdf created using this code should never be shared.

## Donation
This is just an attempt at patching the original work - please consider supporting the original author:

*One more thing: If you found this script helpful, please recommend it to others or [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=epedemont%40protonmail.ch&currency_code=USD&source=url). I'd really appreciate it.*
