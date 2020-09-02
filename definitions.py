import requests
import os
from bs4 import BeautifulSoup

URL = 'https://www.dictionary.com/browse/QUERY?s=t'
path1 = "." + os.sep + "data" + os.sep + "words.txt"
path2 = "." + os.sep + "data" + os.sep + "dictionary.txt"

dictionary = []

with open(path1) as file:
    lines = file.readlines()
    for line in lines:
        query = line.replace("\n", "")
        print(query)
        query_url = URL.replace("QUERY", query)
        page = requests.get(query_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            definition = soup.find_all("span", class_="css-1p89gle")[0].text
            dictionary.append((query, definition))
        except IndexError:
            continue

with open(path2, "w") as file:
    for line in dictionary:
        text = line[0] + "|" + line[1] + "\n"
        file.write(text)
