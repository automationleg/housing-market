# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from collections import OrderedDict
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class OfertyPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('oferty_data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get('cena') or not adapter.get('cena').isdigit():
            raise DropItem(f'no price available')

        for k, v in item.items():
            if v:            
                if k in ['liczba_pokoi','liczba_pieter', 'rok_budowy']:
                    item[k] = int(item[k])
                elif k in ['powierzchnia_uzytkowa', 'cena', 'cena_za_m2']:
                    item[k] = float(item[k])
                elif k == 'pietro':
                    if v == 'parter':
                        item[k] = 0
                    else:
                        item[k] = int(item[k])

        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
