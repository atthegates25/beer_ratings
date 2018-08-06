from scrapy import Spider, Request
from beer_advocate.items import RatingSummaryPageItem
from beer_advocate.masking_utilities import *
from lxml.html import fromstring
import pandas as pd
import numpy as np
import re, os, requests
import datetime as dt


class BeerAdvocateRatingsSummarySpider(Spider):
    name = "ba_ratings_summary_spider"
    allowed_urls = ["https://www.beeradvocate.com/"]
    start_urls = ["https://www.beeradvocate.com/beer/style/116/"]

    # get list of free proxies and use only elite proxies
    def parse(self, response):
        # find total number of beers and number of pages
        xpath_response = response.xpath('//table//tr[1]/td//b/text()').extract_first()
        _, num_per_page, num_beers = map(lambda d: int(d), re.findall('\d+',xpath_response))
        num_pages = (num_beers // num_per_page) + 1
        # generate the corresponding urls to scrape
        base_url = "https://www.beeradvocate.com/beer/style/116/"
        result_urls = list(map(lambda i: base_url + "?sort=revsD&start=" + str(num_per_page*i), range(0,num_pages)))

        # narrow down list to test
        #result_urls = result_urls[0:2]

        # get list of user_agents.  for now, only use first
        user_agent_list = get_user_agent_list()
        user_agent = user_agent_list[0]

        # generate proxy list and associated parameters
        # pass in test url and user agent to return only working proxies
        proxy_list = get_proxy_list(test_url=base_url, user_agent=user_agent) # get list of proxies

        prxy_lst_updt = dt.datetime.now() # set time of last proxy list update
        prxy_updt_interval = 1 # proxy refresh interval in minutes
        num_proxies = len(proxy_list) # get number of proxies
        dt_format = '%m/%d/%Y %H:%M:%S:%f'
        i = 0

        # used for debugging purposes
        print('Proxy list generated at: ' + prxy_lst_updt.strftime(dt_format) + '; length: ' + str(len(proxy_list)))

        for url in result_urls:
            #check how much time has passed since proxies were refreshed
            i += 1
            #proxy_age_check_now = dt.datetime.now()
            #time_since_prxy_updt = proxy_age_check_now - prxy_lst_updt
            #print('last update: ' + prxy_lst_updt.strftime(dt_format) + '; now: ' + proxy_age_check_now.strftime(dt_format) + '; time elapsed: ' + str(time_since_prxy_updt.total_seconds()))

            # refresh list if threshold has passed - #### remove for now because it doesn't appear to impact success of proxy
            #if time_since_prxy_updt.total_seconds() > prxy_updt_interval*60:
            #    proxy_list = get_proxy_list() # get list of proxies
            #    prxy_lst_updt = dt.datetime.now() # set time of last proxy list update
            #    num_proxies = len(proxy_list)
            #    print('Proxy list generated at: ' + prxy_lst_updt.strftime(dt_format) + '; length: ' + str(len(proxy_list)))

            # generate randon integer
            np.random.seed()
            r = np.random.randint(low=0,high=num_proxies)
            proxy_to_use = proxy_list.iloc[r,0]
            proxy_code = proxy_list.iloc[r,1]
            proxy_last_checked = proxy_list.iloc[r,2]
            print('Proxy attempted|' + str(i) + '|' + str(50*(i-1)) + '|' + proxy_to_use + '|' + proxy_code + '|' + proxy_last_checked)
            yield Request(url=url, headers={'User-Agent': user_agent}, meta={'num_per_page': num_per_page, 'proxy': proxy_to_use, 'proxy_used': proxy_to_use, 'page_number': i}, callback=self.parse_ratings_summary_page)

    def parse_ratings_summary_page(self, response):
        print('Proxy successful|' + str(response.meta['page_number']) + '|' + str(50*(response.meta['page_number']-1)) + '|' + response.meta['proxy_used'])
        num_per_page = response.meta['num_per_page']
        beer_name = response.xpath('//table//tr/td[@class="hr_bottom_light"]/a/b/text()').extract()
        brewery_name = response.xpath('//table//tr/td[@class="hr_bottom_light"]/a/text()').extract()
        beer_brewery_url = response.xpath('//table//tr/td[@class="hr_bottom_light"]/a/@href').extract()
        beer_url = beer_brewery_url[0:2*num_per_page:2]
        brewery_url = beer_brewery_url[1:2*num_per_page:2]
        abv = response.xpath('//table//tr/td[@class="hr_bottom_light"]/span/text()').extract()
        num_ratings_and_score = response.xpath('//table//tr/td[@class="hr_bottom_light"]/b/text()').extract()
        num_ratings = num_ratings_and_score[0:2*num_per_page:2]
        score = num_ratings_and_score[1:2*num_per_page:2]

        num_beers = len(beer_name)
        index = range(0,num_beers)

        for i in index:
            item = RatingSummaryPageItem()
            item['beer_name'] = beer_name[i]
            item['beer_url'] = beer_url[i]
            item['brewery_name'] = brewery_name[i]
            item['brewery_url'] = brewery_url[i]
            item['abv'] = abv[i]
            item['num_ratings'] = num_ratings[i]
            item['score'] = score[i]

            yield item
