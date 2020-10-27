let list = []//Output from index.html thing %TODO: Formalize
let bookId = "CM86156425/"
convertBlobToBase64 = blob => new Promise((resolve, reject) => {
    const reader = new FileReader;
    reader.onerror = reject;
    reader.onload = () => {
        resolve(reader.result);
    };
    reader.readAsDataURL(blob);
});

save = function (data, filename) {
    if (!data) {
        console.error('Console.save: No data')
        return;
    }

    if (!filename) filename = 'story.json'

    if (typeof data === "object") {
        data = JSON.stringify(data, undefined, 4)
    }

    var blob = new Blob([data], {
            type: 'text/json'
        }),
        e = document.createEvent('MouseEvents'),
        a = document.createElement('a')

    a.download = filename
    a.href = window.URL.createObjectURL(blob)
    a.dataset.downloadurl = ['text/json', a.download, a.href].join(':')
    e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
    a.dispatchEvent(e)
}

for (idx = 0; idx < list[0].pdfPlayerPageInfoTOList.length; idx++) {
    list[0].pdfPlayerPageInfoTOList[idx].data = await fetch(
        "https://etext.pearson.com/eplayer/ebookassets/prod1/ebook" + bookId + "/"  + list[0].pdfPlayerPageInfoTOList[idx].pdfPath,
        {
            headers: {
                'x-requested-with': 'pearsonEbookDownloader',
                'cors-origin-set': 'https://etext.pearson.com',
                'Origin': 'https://etext.pearson.com'
            }
        }).then(resp => resp.blob()).then(convertBlobToBase64);
}

save(list, "pages.json")