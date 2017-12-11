import os
import time
import urllib2
import shutil
import sys
import re
import twilio
from twilio.rest import Client

try:
	from bs4 import BeautifulSoup
	from bs4.element import Comment
except Exception as e:
	print "Are you sure you have BeautifulSoup installed? Enter 'pip install BeautifulSoup4' in the terminal to install."
	sys.exit()

def checkIfUpdated(url="http://example.com/", secondsInterval=5, filePrefix="example", compareText=False, useTwilio=False, phoneNumber="0"):

    account_sid = 'AC0bafa63942dbc2805fd2a5339342192a'
    auth_token = '324662f05f9d59c0a3479dd58b07356a'
    twilio_phone_number = '+15036104140'
    my_phone_number = "+" + re.sub("\D", "", phoneNumber) # remove non-digits from phone number

    # it's good practice to have headers
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)

    # file cleanup
    if (os.path.isfile(filePrefix + "_old.html")): 
        os.remove(filePrefix + "_old.html")
    if (os.path.isfile(filePrefix + "_new.html")): 
        os.remove(filePrefix + "_new.html")
    if (not os.path.isfile(filePrefix + "_saved.html")): # check if webpage has been scraped before
        saved_webpage = open(filePrefix + "_saved.html", "w+")
        saved_webpage.write(urllib2.urlopen(req).read())
        saved_webpage.close()

    while True:
        # load the webpage
        webpage = urllib2.urlopen(req)
        webpage_html = webpage.read();

        if (webpage.getcode() == 200): # make sure website returns an OK status code
            saved_webpage = open(filePrefix + "_saved.html", "r+")

            if (compareText): # compare the visible text of the pages
                webpageChanged = (text_from_html(saved_webpage.read()).encode('utf-8') != text_from_html(webpage_html).encode('utf-8'))
            else: # compare the raw html of the pages
                webpageChanged = (saved_webpage.read() != webpage_html)

            if (webpageChanged):
                print("Changes detected at " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "!")
                print("Compare " + filePrefix + "_old.html and " + filePrefix + "_new.html to see differences.")
    
                # make a copy of file_saved.html and name it file_old.html
                shutil.copyfile(filePrefix + "_saved.html", filePrefix + "_old.html")
                new_webpage = open(filePrefix + "_new.html", "w")
                new_webpage.write(webpage_html)
                new_webpage.close()

                # update file_saved.html
                saved_webpage.seek(0)
                saved_webpage.write(webpage_html)
                saved_webpage.close()

                # quit the program

                if (useTwilio): # text user
                    body = "The webpage at: " + url + " has updated!"
                    client = Client(account_sid, auth_token)
                    client.messages.create(
                        body=body,
                        to=my_phone_number,
                        from_=twilio_phone_number
                    )

                break
            else:
                print("No changes detected at " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ".")

                # update file_saved.html
                saved_webpage.seek(0)
                saved_webpage.write(webpage_html)
                saved_webpage.close()
        else:
            print("Error, could not fetch webpage. Status code: " + str(webpage.getcode()) + ".")

        # wait however many seconds specified
        time.sleep(secondsInterval)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

urlInput = str(raw_input("What url do you want to monitor for updates? "))
updateInput = int(raw_input("\nHow many seconds do you want to wait between checks (5 seconds minimum)? "))

if (updateInput < 5):
	print("Wait time too low. Page will be checked every 5 seconds.")
	updateInput = 5

filePrefixInput = str(raw_input("\nEnter an alphanumeric word (letters and numbers only). You should use a different word for every new website you want to check: "))
compareTextString = str(raw_input("\nDo you want to use the fancy method to check for updates to the page? (yes/no)\n(I recommend NOT using this method until you've tried the normal method first) "))

if (compareTextString.lower() == "yes" or compareTextString.lower() == "y"):
	compareTextBoolean = True
else:
	compareTextBoolean = False

useTwilioString = str(raw_input("\nDo you want to get a text when the webpage updates (yes/no)? "))

if (useTwilioString.lower() == "yes" or useTwilioString.lower() == "y"):
    useTwilioBoolean = True
    phoneNumberInput = str(raw_input("\nWhat phone number do you want texts to be sent to?\n(make sure to include the country code at the beginning) "))
else:
    useTwilioBoolean = False
    phoneNumberInput = "0";

print("")

checkIfUpdated(urlInput, updateInput, filePrefixInput, compareTextBoolean, useTwilioBoolean, phoneNumberInput)