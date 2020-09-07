"""https://www.spitogatos.gr/search/results/residential/sale/r100/m2038m2610m2616m3011m6007m6013m384410m/price_nd-30000?ref=homepageMapSearchSR"""

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent



class Xescraper():
    headers = {
    # ":authority": "www.xe.gr",
    # ":method": "GET",
    # ":path": "/property/search?System.item_type=re_residence&Transaction.price.to=30000&Transaction.type_channel=117518&Publication.level_num.from=1&Geo.area_id_new__hierarchy=82473,82339,82419,82420,82524,82509,82521,82360",
    # ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age = 0",
    "cookie": "property_preferences=%257B%2522cpOpen%2522%253Afalse%252C%2522comparisonListHeight%2522%253A0%257D; __SID=5101A7C2-9F6C-11EA-AA35-78A435896A6C; __XE_COOKIE=3717ee47de043ce873cb38b75a670a22; xe_preferences=%257B%2522comparisonListHeight%2522%253A153%252C%2522cpOpen%2522%253Afalse%257D; _ga=GA1.2.1387924590.1590509819; _gid=GA1.2.194297332.1590509819; __utma=175768868.1387924590.1590509819.1590509819.1590509819.1; __utmc=175768868; __utmz=175768868.1590509819.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; reese84=3:/7AUqmXGRbh6KCBZOJxcGw==:sWO1kNvCSkxac4QPDxocAKLVUg47KoiKHxp/hejhHdJqmYjquJDzNG2vqhXmLPkxiO0A7orXE1qi999mZ1Bs3OWzgUZRvaaTquz0SOy9Fo+9RxCy/lAwwPpXXCuayu+RV2+mf0qCSy4vc/w6OWYKw0ic1z2Za1Kmqiy08RBUI31Q1X2YViW8I2HYNTq3xAeuV0Yjk71sQRXqOhiOwYL4YNa+pDtktE83tRFbSsDGezjD09poqLr3vktnTeE68eY1eQok/MF477AHtl4XMGfyE1VMiaCn/zRz8KIfh8XxAeS08BQLbLHAZyCWlHrjKpv3RXH1sT0Pd/FvGyAm/+mjXbYTrPSn3UvaTgqZa66WwyBkp3D7umNI8Vtnl0KpXD8u7P5IjVvzBc50HNiR4olNVjTYPpaRDIU5VLebtdEOPWU=:7cgfNUNXTGiJFN5lyQKt/rb2psD3GSgatgJ9wTmA+W8=; _fbp=fb.1.1590509819779.1325482083; intercom-id-bewzsb79=dd2ce869-b1fd-4d6d-ac5a-a0cb10b2a544; intercom-session-bewzsb79=; __utmb=175768868.6.9.1590509821512",
    "dnt": "1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    ua = UserAgent()

    # fetch the url site with the params and headers
    def fetch(self, url, params):
        print(f"HTTP GET request to URL: {url}", end="")
        res = requests.get(url, params=params, headers=self.headers)
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
        pass


    # save data to csv format
    def to_csv(self):
        pass


    # actual running of the class
    def run(self):
        params="System.item_type=re_residence&Transaction.price.to=30000&Transaction.type_channel=117518&Publication.level_num.from=1&Geo.area_id_new__hierarchy=82473,82339,82419,82420,82524,82509,82521,82360"
        res = self.fetch('https://www.xe.gr/property/search?', params)
        self.save_response(res.text)


if __name__ == '__main__':
    scraper = Xescraper()
    scraper.run()
