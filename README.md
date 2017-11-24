# webScraper-Seth
Monitor a website for changes.

## How to run

`git clone https://github.com/Fantop/webScraper-Seth.git` or download and extract the zip.

`cd webScraper-Seth`

`pip install BeautifulSoup4`

`python webScraper.py`

Press control-c to exit the program at any time.


Example:
![example](https://i.cubeupload.com/WeFVCp.png)

## Notes

* Make sure you are running Python 2. Use `python --version` to check.
* Make sure you are giving a unique word for every url you are checking. This is necessary because the program stores copies of the page's html and needs unique file names when it saves these.
* I did not write the function that parses the visible text from the HTML. Rest of the code is completely original.