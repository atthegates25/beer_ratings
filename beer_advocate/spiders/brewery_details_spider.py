from scrapy import Spider, Request
from beer_advocate.items import BreweryDetailsItem
from beer_advocate.masking_utilities import *
from lxml.html import fromstring
import pandas as pd
import numpy as np
import re, os, requests
import datetime as dt


class BABreweryDetailsSpider(Spider):
    name = "brewery_details_spider"
    allowed_urls = ["https://www.beeradvocate.com/"]
    start_urls = ["https://www.beeradvocate.com/beer/"]

    # get list of free proxies and use only elite proxies
    def parse(self, response):
        # set base url for all brewery profiles
        base_url = "https://www.beeradvocate.com"
        # import list of breweries to collect data from
        brewery_list_filename = "./runs/20180803/remaining_breweries.txt"
        brewery_list = pd.read_csv(brewery_list_filename, sep='\t')

        # narrow down list to test
        #brewery_list = brewery_list[0:3]

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

        # used for debugging purposes
        print('Proxy list generated at: ' + prxy_lst_updt.strftime(dt_format) + '; length: ' + str(len(proxy_list)))

        for brewery in brewery_list.iterrows():
            #check how much time has passed since proxies were refreshed
            brewery = brewery[1]
            brewery_id = brewery[0]
            brewery_name = brewery[1]
            brewery_url = base_url + brewery[2]
            #print(str(brewery_id) + '; ' + brewery_name + '; ' + brewery_url)

            # generate randon integer
            np.random.seed()
            r = np.random.randint(low=0,high=num_proxies)
            proxy_to_use = proxy_list.iloc[r,0]
            proxy_code = proxy_list.iloc[r,1]
            proxy_last_checked = proxy_list.iloc[r,2]
            print('Proxy attempted||' + str(brewery_id) + '||' + brewery_name + '||' + proxy_to_use + '||' + proxy_code + '||' + proxy_last_checked)
            yield Request(url=brewery_url, headers={'User-Agent': user_agent}, meta={'brewery_id': brewery_id, 'brewery_name': brewery_name, 'brewery_url': brewery_url, 'proxy': proxy_to_use, 'proxy_used': proxy_to_use}, callback=self.parse_brewery_detail_page)

    def parse_brewery_detail_page(self, response):
        # unpack meta data
        brewery_id = response.meta['brewery_id']
        brewery_name = response.meta['brewery_name']
        brewery_url = response.meta['brewery_url']

        # print success msg for debugging purposes
        print('Proxy successful||' + str(brewery_id) + '||' + brewery_name + '||' + response.meta['proxy_used'])

        # parse page
        # table with all relevant data
        main_box = response.xpath('//*[@id="ba-content"]')
        # table with score info
        score_box = main_box.xpath('div//div[@id="score_box"]')
        ba_score = score_box.xpath('//span[@class="ba-ravg"]/text()').extract_first()
        ba_score_desc = score_box.xpath('b[2]/text()').extract_first()
        ba_num_ratings = score_box.xpath('text()')[5].extract().split('\t')[0].replace(',','')

        # main stats table
        stats_box = main_box.xpath('//div[@id="stats_box"]')
        # beer stats table & corresponding stats
        bs_box = stats_box.xpath('div[2]')
        bs_num_beers, bs_num_reviews, bs_num_ratings = list(map(lambda s: s.replace(',',''),bs_box.xpath('div/dl/dd/text()').extract()))

        # place stats box
        ps_box = stats_box.xpath('div[4]')
        #print(type(ps_box))
        if ps_box == []:
            ps_ba_score = ''
            ps_num_reviews = ''
            ps_num_ratings = ''
            ps_pDev = ''
        else:
            ps_ba_score = ps_box.xpath('div/dl/dd[1]/a/text()').extract_first().split('/')[0]
            ps_num_reviews = ps_box.xpath('div/dl/dd[2]/span/text()').extract_first().replace(',','')
            ps_num_ratings = ps_box.xpath('div/dl/dd[3]/span/text()').extract_first().replace(',','')
            ps_pDev = ps_box.xpath('div/dl/dd[4]/span/text()').extract_first().replace('\t','').replace('\n','')

        # info box
        info_box = main_box.xpath('//div[@id="info_box"]')
        place_type, place_address1, place_address2, place_postal_code = list(map(lambda s: s.replace('\t','').replace('\n','').replace('\r',''),info_box.xpath('text()').extract()))[4:8]
        place_city = info_box.xpath('a[1]/text()').extract_first()
        place_state = info_box.xpath('a[2]/text()').extract_first()
        place_country = info_box.xpath('a[3]/text()').extract_first()

        item = BreweryDetailsItem()
        item['brewery_id'] = str(brewery_id)
        item['brewery_name'] = brewery_name
        item['brewery_url'] = brewery_url
        item['ba_score'] = ba_score
        item['ba_score_desc'] = ba_score_desc
        item['ba_num_ratings'] = ba_num_ratings
        item['place_type'] = place_type
        item['place_address1'] = place_address1
        item['place_address2'] = place_address2
        item['place_city'] = place_city
        item['place_state'] = place_state
        item['place_postal_code'] = place_postal_code
        item['place_country'] = place_country
        item['bs_num_beers'] = bs_num_beers
        item['bs_num_reviews'] = bs_num_reviews
        item['bs_num_ratings'] = bs_num_ratings
        item['ps_ba_score'] = ps_ba_score
        item['ps_num_reviews'] = ps_num_reviews
        item['ps_num_ratings'] = ps_num_ratings
        item['ps_pDev'] = ps_pDev

        yield item
