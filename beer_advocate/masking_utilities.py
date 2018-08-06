# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import requests
from lxml.html import fromstring
import pandas as pd

extract_first = lambda L: '' if len(L)==0 else L[0]

def get_response_code(test_url, proxy=None, user_agent=None):
    if not proxy is None:
        if not user_agent is None:
            try:
                r = requests.get(test_url, proxies={'https': proxy}, headers={'user-agent': user_agent})
                return(r.status_code)
            except:
                return(-1)
        else:
            try:
                r = requests.get(test_url, proxies={'https': proxy})
                return(r.status_code)
            except:
                return(-1)
    else:
        return(-200)

# get list of free proxies and use only elite proxies
def get_proxy_list(test_url=None, user_agent=None):

    url = "https://free-proxy-list.net/" # url for website with proxies
    response = requests.get(url)

    #parse response to get list of proxies
    parser = fromstring(response.text)
    rows = parser.xpath('//*[@id="proxylisttable"]//tr')
    rows = rows[1:301]
    ip_address = list(map(lambda o: extract_first(o.xpath('td[1]/text()')), rows))
    port = list(map(lambda o: extract_first(o.xpath('td[2]/text()')), rows))
    code = list(map(lambda o: extract_first(o.xpath('td[3]/text()')), rows))
    country = list(map(lambda o: extract_first(o.xpath('td[4]/text()')), rows))
    anon = list(map(lambda o: extract_first(o.xpath('td[5]/text()')), rows))
    https = list(map(lambda o: extract_first(o.xpath('td[7]/text()')), rows))
    last_checked = list(map(lambda o: extract_first(o.xpath('td[8]/text()')), rows))
    # zip into dictionary and then pandas df
    result = {'ip_address': ip_address, 'port': port, 'code': code, 'country': country, 'anon': anon, \
              'https': https, 'last_checked': last_checked}
    result = pd.DataFrame(result)
    # add field forproxy
    result['proxy'] = result.ip_address + ":" + result.port
    # filter df on country codes that are usually ok
    ok_codes = ['US', 'GB', 'DE', 'CA', 'FR']
    result = result.loc[(result.anon=='elite proxy') & (result.https=='yes') & (result.code.isin(ok_codes)),:]

    # test proxies by getting response codes
    if not test_url is None:
        print('test_url: ' + test_url)

        proxies = list(result['proxy'])
        response_codes = list(map(lambda p: get_response_code(test_url, p, user_agent), proxies))

        if not user_agent is None:
            print('user_agent: ' + user_agent)
        else:
            print('user_agent is None')

    else:
        print('test_url is None')

    result['response_code'] = response_codes

    # filter out non-200 HTTP status codes and narrow down columns
    result = result.loc[(result.response_code==200), ['proxy', 'code', 'last_checked']]
    return(result)

def get_proxy_list_old():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    parser = fromstring(response.text)
    ip_address = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[1]/text()')
    port = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[2]/text()')
    code = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[3]/text()')
    country = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[4]/text()')
    anon = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[5]/text()')
    https = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[7]/text()')
    last_checked = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[8]/text()')
    result = {'ip_address': ip_address, 'port': port, 'code': code, 'country': country, 'anon': anon, \
              'https': https, 'last_checked': last_checked}
    result = pd.DataFrame(result)
    result['proxy'] = result.ip_address + ":" + result.port
    ok_codes = ['US','CA','DE','FR','ES','AU','GB']
    #ok_codes = ['US']
    result = list(result.loc[(result.anon=='elite proxy') & (result.https=='yes') & (result.code.isin(ok_codes)), 'proxy'])
    return(result)

def get_proxy_list_debug():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    parser = fromstring(response.text)
    ip_address = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[1]/text()')
    port = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[2]/text()')
    code = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[3]/text()')
    country = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[4]/text()')
    anon = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[5]/text()')
    https = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[7]/text()')
    last_checked = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[8]/text()')
    result = {'ip_address': ip_address, 'port': port, 'code': code, 'country': country, 'anon': anon, \
              'https': https, 'last_checked': last_checked}
    result = pd.DataFrame(result)
    return(result)

def get_proxy_list_test():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    parser = fromstring(response.text)
    ip_address = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[1]/text()')
    port = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[2]/text()')
    code = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[3]/text()')
    country = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[4]/text()')
    anon = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[5]/text()')
    https = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[7]/text()')
    last_checked = parser.xpath('//*[@id="proxylisttable"]/tbody/tr/td[8]/text()')
    result = {'ip_address': ip_address, 'port': port, 'code': code, 'country': country, 'anon': anon, \
              'https': https, 'last_checked': last_checked}
    result = pd.DataFrame(result)
    return(result)


# get list of user agents
def get_user_agent_list():
    url = "https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/1"
    response = requests.get(url)
    parser = fromstring(response.text)
    user_agent = parser.xpath('//table//tbody/tr/td[1]/a/text()')
    #version = parser.xpath('//table//tbody/tr/td[2]/text()')
    ua_os = parser.xpath('//table//tbody/tr/td[3]/text()')
    hardware_type = parser.xpath('//table//tbody/tr/td[4]/text()')
    popularity = parser.xpath('//table//tbody/tr/td[5]/text()')
    result = {'user_agent': user_agent, 'ua_os': ua_os, 'hardware_type': hardware_type, 'popularity': popularity}
    result = pd.DataFrame(result)
    result = list(result.loc[(result.hardware_type=='Computer') & (result.ua_os=='Windows') & (result.popularity=='Very common'), 'user_agent'])
    return(result)
