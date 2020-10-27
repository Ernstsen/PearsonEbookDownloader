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

Also... Please don't use this for piracy. I paid for my online textbook, as should you, but I paid for a working textbook, not something that takes a minute to load each page of. While I can't stop you, please only use this utility if you have paid for the textbook.

## Donation
This is just an attempt at patching the original work - please consider supporting the original author:

*One more thing: If you found this script helpful, please recommend it to others or [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=epedemont%40protonmail.ch&currency_code=USD&source=url). I'd really appreciate it.*
