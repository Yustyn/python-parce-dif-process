import time
import tracemalloc
import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup

d = {}


def main():
    URL = "https://www.ukr.net/"
    response = requests.get(URL)
    response.encoding = 'UTF8'
    d['site'] = URL
    d['news'] = []

    soup = BeautifulSoup(response.text, 'html.parser')

    data = soup.select('section', class_='feed__section')

    for i in range(6, len(data) - 4):
        d['news'].append({})
        d['news'][i - 6]['category'] = data[i].select_one('a').text
        d['news'][i - 6]['time'] = data[i].select_one('time').text
        d['news'][i - 6]['url'] = data[i].find_all(href=True)[1]['href']
        d['news'][i - 6]['title'] = data[i].find_all(href=True)[1].text
        d['news'][i - 6]['source'] = data[i].find_all('span')[0].text[1:-1]

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(
            d,
            file,
            indent=4,
            ensure_ascii=False,
        )
        file.close()


tracemalloc.start()
start = time.time()
main()
print("Current %d, Peak %d" % tracemalloc.get_traced_memory())
print("All done! {}".format(time.time() - start))