# |====================================|
# |            BASH WAVE               |
# |          (realname tba)            |
# |           by gardotjar             |
# |====================================|

# Bash Wave (realname TBA) is a program that
# takes 3 random quotes from bash.org and then
# sends them to an email address.
# By using a neat trick with self-phone carriers
# Bash Wave (real name TBA) allows users to send
# these quotes to a cellphone via SMS.
# This way you can set it up on your pc before going
# somewhere with no internet, and you won't be so bored

# You'll have to fill in some information for this to work, so please complete the follow variables :
#(PS: I sugest using outlook for the email address, as google upped their anti script desu.

YourEmailAddress="AnAdress@ADomain.com"
YourEmailPassword="SuperSecretEmailPassword123"
PhoneEmailAddress="yourphonenumber@yourcarrier.net" # Cool trick, if you email the right address it'll send a text to your phone!
								 # in order to figure out the right address take a look at this link!
                                 # https://20somethingfinance.com/how-to-send-text-messages-sms-via-email-for-free/

# If at any point you have troubles getting this to work, which you probably will..
# or if you have troubles reading/modding my sloppy code...
# I can be reached at #aisuite or ##aisuite on freenode.



import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import random
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#
#   -------------------------------
#   This Part Defines The Functions
#   -------------------------------
#

def clean(quote) :
    raw_quote = quote.replace("Home / Latest / Browse /\n", "")
    raw_quote = raw_quote.replace("Random >0 / Top 100-200 /\n", "")
    raw_quote = raw_quote.replace("Add Quote / Search / ModApp\n", "")
    raw_quote = raw_quote.replace("Hosted by Idologic: high quality reseller and dedicated hosting.\n", "")
    raw_quote = raw_quote.replace("QDB 1999-2018, All Rights Reserved.\n", "")
    raw_quote = raw_quote.replace("QDB: Quote #"+str(quotenum)+"\n", "")
    raw_quote = raw_quote.replace("QDB\n", "")
    raw_quote = raw_quote.replace("Admin\n", "")
    raw_quote = raw_quote.replace("Paypal Donate\n", "")

    raw_quote = raw_quote.replace("Paypal Donate\n", "")
    raw_quote = raw_quote.replace("Home / Latest / Browse\n", "")
    raw_quote = raw_quote.replace("/ Top 100-200 / Add Quote\n", "")
    raw_quote = raw_quote.replace("/ Random >0\n", "")
    raw_quote = raw_quote.replace("/ ModApp / Search / #\n", "")

    raw_quote = raw_quote.replace("\n", "\n\n") # This line adds double spacing, remove it if you don't like that
    raw_quote = raw_quote.replace("[X]", "[X]\n")
    raw_quote = remove_last_line(raw_quote) # NEVER REMOVE THIS LINE. YOU'LL CAUSE AN ASCII FORMAT ERROR
    return raw_quote

# <Stuff I copy Pasted From Stack overflow.>
def remove_last_line(s):
    return s[:s.rfind('\n')]
# <\stuff I copy Pasted From Stack overflow.>

#
#   ------------------------------------
#   This Part Gets The Bash.org Quote(s)
#   ------------------------------------
#

quotes = []

count = 0
while True :
    # get the html
    quotenum = random.randrange(0,21064)
    url = "http://www.bash.org/?" + str(quotenum)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')] # Just incase someone tries to script block :P
    html = opener.open(url)
    soup = BeautifulSoup(html, "lxml")
    # clean it into plain text
    for script in soup(["script", "style"]):
        script.extract()
    # get the text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # Make sure it ain't a 404 error page
    if "does not exist." not in text :
        quotes.append(clean(text))
        count += 1
        if count >= 3 : # Puts three quotes together in order to cut down on the number of emails sent
            break
    else :
        print("404'ed")

quote_compilation = ""

for i in quotes :
    quote_compilation += i
    quote_compilation += "--------------------------" # seperate each quote from the other
print (quote_compilation)

#
#   ----------------------------------------
#   This Part Sends You A Text Msg Via Email
#   ----------------------------------------
#

username = YourEmailAddress 
password = YourEmailPassword

fromaddr = YourEmailAddress
toaddr = PhoneEmailAddress # The format for this should be PhoneNumber@PhoneCompaniesDomain.ca/com
                                 # you can find a list here: https://20somethingfinance.com/how-to-send-text-messages-sms-via-email-for-free/
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "" # You can add a subject but it'll just appear in brackets at the start of the text
body = quote_compilation
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
server.starttls()
server.login(username,password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
