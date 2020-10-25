"""
This script crawls addresses for supermarkets from https://www.meinprospekt.de/filialen/SUPERMARKET-NAME 
for specific supermarket companies as per defined below.

Results are saved into a csv file at the script directory. - Happy crawling.
"""

import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import os
from datetime import date
import re
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__)) # get current file path for saving excel to same path later

def remove_umlaut(string): # function to remove german typical characters
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string

# target urls
url = ["https://www.meinprospekt.de/filialen/rewe-de/", "https://www.meinprospekt.de/filialen/lidl/", "https://www.meinprospekt.de/filialen/aldisued-de/", \
    "https://www.meinprospekt.de/filialen/aldinord-de/", "https://www.meinprospekt.de/filialen/penny-de/", "https://www.meinprospekt.de/filialen/netto-marken-discount-de/", \
    "https://www.meinprospekt.de/filialen/norma-de/", "https://www.meinprospekt.de/filialen/real-de/", "https://www.meinprospekt.de/filialen/edeka/", \
    "https://www.meinprospekt.de/filialen/edekacenter-de/", "https://www.meinprospekt.de/filialen/kaufland/", "https://www.meinprospekt.de/filialen/netto1-de/"]

# bs4 setup
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'  # user agent
headers = {'User-Agent': user_agent}  # add user agent to request header

address_list = []  # define list for table cell content

for supermarkt_url in url: # crawl for each supermarket chain url
    
    # create url range for further sub-sites
    url_range = []
    url_range.append(supermarkt_url)
    for i  in range(0,10):
        url_range.append(supermarkt_url + str(i))

    counter = 0

    # crawl each site for each supermarket chain
    for i_url in url_range:    
        # request url content and read / parse response html
        request = urllib.request.Request(i_url, None, headers=headers)
        
        try:
            response = urllib.request.urlopen(request)

            html = response.read().decode('utf-8', 'ignore')
            soup = BeautifulSoup(html, "html.parser")
    
            soup_result = soup.find_all("a", {"class":"mp-address"})  # find addresses

            for i in soup_result:
                i = str(i)
                supermarket_regex = re.compile(r'title=".*"') # find address in found class based on item title
                reg_result = supermarket_regex.search(i)
                try:
                    x = remove_umlaut(reg_result.group()[7:-1])
                    x = x.replace("&amp", "und")
                    address_list.append(x)
                    counter += 1
                except AttributeError:
                    pass
        except HTTPError:
            pass

    print(f"{counter} for {supermarkt_url}") # print number of addresses for each supermarket
        
df = pd.DataFrame(data=address_list, columns=["Address"])
df.drop_duplicates(inplace=True)

print(f"Supermarket addresses found: {df.shape}") # total number of addresses

today = date.today()
today_date = today.strftime(r"%Y%m%d")

df["Address"].to_csv(f"{dir_path}\\{today_date}_supermarkt_filialen.csv", header=False, index=False)  # save data to excel
print(f"File printed to {dir_path}!") # show file location
