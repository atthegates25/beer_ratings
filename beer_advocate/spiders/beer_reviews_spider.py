from scrapy import Spider, Request
from beer_advocate.items import BeerRatingItem
from beer_advocate.masking_utilities import *
from lxml.html import fromstring
import pandas as pd
import numpy as np
import re, os, requests
import datetime as dt


class BABeerReviewsSpider(Spider):
    name = "beer_reviews_spider"
    allowed_urls = ["https://www.beeradvocate.com/"]
    start_urls = ["https://www.beeradvocate.com/beer/"]

    # get list of free proxies and use only elite proxies
    def parse(self, response):
        # set base url for all brewery profiles
        base_url = "https://www.beeradvocate.com"
        # import list of breweries to collect data from
        beer_list_filename = "./runs/20180803/data_files/beer_list_20180803.txt"
        beer_list = pd.read_csv(beer_list_filename, sep='\t')
        # filter out beers that have no ratings
        beer_list = beer_list.loc[beer_list['num_ratings'] >= 200,]

        # narrow down list to test
        #beer_list = beer_list[1:25]
        beer_list = beer_list.loc[(beer_list['num_ratings'] >= 1000) & ((beer_list['num_ratings'] < 4500)),]

        # get list of user_agents.  for now, only use first
        user_agent_list = get_user_agent_list()
        user_agent = user_agent_list[0]

        # generate proxy list and associated parameters
        # pass in test url and user agent to return only working proxies
        proxy_list = get_proxy_list(test_url=base_url, user_agent=user_agent) # get list of proxies

        # set parameters for monitoring proxies
        prxy_lst_updt = dt.datetime.now() # set time of last proxy list update
        prxy_updt_interval = 60 # proxy refresh interval in minutes
        num_proxies = len(proxy_list) # get number of proxies
        dt_format = '%m/%d/%Y %H:%M:%S:%f'

        # used for debugging purposes
        print('Proxy list generated at: ' + prxy_lst_updt.strftime(dt_format) + '; length: ' + str(len(proxy_list)))

        for beer in beer_list.iterrows():
            # unpack parameters of beer
            beer = beer[1]
            brewery_id = beer[0]
            beer_id = beer[1]
            brewery_name = beer[2]
            beer_name = beer[3]
            beer_url = base_url + beer[4]

            # check how much time has passed since proxies were refreshed
            # see how much time has passed since last update
            proxy_age_check_now = dt.datetime.now()
            time_since_prxy_updt = proxy_age_check_now - prxy_lst_updt
            print('last update: ' + prxy_lst_updt.strftime(dt_format) + '; now: ' + proxy_age_check_now.strftime(dt_format) + '; time elapsed: ' + str(time_since_prxy_updt.total_seconds()))

            # refresh list if threshold has passed
            if time_since_prxy_updt.total_seconds() > prxy_updt_interval*60:
                proxy_list = get_proxy_list() # get list of proxies
                prxy_lst_updt = dt.datetime.now() # set time of last proxy list update
                num_proxies = len(proxy_list)
                print('Proxy list generated at: ' + prxy_lst_updt.strftime(dt_format) + '; length: ' + str(len(proxy_list)))


            # generate randon proxy
            np.random.seed()
            r = np.random.randint(low=0,high=num_proxies)
            proxy_to_use = proxy_list.iloc[r,0]
            proxy_code = proxy_list.iloc[r,1]
            proxy_last_checked = proxy_list.iloc[r,2]

            # print for debugging purposes
            print('Proxy attempted||Review Start Page||' + str(brewery_id) + '||' + str(beer_id) + '||' + brewery_name + '||' + beer_name + '||' + '||' + proxy_to_use + '||' + proxy_code + '||' + proxy_last_checked)

            yield Request(url=beer_url, headers={'User-Agent': user_agent}, meta={'user_agent': user_agent, 'brewery_id': brewery_id, 'brewery_name': brewery_name, 'beer_id': beer_id, 'beer_name': beer_name, 'beer_url': beer_url, 'proxy': proxy_to_use, 'proxy_used': proxy_to_use}, callback=self.parse_beer_review_start_page)

    def parse_beer_review_start_page(self, response):
        # unpack meta data
        brewery_id = response.meta['brewery_id']
        beer_id = response.meta['beer_id']
        brewery_name = response.meta['brewery_name']
        beer_name = response.meta['beer_name']
        beer_url = response.meta['beer_url']
        proxy = response.meta['proxy_used']
        user_agent = response.meta['user_agent']

        # print success msg for debugging purposes
        print('Proxy successful||Review Start Page||' + str(brewery_id) + '||' + str(beer_id) + '||' + brewery_name + '||' + beer_name + '||' + '||' + proxy)

        # find number of beers and generate corresponding urls
        num_ratings = int(response.xpath('//*[@id="ba-content"]/div[13]/b[1]/text()').extract_first().split(': ')[1].replace(',',''))
        num_per_page = 25
        num_pages = (num_ratings // num_per_page) + 1
        beer_ratings_urls = list(map(lambda i: beer_url + "?view=beer&sort=&start=" + str(num_per_page*i), range(0,num_pages)))

        #print(beer_ratings_urls[0:10])

        #beer_ratings_urls = [beer_url + "?view=beer&sort=&start=" + str(13950)]

        for url in beer_ratings_urls:
            start_num = str(url.split('start=')[1])

            # print for debugging purposes
            print('Proxy attempted||Review Page||' + str(brewery_id) + '||' + str(beer_id) + '||' + brewery_name + '||' + beer_name + '||' + start_num + '||' + proxy)

            yield Request(url=url, headers={'User-Agent': user_agent}, meta={'brewery_id': brewery_id, 'brewery_name': brewery_name, 'beer_id': beer_id, 'beer_name': beer_name, 'start_num': start_num, \
                'proxy': proxy, 'proxy_used': proxy}, callback=self.parse_beer_review_page)

    def parse_beer_review_page(self, response):
        # unpack meta data
        brewery_id = response.meta['brewery_id']
        beer_id = response.meta['beer_id']
        brewery_name = response.meta['brewery_name']
        beer_name = response.meta['beer_name']
        start_num = response.meta['start_num']
        proxy = response.meta['proxy_used']

        # print success msg for debugging purposes
        print('Proxy successful||Review Page||' + str(brewery_id) + '||' + str(beer_id) + '||' + brewery_name + '||' + beer_name + '||' + start_num + '||' + proxy)

        # get container for all reviews on page
        main_box = response.xpath('//*[@id="rating_fullview"]')
        reviews = main_box.xpath('div[@id="rating_fullview_container"]')

        for review in reviews:
            rating_agg = review.xpath('div[@id="rating_fullview_content_2"]/span[@class="BAscore_norm"]/text()').extract_first()
            component_ratings = review.xpath('div[@id="rating_fullview_content_2"]/span[@class="muted"]/text()')
            # check if component ratings exist
            if component_ratings == None:
                rating_look = ''
                rating_smell = ''
                rating_taste = ''
                rating_feel = ''
                rating_overall = ''
            else:
                # filter out element with number of characters of the review
                component_ratings = list(map(lambda s: s.replace(',',''), component_ratings.extract()))
                component_ratings = list(filter(lambda s: re.search('^\d+ characters$', s) == None, component_ratings))
                if component_ratings == []:
                    rating_look = ''
                    rating_smell = ''
                    rating_taste = ''
                    rating_feel = ''
                    rating_overall = ''
                else:
                    component_ratings = list(map(lambda s: s.replace(' ','').split(':'),component_ratings[0].split('|')))
                    rating_look = component_ratings[0][1]
                    rating_smell = component_ratings[1][1]
                    rating_taste = component_ratings[2][1]
                    rating_feel = component_ratings[3][1]
                    rating_overall = component_ratings[4][1]

            review_section = review.xpath('div[@id="rating_fullview_content_2"]/text()')
            # check if review exists
            if len(review_section) > 1:
                review_text = review_section.extract()
                review_text = ''.join(list(filter(lambda s: s.find('rDev')==-1, review_text)))
                review_text = review_text.replace('\n','_@@_')
            else:
                review_text = ''
            user_name = review.xpath('div[@id="rating_fullview_content_2"]/div//a/text()')[0].extract()
            user_url = review.xpath('div[@id="rating_fullview_content_2"]/div//a/@href')[0].extract()

            item = BeerRatingItem()
            item['brewery_name'] = brewery_name
            item['brewery_id'] = str(brewery_id)
            item['beer_name'] = beer_name
            item['beer_id'] = str(beer_id)
            item['user_name'] = user_name
            item['user_url'] = user_url
            item['rating_agg'] = rating_agg
            item['rating_look'] = rating_look
            item['rating_smell'] = rating_smell
            item['rating_taste'] = rating_taste
            item['rating_feel'] = rating_feel
            item['rating_overall'] = rating_overall
            item['review'] = review_text

            yield item
