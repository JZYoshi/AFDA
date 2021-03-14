# -*- coding: utf-8 -*-
import requests;
from bs4 import BeautifulSoup;
from bs4 import PageElement, ResultSet;
from typing import Callable, List;
from functools import reduce;
import os;
import re;

def get_all_href_elements(url: str) -> ResultSet:
    """
    To get all the <a> elements in the DOM returned by the given url

    :param url: a string of url 

    :returns: a ResultSet containing all the <a> elements in the DOM
    """
    return BeautifulSoup(requests.get(url).text, 'html.parser').find_all('a')

def get_filtered_hrefs(url: str, fil: Callable[[PageElement], bool]) -> List[str]:
    """
    To search the DOM given the url for specific <a> elements satisfying the given filter,
    and return a list of urls contained by these <a> elements

    :param url: a string of url

    :param fil: a function (PageElement) -> bool

    :returns: a list of strings of url
    """
    hrefElements = get_all_href_elements(url)
    filtered = filter(fil, hrefElements)
    return list(map(lambda element: (url if url.endswith('/') else url + "/") + element.get('href'), filtered))

def search_hrefs(startUrl: str, filters: List[Callable[[PageElement], bool]]) -> List[str]:
    """
    Given a start url, find progressively the descendant elements that satisfy the given filters.
    The filters are applied in order through the transitions, which means we apply one filter during one transition,
    so the number of filters is the number of transitions to take place. Here, a transition means the process of finding
    <a> elements in the current DOM and append each of their relative links to the current url to form a list of new urls.
    The function returns a list of final urls obtained.  

    :param startUrl: a string of url

    :param filters: a list of function (PageElement) -> bool

    :returns: a list of strings of url
    """
    urls = [ startUrl ]
    for fil in filters:
        urls = reduce(list.__add__, list(map(lambda url: get_filtered_hrefs(url, fil), urls)))
    return urls

if __name__=="__main__":
    filters = [ lambda ele: re.match('[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])', ele.string),
                lambda ele: re.match('^[0-2][0-9]$', ele.string),
                lambda ele: ele.string.endswith('.csv.tar')]
    # To decomment when wanting to fetch all the files
    # res = search_hrefs('https://opensky-network.org/datasets/states/', filters)
    # tempo_dname = '../data/__tempo_archive/'
    # if not os.path.exists(tempo_dname):
    #            os.mkdir(tempo_dname)
    # for url in res:
    #     fname = url[-(len(url) - url.rfind('/') - 1):]
    #     print(fname)
    #     fileObj = requests.get(url)
    #     with open(tempo_dname + fname, 'wb') as local_file:
    #         local_file.write(fileObj.content)