"""https://www.spitogatos.gr/search/results/residential/sale/r100/m2038m2610m2616m3011m6007m6013m384410m/price_nd-30000?ref=homepageMapSearchSR"""

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent



class Spitoscraper():
    headers = { "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "cookie": "PHPSESSID=mak5t38l3r035csdhimgu99lql; spitogatosHomepageMap=0; currentCurrency=EUR; _cmpQcif3pcsupported=1; _fbp=fb.1.1590600358549.2017671490; _hjid=7bf8f09d-c4b1-4a85-8a92-ba32db9c898d; _pubcid=d33d9ecc-1495-4197-af3f-fb90eab09cc6; _ga=GA1.2.1522910827.1590600359; _gid=GA1.2.1491863417.1590600359; DigiTrust.v1.identity=eyJpZCI6Ik44OVpyT2VndXJQVXIzZlA4Z0tyMW5JUHdVZDRja0NwblQ0N0FxVGhlaVIyMEM1SjVNQjduTm93U1paRW9Oc0JzcDc5RkljR1VVNHRBdFVvWVZhK1hJYnFicnBsalM0QTdZNmtIS2FQWWoyUjkvV0VoWDlHTFhXNEhwWjRaaEZXQjgyL2NoKzFzNzNYTVZCKyt2ZFVyZ29Gb1NFczNFZXk4L0pQRktLdFcvbmx4dUVSSVVvVy9BOFU4aHdST0pYaU5Sak1wTjhOWXo4QTRyajA2dHRqVFc2bnhBUEovdkJTajNCZUg2bzk1U3NpYVFaL2t4bzJlZGNvK09PTUU5a3haSTNDandjdExwK3lIOVduOGN1WXZaUEZFQTJoZk9xbUNLcDM1cVhndFBYakZ1ZjhKTDJvQ2J2Y3p4NUd2aENBbFA0Smx0SURMZEY0NHdEZzVIdXlDdz09IiwidmVyc2lvbiI6MiwicHJvZHVjZXIiOiIxQ3JzZFVOQW82IiwicHJpdmFjeSI6eyJvcHRvdXQiOmZhbHNlfSwia2V5diI6NH0%3D; __beaconTrackerID=00ie2a1zw; pbjs-id5id=%7B%22ID5ID%22%3A%22ID5-ZHMOQy38RprKiZ1ZrCK2MSxJpzcSqBjGLdsgPVF31Q%22%2C%22ID5ID_CREATED_AT%22%3A%222020-05-25T14%3A02%3A17.402Z%22%2C%22ID5_CONSENT%22%3Atrue%2C%22CASCADE_NEEDED%22%3Afalse%2C%22ID5ID_LOOKUP%22%3Atrue%2C%223PIDS%22%3A%5B%5D%7D; __gads=ID=ec2bca978203e2dd:T=1590600371:S=ALNI_MaRvmgFvhKBVfTqr1VAi3D6FmIcmQ; eupubconsent=BO0EltAO0EltAAKAhAENAAAAgAAAAA; euconsent=BO0EltAO0EltAAKAhBENDL-AAAAv1r_7__7-_9f-_f__9uj3Gr_v_f__32ccL5tv3h_7v-_7fi_-0nV4u_1vft9ydk1-5ctDztp507iakiPHmqNeb1n_mz1eZpRP58E09j5335Ew_v8_v-b7BCPN9Y3v-8K9wA; spitogatosS=areaIDs%255B0%255D%3D2038%26areaIDs%255B1%255D%3D2610%26areaIDs%255B2%255D%3D2616%26areaIDs%255B3%255D%3D3011%26areaIDs%255B4%255D%3D6007%26areaIDs%255B5%255D%3D6013%26areaIDs%255B6%255D%3D384410%26propertyCategory%3Dresidential%26listingType%3Dsale%26priceHigh%3D30000; cto_bidid=O708IV9mUkxneGhZVmxlVnA1cSUyQnV1N0wxcjB4Qm1UJTJCUURyNkl3ZG15MnElMkJZJTJGYzFIcUVQVXBOTDdobWJoYVRGYWpDQnBYNzVaZmc2bWNYNkpPU2p3ejFodW9reVFHSlNkRzJReDNtVG92WjQ4eEhFJTNE; cto_bundle=Y1MCpF84OVFKa0FCQlg3bHZ1TFQ0Vms5eTNKRkpHTWdJV1lod1hINDU5dzRGS3hZd05YNEN0WDNEM3ppdVkxYWVaSkcyJTJCSUFhdk5QaG5nZmVkclcyMU14TGpMNjhwWHRtcyUyQmYlMkZRcWxOR0o3Q0hiaEFUYkdKbVRSTTNTajNaWnZyVm5OUXJzSTElMkYxR1BOcUx1MG84UnpEJTJGWE9nJTNEJTNE; openedTabs=1; reese84=3:I+rBDG4pzLJcgb3veBHdmg==:dieqJURAN5QyTdK+uqgGEvEqZYskcy+7U9VMIR/ZTlRu+lHXStbANu6V95f+3YrOj+WJIdI5BlS7ayXHZHIjv/frZFMP5xqCFBIweoUOZMtvdQUMT+OlGvPU7ejeHQ7ZPOJjvDTCpkYFgBiyEfsUvoq4NCE6sK25hcYyBXpInacLfAvPGzJ06Q4WoTeZsDujMfhrIbsRKL4xrcbg6MkHOZ9M0GHSy+uO4TOiWZxJiPT8JXhijR69GB3G3ZnX1+HeSSVOhBKwuPA+BTC22/TS/4iIQkc8jYe5KQ0n9orngUREJMTbFbBAIgLwngNBmFw9lVkNGXlkTYOp22nuzvUWfgLbCaCoxW84pURMysLqrhk5u8hd8gowypXx+LHQtDrBtnDZ8L/+KLHecKDq08JRsuhSmzaIIv6GMoaQnKvxXvI=:i7lVL+Ma7hiuN6kJgI+C5jUkV2l2SAzGntJjag0Gq1U=",
                "dnt": "1",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
                }
    ua = UserAgent()

    # fetch the url site with the params and headers
    def fetch(self, url):
        print(f"HTTP GET request to URL: {url}", end="")
        res = requests.get(url, headers=self.headers)
        print(f" | Status code {res.status_code}")

        return res

    # create a HTML file with fetch's data(which is the response
    def save_response(self, res):
        with open('res.html', 'w', encoding="utf-8") as html_file:
            html_file.write(res)

    # write each line one after another from save_response
    def load_response(self):
        html = ""
        with open('res.html', 'r', encoding="utf-8") as html_file:
            for line in html_file:
                html += line

        return html

    #actual parsing
    def parse(self, html):
        print(html)
        content = BeautifulSoup(html, 'lxml')
        title = content.findAll("div", {"class": "media search_listing_title"})
        # print(title)

    # save data to csv format
    def to_csv(self):
        pass


    # actual running of the class
    def run(self):
        # params="System.item_type=re_residence&Transaction.price.to=30000&Transaction.type_channel=117518&Publication.level_num.from=1&Geo.area_id_new__hierarchy=82473,82339,82419,82420,82524,82509,82521,82360"
        # res = self.fetch('https://www.spitogatos.gr/search/results/residential/sale/r100/m2038m2610m2616m3011m6007m6013m384410m/price_nd-30000?ref=homepageMapSearchSR')
        # self.save_response(res.text)
        # part2
        html = self.load_response()
        self.parse(html)
        # self.to_csv()

if __name__ == '__main__':
    scraper = Spitoscraper()
    scraper.run()
