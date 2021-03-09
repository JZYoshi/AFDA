# -*- coding: utf-8 -*-
import requests;
from bs4 import BeautifulSoup;
from bs4 import PageElement, ResultSet;
from typing import Callable, List;
from functools import reduce;
import re;

def get_all_href_elements(url: str) -> ResultSet:
    return BeautifulSoup(requests.get(url).text, 'html.parser').find_all('a')

def get_filtered_hrefs(url: str, fil: Callable[[PageElement], bool]) -> List[str]:
    hrefElements = get_all_href_elements(url)
    filtered = filter(fil, hrefElements)
    return list(map(lambda element: (url if url.endswith('/') else url + "/") + element.get('href'), filtered))

def search_hrefs(startUrl: str, filters: List[Callable[[PageElement], bool]]) -> List[str]:
    urls = [ startUrl ]
    for fil in filters:
        urls = reduce(list.__add__, list(map(lambda url: get_filtered_hrefs(url, fil), urls)))
    return urls

filters = [ lambda ele: re.match('[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])', ele.string),
            lambda ele: re.match('^[0-2][0-9]$', ele.string),
            lambda ele: ele.string.endswith('.csv.tar')]
# To decomment when wanting to fetch all the files
# res = search_hrefs('https://opensky-network.org/datasets/states/', filters)
# for url in res:
#     fname = url[-(len(url) - url.rfind('/') - 1):]
#     print(fname)
#     fileObj = requests.get(url)
#     with open('./dataset/' + fname, 'wb') as local_file:
#         local_file.write(fileObj.content)