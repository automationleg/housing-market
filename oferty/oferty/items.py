# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import json
from collections import OrderedDict


class OrderedItem(scrapy.Item):
    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __repr__(self):
        return json.dumps(OrderedDict(self), ensure_ascii = False)  # it should return some string

class FlatItem(OrderedItem):
    # define the fields for your item here like:
    miasto = scrapy.Field()
    dzielnica = scrapy.Field()
    poddzielnica = scrapy.Field()
    ulica = scrapy.Field()
    cena = scrapy.Field()
    cena_za_m2 = scrapy.Field()
    powierzchnia_uzytkowa = scrapy.Field()
    liczba_pokoi = scrapy.Field()
    pietro = scrapy.Field()
    liczba_pieter = scrapy.Field()
    rok_budowy = scrapy.Field()
    rynek_pierwotny = scrapy.Field()
    url = scrapy.Field()

    # def __repr__(self):
    #     return f"miasto: {self['miasto']}, dzielnica: {self['dzielnica']}, poddzielnica: {self['poddzielnica']}, ulica: {self['ulica']}"
    
