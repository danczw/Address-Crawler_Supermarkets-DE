# -*- coding: iso-8859-1 -*-

"""
This script crawls addresses for supermarkets from https://www.meinprospekt.de/filialen/SUPERMARKET-NAME 
for specific supermarket companies as per defined below.

Results are saved into a csv file at the script directory. - Happy crawling.
"""

# TODO: work on coding to handle öäü

import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import os
import re
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__)) # get current file path for saving excel to same path later

url = ["https://www.meinprospekt.de/filialen/rewe-de/", "https://www.meinprospekt.de/filialen/lidl/", "https://www.meinprospekt.de/filialen/aldisued-de/", \
    "https://www.meinprospekt.de/filialen/aldinord-de/", "https://www.meinprospekt.de/filialen/penny-de/", "https://www.meinprospekt.de/filialen/netto-marken-discount-de/", \
    "https://www.meinprospekt.de/filialen/norma-de/", "https://www.meinprospekt.de/filialen/real-de/", "https://www.meinprospekt.de/filialen/edeka/", \
    "https://www.meinprospekt.de/filialen/edekacenter-de/", "https://www.meinprospekt.de/filialen/kaufland/", "https://www.meinprospekt.de/filialen/netto1-de/"]  # target urls

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'  # user agent
headers = {'User-Agent': user_agent}  # add user agent to request header

address_list = []  # define list for table cell content

for supermarkt_url in url:
    url_range = []
    url_range.append(supermarkt_url)
    
    # create url range for further websites
    for i  in range(0,10):
        url_range.append(supermarkt_url + str(i))

    filial_list = []

    for i_url in url_range:    
        # request url content and read / parse response html
        request = urllib.request.Request(i_url, None, headers=headers)
        
        try:
            response = urllib.request.urlopen(request)

            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
    
            soup_result = soup.find_all("a", {"class":"mp-address"})  # find addresses

            for i in soup_result:
                i = str(i)
                supermarket_regex = re.compile(r'title=".*"')
                reg_result = supermarket_regex.search(i)
                try:
                    filial_list.append(reg_result.group()[7:-1])
                    address_list.append(reg_result.group()[7:-1])
                except AttributeError:
                    filial_list.append("EXCEPT ATTRIBUTE ERROR")
        except HTTPError:
            pass

    print(f"{len(filial_list)} for {supermarkt_url}")
        
print(f"Filialen gefunden: {len(address_list)}")

df = pd.DataFrame(data=address_list, columns=["Address"])
df.to_csv(f"{dir_path}\\supermarkt_filialen.csv", sep=";")  # save data to excel
print(f"Excel printed to {dir_path}!") # show file location