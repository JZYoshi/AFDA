# -*- coding: utf-8 -*-
import requests;
from bs4 import BeautifulSoup;
from bs4 import PageElement, ResultSet;
from typing import Callable, List;
from functools import reduce;
import re;
import pandas as pd;
import tarfile;

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

gz_files = []

tarObj = tarfile.open('../dataset/states_2020-05-25-06.csv.tar')
for member in tarObj.getmembers():
    if (member.name.endswith('.csv.gz')):
        tarObj.extractfile(member)
        gz_files.append(member.name)
tarObj.close()
# df = pd.read_csv('./states_2020-05-25-06.csv.gz', compression='gzip')
print(gz_files)