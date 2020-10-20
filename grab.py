import requests
import os
from urllib.parse import urlencode as u
import subprocess
import json

base = 'api/v1'

session = requests.Session()
session.headers.update({'referer': 'https://translatefor.sg'})

def get_categories():
    return session.get('https://api.translatefor.sg/api/v1/categories').json()['results']

def get_languages():
    return session.get('https://api.translatefor.sg/api/v1/languages').json()['results']

def dump_category(language, category):
    path = os.path.join(base, language, category + '.json')
    q = u({'language__name': language, 'phrase__category__name': category})
    url = f'https://api.translatefor.sg/api/v1/translations/?{q}'
    print(q)
            
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()

    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

def dump_language(language, category):
    path = os.path.join(base, 'downloadables', language, category + '.json')
    q = u({'language__name': language, 'category__name': category})
    url = f'https://api.translatefor.sg/api/v1/downloadables/?{q}'
    print(q)
            
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()

    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
def main():
    for language in get_languages():
        subprocess.call(['mkdir', '-p', os.path.join(base, language['name'])])
        for category in get_categories():
            dump_category(language['name'], category['name'])
        path = os.path.join(base, language['name'],  'All.json')
        q = u({'language__name': language['name']})
        url = f'https://api.translatefor.sg/api/v1/translations/?{q}'
        print(q)
                
        resp = session.get(url)
        resp.raise_for_status()
        data = resp.json()

        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

# def main():
#     for language in get_languages():
#         subprocess.call(['mkdir', '-p', os.path.join(base, 'downloadables', language['name'])])
#         for category in get_categories():
#             dump_language(language['name'], category['name'])
#         path = os.path.join(base, 'downloadables', language['name'],  'All.json')
#         q = u({'language__name': language['name']})
#         url = f'https://api.translatefor.sg/api/v1/downloadables/?{q}'
#         print(q)
                
#         resp = session.get(url)
#         resp.raise_for_status()
#         data = resp.json()

#         with open(path, 'w') as f:
#             json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

main()