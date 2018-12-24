import json
import requests
import yaml
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

now = datetime.now()
then = now - timedelta(days=2)

hits = {}

BASE_URL = 'https://www.ncbi.nlm.nih.gov/pubmed'
f = yaml.load(open('terms.yaml'))
for item in f:
    term = f'{item} AND "{now.isoformat()}"[MHDA]:"{(now - timedelta(days=2)).isoformat()}"[MHDA]'
    start = f'{BASE_URL}/?term={term}'
    url = f'{start}&page={{}}'
    soup = BeautifulSoup(requests.get(start).content)
    pages = int(soup.find('input', {'id':'pageno2'}).get('last'))

    for page in range(0, pages):
        soup = BeautifulSoup(requests.get(url.format(page), stream=True).content)
        try:
            results = soup.find_all('div', {'class':'rslt'})
            for row in results:
                pmid = row.find('a').get('href')
                title = row.find('a').get_text()
                hits[pmid.split('/')[2]] = {
                    'pmid': f'{BASE_URL}{pmid}',
                    'title': title,
                    }

        except AttributeError:
            print(page)

with open('hits.json' 'w') as f:
    json.dump(hits, f)
