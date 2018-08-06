# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeerAdvocateItem(scrapy.Item):
    #ip_address = scrapy.Field()
    pass

class RatingSummaryPageItem(scrapy.Item):
    beer_name = scrapy.Field()
    beer_url = scrapy.Field()
    brewery_name = scrapy.Field()
    brewery_url = scrapy.Field()
    abv = scrapy.Field()
    num_ratings = scrapy.Field()
    score = scrapy.Field()



class BreweryDetailsItem(scrapy.Item):
    brewery_id = scrapy.Field()
    brewery_name = scrapy.Field()
    brewery_url = scrapy.Field()
    ba_score = scrapy.Field()
    ba_score_desc = scrapy.Field()
    ba_num_ratings = scrapy.Field()
    place_type = scrapy.Field()
    place_address1 = scrapy.Field()
    place_address2 = scrapy.Field()
    place_city = scrapy.Field()
    place_state = scrapy.Field()
    place_postal_code = scrapy.Field()
    place_country = scrapy.Field()
    bs_num_beers = scrapy.Field()
    bs_num_reviews = scrapy.Field()
    bs_num_ratings = scrapy.Field()
    ps_ba_score = scrapy.Field()
    ps_num_reviews = scrapy.Field()
    ps_num_ratings = scrapy.Field()
    ps_pDev = scrapy.Field()

class BeerRatingItem(scrapy.Item):
    brewery_name = scrapy.Field()
    brewery_id = scrapy.Field()
    beer_name = scrapy.Field()
    beer_id = scrapy.Field()
    user_name = scrapy.Field()
    user_url = scrapy.Field()
    rating_agg = scrapy.Field()
    rating_look = scrapy.Field()
    rating_smell = scrapy.Field()
    rating_taste = scrapy.Field()
    rating_feel = scrapy.Field()
    rating_overall = scrapy.Field()
    review = scrapy.Field()
