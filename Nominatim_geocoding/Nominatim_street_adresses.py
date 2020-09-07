import requests
import json
import time


class Geocoder:

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "dnt": "1",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }

    results = []

    # base_url
    base_url = "https://nominatim.openstreetmap.org/search"

    def fetch(self, address):
        # string query parameters
        params = {
            "q": address,
            "format": "geocodejson"
        }
        response = requests.get(self.base_url, params=params)
        print(f"HTTP Get request to url: {response} | Status Code: {response.status_code}")

        return response

    def parse(self, response):
        coordinates = (json.dumps(response['features'][0]['geometry']['coordinates'], indent=2)).replace("\n", "").replace("[", "").replace("]", "").strip()
        labels = (json.dumps(response['features'][0]['properties']['geocoding']['label'], indent=2))

        # retrieved data
        self.results.append({
            'Addresses': labels,
            'coordinates': coordinates

        })
        # print(json.dumps(items, indent=2))
        return self.results

    def store_json(self):
        with open('geocoord.json', 'w') as geocoord_json:
            geocoord_json.write(json.dumps(self.results, indent=2))


    def run(self):
        # addresses list
        addresses = ''

        # fetch addresses from file
        with open('addresses.txt', 'r') as f:
            for line in f.read():
                addresses += line

        # convert addresses to list
        addresses = addresses.split('\n')

        # loop over addresse
        for address in addresses:
            res = self.fetch(address).json()
            self.parse(res)

            # respect Nominatim crawling policies
            time.sleep(2)

        # store results
        self.store_json()


if __name__ == "__main__":
    geocoder = Geocoder()
    geocoder.run()
