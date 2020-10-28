#! /usr/bin/env python3
import base64
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

import urllib.parse
import tempfile
import json
import urllib.request
import os
import sys
import re

from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject, DictionaryObject, ArrayObject, NumberObject

from multiprocessing.pool import ThreadPool

language = "en_US"
roletypeid = 2  # 3 for instructor, though the server doesn't seem to care

arabicRegex = re.compile(r"^(?P<prefix>.*?)(\d+)$")
romanRegex = re.compile(
    r"^(?P<prefix>.*?)((?:(M{1,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})|M{0,4}(CM|C?D|D?C{1,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|X?L|L?X{1,3})(IX|IV|V?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|I?V|V?I{1,3})))+)$",
    re.IGNORECASE)

bookmarkInfoUrl = "https://auth.ebookplus.pearsoncmg.com/ebook/pdfplayer/getbaskettocinfo?userroleid={userroleid}&bookid={bookid}&language={language}&bookeditionid={bookeditionid}&basket=all&ispreview=Y&scenarioid={scenarioid}"


def main():

    print("Loading metadata and eText information...")

    with open("bookinfo.json", 'r') as bookInfoRequest:
        str_response = bookInfoRequest.read()
        bookInfo = json.loads(str_response)
        bookInfo = bookInfo[0]['userBookTOList'][0]

    with open("pageinfo.json", 'r') as pageInfoRequest:
        pageInfo = json.loads(pageInfoRequest.read())
        pageInfo = pageInfo[0]['pdfPlayerPageInfoTOList']

    with open("pages.json", 'r') as file:
        downloadedData = json.loads(file.read())[0]["pdfPlayerPageInfoTOList"]

    def get_data(page_id):
        b = next((x['data'] for x in downloadedData if x['pageID'] == page_id), None)
        return bytearray(base64.standard_b64decode(b[len("data:application/pdf;base64,"):]))

    with tempfile.TemporaryDirectory() as pdfDownloadDir:
        # Use a temporary directory to download all the pdf files to
        # First, download the cover file
        pdfPageTable = {}

        pdf_page_label_table = {}

        # urllib.request.urlretrieve(getPageUrl(bookInfo['pdfCoverArt'], isCover="Y"), os.path.join(pdfDownloadDir, "0000 - cover.pdf"))
        with open(os.path.join(pdfDownloadDir, "0000 - cover.pdf"), 'w+b') as ous:
            ous.write(get_data(pageInfo[0]['pageID']))

        # Then, download all the individual pages for the e-book
        def download(pdfPage):
            pdfPageTable[pdfPage['bookPageNumber']] = pdfPage['pageOrder']
            savePath = os.path.join(pdfDownloadDir,
                                    "{:04} - {}.pdf".format(pdfPage['pageOrder'], pdfPage['bookPageNumber']))
            with open(savePath, 'w+b') as out:
                out.write(get_data(pdfPage['pageID']))
            # urllib.request.urlretrieve(getPageUrl(pdfPage['pdfPath']), savePath)

        threadPool = ThreadPool(40)  # 40 threads should download a book fairly quickly
        print("Reading pages from pageinfo.json to \"{}\"...".format(pdfDownloadDir))
        threadPool.map(download, pageInfo)

        print("Assembling PDF...")

        # Begin to assemble the final PDF, first by adding all the pages
        fileMerger = PdfFileWriter()
        for pdfFile in sorted(os.listdir(pdfDownloadDir)):
            page = PdfFileReader(os.path.join(pdfDownloadDir, pdfFile)).getPage(0)
            os.remove(os.path.join(pdfDownloadDir, pdfFile))  # Save on memory a bit
            fileMerger.addPage(page)

        bookmarksExist = True

        # TODO: Bookmarks currently not supported
        with open("bookmarks.json", 'r') as bookmarkInfoRequest:
            try:
                bookmarkInfo = json.loads(bookmarkInfoRequest.read())
                bookmarkInfo = bookmarkInfo[0]['basketsInfoTOList'][0]
            except Exception as e:
                bookmarksExist = False

        def recursiveSetBookmarks(aDict, parent=None):
            if isinstance(aDict, dict):
                aDict = [aDict]
            for bookmark in aDict:
                # These are the main bookmarks under this parent (or the whole document if parent is None)
                bookmarkName = bookmark['name']  # Name of the section
                pageNum = str(bookmark['linkvalue']['content'])  # First page (in the pdf's format)

                latestBookmark = fileMerger.addBookmark(bookmarkName, pdfPageTable[pageNum], parent)

                if 'basketentry' in bookmark:
                    recursiveSetBookmarks(bookmark['basketentry'], latestBookmark)

        if bookmarksExist:
            print("Adding bookmarks...")
            fileMerger.addBookmark("Cover", 0) # Add a bookmark to the cover at the beginning
            recursiveSetBookmarks(bookmarkInfo['document'][0]['basketcollection']['basket']['basketentry'])
        else:
            print("Bookmarks don't exist for book")
        print("Fixing metadata...")
        # Hack to fix metadata and page numbers:
        pdf_page_label_table = [(v, k) for k, v in pdfPageTable.items()]
        pdf_page_label_table = sorted(pdf_page_label_table, key=(lambda x: int(x[0])))
        labels = ArrayObject([
            NameObject(0), DictionaryObject({NameObject("/P"): NameObject("(cover)")})
        ])
        last_mode = None
        last_prefix = ""
        # Now we check to see the ranges where we have roman numerals or arabic numerals
        # The following code is not ideal for this, so I'd appreciate a PR with a better solution
        for pageNumber, pageLabel in pdf_page_label_table:
            curr_mode = None
            prefix = ""
            style = DictionaryObject()
            if arabicRegex.match(pageLabel):
                curr_mode = "arabic"
                prefix = arabicRegex.match(pageLabel).group("prefix")
                style.update({NameObject("/S"): NameObject("/D")})
            elif romanRegex.match(pageLabel):
                curr_mode = "roman"
                prefix = romanRegex.match(pageLabel).group("prefix")
                style.update({NameObject("/S"): NameObject("/r")})
            if curr_mode != last_mode or prefix != last_prefix:
                if prefix:
                    style.update({
                        NameObject("/P"): NameObject("({})".format(prefix))
                    })
                labels.extend([
                    NumberObject(pageNumber),
                    style,
                ])
                last_mode = curr_mode
                last_prefix = prefix
        root_obj = fileMerger._root_object
        # Todo: Fix the weird page numbering bug
        pageLabels = DictionaryObject()
        # fileMerger._addObject(pageLabels)
        pageLabels.update({
            NameObject("/Nums"): ArrayObject(labels)
        })
        root_obj.update({
            NameObject("/PageLabels"): pageLabels
        })

        print("Writing PDF...")
        with open("{}.pdf".format(bookInfo['title']).replace("/", "").replace(":", "_"), "wb") as outFile:
            fileMerger.write(outFile)


if __name__ == '__main__':
    #TODO: Consider checking if files exists, as to avoid nasty crash if they do not
    main()
