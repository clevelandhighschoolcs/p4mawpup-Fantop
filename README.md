# webScraper-Seth
Monitor a website for changes.

## How to run

`git clone https://github.com/clevelandhighschoolcs/p4mawpup-Fantop.git` or download and extract the zip.

`cd p4mawpup-Fantop`

`pip install BeautifulSoup4` and `pip install twilio`

Or alternatively `pip install -r requirements.txt`

`python webScraper.py`

Press control-c to exit the program at any time.


Example:

![example](https://image.ibb.co/dR1BkR/example.png)

Flowchart:

![flowchart](https://raw.githubusercontent.com/clevelandhighschoolcs/p4mawpup-Fantop/master/flowchart.png)

## Algorithm
When the program is run, one of two different algorithms can be used to check if the webpage has been updated. The simple algorithm checks that the old html and new html are equal; looking for any difference in the two strings of html. If the strings are not equal, the page has been updated. The fancy algorithm parses any visible text from the old and new html, then it checks that these two strings of parsed text are equal. Again, if the strings are not equal, the page has been updated.

## Notes

* Make sure you are running Python 2.7.x. Use `python --version` to check.
* Make sure you are giving a unique word for every url you are checking. This is necessary because the program stores copies of the page's html and needs unique file names when it saves these.
* I did not write the function that parses the visible text from the HTML. Credit goes to [jbochi](https://stackoverflow.com/users/230636/jbochi). Rest of the code is completely original.
