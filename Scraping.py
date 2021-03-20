from bs4 import BeautifulSoup
import requests
from lxml import html

to_url = 'https://alphardic.com/media/'
response = requests.get('https://alphardic.com/media/')
print(response)

page_soup = BeautifulSoup(response.content, 'html.parser')
lxml_converted = html.fromstring(str(page_soup))

page_title = lxml_converted.xpath('//*[@id="st-text-logo"]/p/a')
print(page_title[0].text.replace("　","").replace(" ","").replace("\n",""))

for row in page_title:
    row.text