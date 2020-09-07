"https://www.rightmove.co.uk/property-for-sale/"

import requests
from bs4 import BeautifulSoup
import json
import csv


class RightMove:
    results = []

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "permuserid=200526YIM080ZNI45QHKGQG1YDJMGLRH; beta_optin=N:3:-1; RM_Register=C; __utma=6980913.1051301135.1590482720.1590482720.1590482720.1; __utmc=6980913; __utmz=6980913.1590482720.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; _gaRM=GA1.3.1051301135.1590482720; _gaRM_gid=GA1.3.618886707.1590482721; cdUserType=none; TS01a07bd2=012f990cd36828ec869950e357aca14029940684e523c4f27797219b803b178fe7b0ab26e83c6249516f13b7859bb989ba2679cecf2acf75b7a45691485f98a6166e26d9f04d8e0917da2954a73f17ca59107e2403ae7c77332934ea9c1001aa201ad036eb8afe4db54c6a00015d83a7703fc20772; __utmv=6980913.|1=source=google-seo=1^2=keyword=not-provided=1^33=Login%20Register%20Modal%20Test=T=1; __utmb=6980913.5.9.1590482799326; _gcl_au=1.3.458900911.1590482799; OptanonAlertBoxClosed=2020-05-26T08:46:39.503Z; _fbp=fb.2.1590482802129.962459231; JSESSIONID=9C727EAA6DB394E0F18A336701415C10; svr=1718; TS01ec61d1=012f990cd34d49fb2582205fd2e94dd33b11b07fef23c4f27797219b803b178fe7b0ab26e8555aef86cea4a648aa101f1f6dc75d3028a90849a21fd8da9b9e33738b20b37a03cef27e054c468733019832367a8352; rmsessionid=5a00d45e-83b4-4087-b02c-a1903c27e91a; TS019c0ed0=012f990cd31d8e6398b0fabe2b4d22c82332c0ccd323c4f27797219b803b178fe7b0ab26e8e22b80324b9a203674194f78869cfcadcf27920ca388fa684f308120738a57023fcc5fb6d144f093fc8b9d72228d17b54d80fdca2a1b6c96991f05882a07e109bd2f42aa4db7a0debdbc2013ea6417e2; TS01826437=012f990cd37ab7319373b9fe251cb13fbdf07928ad23c4f27797219b803b178fe7b0ab26e83c6249516f13b7859bb989ba2679cecf2acf75b7a45691485f98a6166e26d9f04d8e0917da2954a73f17ca59107e2403ae7c77332934ea9c1001aa201ad036eb3eab429115bdc8cfd30240e3b07aab1a82cf9dc5b1e2cab38071c1b8e2a44bafc601e2749f65a58e90a0923dfe1a61f4; __gads=ID=e56fe601197ace79:T=1590482822:S=ALNI_MYb4FzKgTlalZ-5ahJ9kxVeAprvXw; _dc_gtm_UA-3350334-63=1; _gat_UA-3350334-63=1; OptanonConsent=isIABGlobal=false&datestamp=Tue+May+26+2020+11%3A48%3A30+GMT%2B0300+(Eastern+European+Summer+Time)&version=5.11.0&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false&consentId=15ba27e6-d8a6-46f9-830c-6f5005e7bed8",
        "DNT": "1",
        "Host": "www.rightmove.co.uk",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }

    def fetch(self, url):
        print(f"HTTP GET request to URL: {url}", end="")
        response = requests.get(url, headers=self.headers)
        print(f' | STATUS CODE: {response.status_code}')
        return response

    def save_response(self, response):
        with open("rightmove.html", 'w', encoding="utf-8") as rightmove:
            rightmove.write(response)

    def load_response(self):
        html = ""
        with open("rightmove.html", "r", encoding="utf-8") as rightmove:
            for line in rightmove:
                html += line
        return html

    # starting from part2
    def parse(self, html):
        # print(html)
        content = BeautifulSoup(html, "lxml")

        title = [title.text.strip() for title in content.findAll("h2", {"class": "propertyCard-title"})]
        address = [address['content'] for address in content.findAll("meta", {"itemprop": "streetAddress"})]
        description = [des.text.strip() for des in content.findAll("span", {"data-test": "property-description"})]
        prices = [price.text.strip() for price in content.findAll("div", {"class": "propertyCard-priceValue"})]
        dates = [date.text for date in content.findAll("span", {"class": "propertyCard-branchSummary-addedOrReduced"})]
        sellers = [sale.text.split('by')[-1].strip() for sale in content.findAll("div", {"class": "propertyCard-branchSummary"})]
        for index in range(0, len(title)):
            self.results.append({
                "Title": title[index],
                "Address": address[index],
                "Description": description[index],
                "Price": prices[index],
                "Date": dates[index],
                "Sellers": sellers[index],
            })

            # print(json.dumps(item, indent=2))

    def to_csv(self):
        with open('rightmove.csv', 'w') as right_csv:
            writer = csv.DictWriter(right_csv, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def run(self):
        for page in range(0, 4):
            page = page*24
            url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E93917&index={page}&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords="
            response = self.fetch(url)
            self.parse(response.text)
        self.to_csv()



if __name__ == "__main__":
    scraper = RightMove()
    scraper.run()
