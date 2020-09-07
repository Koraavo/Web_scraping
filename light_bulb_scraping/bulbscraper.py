"https://www.lightup.com/standard-household-lighting.html"
# always check robots.txt for each file
# for this website: it is https://www.lightup.com/robots.txt
# when user_agent = * it means everyone is allowed
    # no headers therefore required to trick the site

import requests
from bs4 import BeautifulSoup
import json
import re


# # this is used to save the site page in an html format for the first time
# base_url = "https://www.lightup.com/standard-household-lighting.html"


# # WRITE FILE
# response = requests.get(base_url)
# with open('bulbs.html', 'w') as html_file:
#     html_file.write(response.text)

# # READ FILE
response = ""
with open('bulbs.html', 'r') as html_file:
    for line in html_file.read():
        response += line

# print(response)
def parse(response):
    content = BeautifulSoup(response, 'lxml')
    title = [title.find('a')['title'] for title in content.findAll("h2", {"class": "product-name"})]
    links = [link.find('a')['href'] for link in content.findAll("h2", {"class": "product-name"})]
    models = [model.text for model in content.findAll("div", {"class": "product-list-sku"})if 'MPN' in model.text]
    skus = [sku.text for sku in content.findAll("div", {"class": "product-list-sku"})if 'SKU' in sku.text]
    prices = [price.text.strip() for price in content.findAll("span", {"class": "regular-price"})]
    details = [detail.find("ul").findAll("li") for detail in content.findAll("div", {"class": "desc std"})]
    bases = ["".join([base.text.strip() for base in detail if 'Base' in base.text]) for detail in details]
    brand = ["".join([brand.text.strip() for brand in detail if 'Brand' in brand.text]) for detail in details]
    wattage = ["".join([wattage.text.strip() for wattage in detail if 'Wattage' in wattage.text]) for detail in details]
    watt_equi = ["".join([watt_equi.text.strip() for watt_equi in detail if 'Watt Equivalent' in watt_equi.text]) for detail in details]
    lumens = ["".join([lumens.text.strip() for lumens in detail if 'Lumens:' in lumens.text]) for detail in details]
    lumens_per_watt = ["".join([lumenw.text.strip() for lumenw in detail if 'Lumens Per Watt:' in lumenw.text]) for detail in details]
    warranty = ["".join([warranty.text.strip() for warranty in detail if 'Warranty:' in warranty.text]) for detail in details]
    features = ["".join([features.text.strip() for features in detail if 'Features:' in features.text]) for detail in details]
    compatibility = ["".join([compat.text.strip() for compat in detail if 'Compatib' in compat.text]) for detail in details]
    wireless = ["".join([wless.text.strip() for wless in detail if 'Wireless' in wless.text]) for detail in details]
    lightify = [([lightify.text for lightify in detail if 'Lightify App' in lightify.text]) for detail in details][-1][0]
    lightify2 = [([lightify2.text for lightify2 in detail if 'Lightify App' in lightify2.text]) for detail in details][-1][1]

    # for index in range(len(links)):
    #     item = {
    #         'Title': title[index],
    #         'Link': links[index],
    #         'Model': models[index],
    #         'SKU': skus[index],
    #         'Base': bases[index],
    #         'Brand': brand[index],
    #         'Wattage': wattage[index],
    #         'Watt_equivalent': watt_equi[index],
    #         'Lumens': lumens[index],
    #         'Lumens Per Watt': lumensWatt[index],
    #         'Prices': prices[index],
    #         'Warranty': warranty[index],
    #         "Features": fea[index]
    #     }
    #
        # print(json.dumps(item, indent=2))



parse(response)