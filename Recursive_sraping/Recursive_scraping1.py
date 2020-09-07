import requests
from bs4 import BeautifulSoup
import json
import csv


class Stockscraper:
    results = []

    def fetch(self, url):
        print(f'HTTP GET REQUESTS TO URL: {url}', end="")
        res = requests.get(url)
        print(f' | STATUS CODE: {res.status_code}')

        return res

    def save_response(self, html):
        with open('stock.html', 'w', encoding='utf-8') as stock_html:
            stock_html.write(html)

    def load_response(self):
        html = ''
        with open('stock.html', 'r', encoding='utf-8') as stock_html:
            for line in stock_html:
                html += line
        return html

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        titles = [title.text for title in content.findAll('h2', {'class': 'entry-title'})]
        links = [link.find('a')['href'] for link in content.findAll('h2', {'class': 'entry-title'})]
        dates = [date.text for date in content.findAll('span', {'class': 'meta-date'})]
        articles = []

        # scraping for text in the links
        for link in links:
            response = requests.get(link)
            article_content = BeautifulSoup(response.text, 'lxml')
            article_body = ''.join(
                [line.text for line in article_content.find('div', {'class': 'entry entry-content'}).findAll('p')])
            articles.append(article_body)

        for index in range(len(titles)):
            self.results.append({
                'Dates': dates[index],
                'Titles': titles[index],
                'Links': links[index],
                'Articles': articles[index]

            })

            # print(json.dumps(items, indent=2))

    def save_to_csv(self):
        with open('stock.csv', 'w', encoding='utf-8') as stock_csv:
            writer = csv.DictWriter(stock_csv, fieldnames=self.results[0].keys())
            writer.writeheader()

            for result in self.results:
                writer.writerow(result)

    def run(self):
        url = 'http://www.stockpricetoday.com/stock-news'
        for page in range(1, 4):
            if page == 1:
                next_page = url
            else:
                next_page = f'{url}/page/{page}/'
            # print(next_page)

            res = self.fetch(url)
            # self.save_response(res.text)
            self.parse(res.text)
        self.save_to_csv()


if __name__ == '__main__':
    scraper = Stockscraper()
    scraper.run()
