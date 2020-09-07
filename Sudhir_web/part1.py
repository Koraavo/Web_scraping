"""https://www.sudhirshivaramphotography.com/online-photography-courses"""

import requests
from bs4 import BeautifulSoup
import json
import csv


class Sudhirscraper:
    results = []

    def fetch(self, url):
        print(f"HTTP GET request to URL: {url}", end="")
        res = requests.get(url)
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

    # actual parsing
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        active_page = content.find("li", {"class": "active"})
        cards = content.findAll("div", {"class": "col-sm-4"})
        for card in cards:
            try:
                titles = [title.text.strip() for title in card.findAll("h4", {"class": "card-title"})]
            except:
                titles = "N/A"

            try:
                prices = [price.text.strip() for price in card.findAll("span", {"class": "course-price"})]
            except:
                prices = "N/A"

            view_course = [course.find("a")["href"] for course in card.findAll("div", {"class": "card-footer"})]
            course_subheads = []
            lesson_plans = []

            for link in view_course:
                response = requests.get(link)
                article_content = BeautifulSoup(response.text, 'lxml')
                course_heads = ["".join(course.text.strip().replace("  ", "").split(",")) for course in
                                article_content.findAll("h4", {"class": "media-heading"})]
                # print(course_subheading)
                course_subheads.append(course_heads)
                # print(course_heads)
                lesson_plan = [lesson.text.strip() for lesson in
                               article_content.findAll("div", {"class": "tab-pane active"})]
                lesson_plans.append("".join(lesson_plan))

            for index in range(len(titles)):
                self.results.append({
                    "Titles": titles[index],
                    "Prices": prices[index],
                    "View Course": view_course[index],
                    "COURSE SUBHEADING": course_subheads[index],
                    "LESSON PLAN": lesson_plans[index]

                })

                print(json.dumps(self.results, indent=2))

    # save data to csv format
    def to_csv(self):
        with open('photography_classes-1.csv', 'w', encoding='utf-8') as stock_csv:
            writer = csv.DictWriter(stock_csv, fieldnames=self.results[0].keys())
            writer.writeheader()

            for result in self.results:
                writer.writerow(result)

    # actual running of the class
    def run(self):
        # part3
        url = 'https://www.sudhirshivaramphotography.com/online-photography-courses'
        res = self.fetch(url)
        self.parse(res.text)
        # self.to_csv()


if __name__ == '__main__':
    scraper = Sudhirscraper()
    scraper.run()
