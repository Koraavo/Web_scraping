"""https://www.zillow.com/homes/for_rent/New-York,-NY_rb/"""

import requests
from bs4 import BeautifulSoup
import json
import csv

class Zillowscraper():
    results = []

    headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "cookie": "ki_s=; zguid=23|%241f3a946c-b983-4fe6-84f4-26a2b3ff333b; zgsession=1|4907638c-663a-4b11-81d4-6247c6f512f8; JSESSIONID=D0E5F29514A7D75013DFB13FF32065EB; __gads=ID=e99ca233891a3ea9:T=1590332025:S=ALNI_MbUeRFz8RT5d7ddFNqQtjB78_Xcvw; _ga=GA1.2.1927103529.1590332045; _gid=GA1.2.119956681.1590332045; _pxvid=6a3c72f2-9dce-11ea-b26f-0242ac12000a; zjs_user_id=null; zjs_anonymous_id=%221f3a946c-b983-4fe6-84f4-26a2b3ff333b%22; _gcl_au=1.1.1393731778.1590332047; KruxPixel=true; DoubleClickSession=true; GASession=true; _fbp=fb.1.1590332048537.1365526442; KruxAddition=true; _uetsid=6631a8aa-ace6-91bc-e703-7251f25c433b; ki_t=1590328919819%3B1590328919819%3B1590332098920%3B1%3B31; AWSALB=HQ8dZlC8CWAvCyFFGUH2Xa16Xb8rGsiNGFi8XzYHVMzB7H4BB8r+ikqmjaL67QJ5E6gjtOBbFYtKpsgdV2OVkD+x+sZ1vYn0+3FkffVWoxIEjbUhFaskaPDOK/Li; AWSALBCORS=HQ8dZlC8CWAvCyFFGUH2Xa16Xb8rGsiNGFi8XzYHVMzB7H4BB8r+ikqmjaL67QJ5E6gjtOBbFYtKpsgdV2OVkD+x+sZ1vYn0+3FkffVWoxIEjbUhFaskaPDOK/Li; search=6|1592924099647%7Crect%3D40.956841215490435%252C-73.35700005116189%252C40.454016029555525%252C-74.59891294883812%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D0%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%096181%09%09%09%09%09%09; _px3=b9d1f74d8c98332a53a88755449597544bed1fd36d60700c4910ed81ab434d54:it/MCsK8zwle+Ar0wYnqcwhsUyeffJS60BMg9tHJTxjm8MAQuEuHoTorAyBZ4JLkxkezkTzZk8huc9JOc+/uNQ==:1000:v3sH1XflE+uXPhqpL1pR7iJHljohL+y6qfziEulTux9Z/SsdcnBGwmdrCeB73SwoXVl6bp0QktwfD9OZ6Fio95Kg5eUJWJbCApIO0oelBe7VO/nL4co2c6rDcSQl4q4OKM2AvrBN0Lhis5oblidYvXZmBmLsnL61ULeU+ftkkPQ=dnt: 1",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
                }


    def fetch(self, url, params):
        print(f"HTTP GET request to URL: {url}", end="")
        res = requests.get(url, params=params, headers=self.headers)
        print(f" | Status code {res.status_code}")

        return res


    def save_response(self, res):
        with open('res.html', 'w', encoding="utf-8") as html_file:
            html_file.write(res)


    def load_response(self):
        html = ""
        with open('res.html', 'r', encoding="utf-8") as html_file:
            for line in html_file:
                html += line

        return html

    def parse(self, html):
        # parse response
        # content that needs to be parsed and what kind of parser
        content = BeautifulSoup(html, "lxml")

        # extract property cards
        cards = content.findAll("article", {'class': 'list-card'})

        # extract coordinates
        scripts = content.find('script', {'data-zrr-shared-data-key': 'mobileSearchPageStore'})
        print(scripts)



        # loop over property cards
        for card in cards:
            try:
                price = card.find('div', {'class': 'list-card-price'}).text
            except:
                price = 'as per size in the details'
            try:
                img = card.find('img')['src']
            except:
                img = 'NA'

            items = {
                'Address': card.find('address', {'class':'list-card-addr'}).text,
                'URLS': card.find('a', {'class': 'list-card-link'})['href'],
                'Price': price,
                'Details': [bds.text for bds in card.find('ul', {'class': 'list-card-details'}).find_all('li')],
                'Images': img

                            }
            '''
            # try to extract coordinates from script
            splitter = '"detailUrl":"' + items['URLS'] + '","latLong":'
            
            try:
                coords = json.loads(script.split(splitter)[-1].split('},')[0] + '}')
                items['coordinates'] = coords
            except:
                coords = script.split(splitter)[-1].split('},')[0] + '}'
                splitter = '<!--{"queryState":{"mapBounds":'

                try:
                    map_bounds = json.loads(coords.split(splitter)[-1])
                    items['coordinates'] = map_bounds
                except:
                    items['coordinates'] = 'N/A'
            '''

            # append items scraped to results_list
            # self.results.append(items)
            # print(json.dumps(items, indent=2))

    def to_csv(self):
        with open('zillow_rent.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def to_json(self):
        with open('zillow_rent.json', 'w') as f:
            f.write(json.dumps(self.results, indent=2))

    def run(self):
        '''
        for page in range(1, 5):
            params = {'searchQueryState': """{"pagination":{"currentPage": %s},"usersSearchTerm":"Atlanta, GA",
            "mapBounds":{"west":-84.79096922441906,"east":-84.17001277558094,"south":33.642931132799994,
            "north":33.89085361537081},"regionSelection":[{"regionId":37211,"regionType":6}],"mapZoom":11,
            "filterState":{"pmf":{"value":false},"fore":{"value":false},"auc":{"value":false},"nc":{"value":false},
            "fr":{"value":true},"fsbo":{"value":false},"cmsn":{"value":false},"pf":{"value":false},
            "fsba":{"value":false}},"isListVisible":true,"isMapVisible":false}"""% page}

            # part3
            res = self.fetch('https://www.zillow.com/homes/Atlanta,-GA_rb/?', params)
            self.parse(res.text)

        self.to_csv()
        self.to_json()

        '''
        # self.save_response()
        html = self.load_response()
        self.parse(html)
        # self.parse(html)


if __name__ == '__main__':
    scraper = Zillowscraper()
    scraper.run()
