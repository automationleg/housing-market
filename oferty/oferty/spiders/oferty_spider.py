import scrapy

import re
from .dzielnice import dzielnice_dict
from oferty.items import FlatItem

class WarsawDistricts(scrapy.Spider):
    name = 'districts'

    # url to get all warsaw districts
    start_urls = ['https://www.oferty.net/mieszkania,warszawa']
    


class FlatsSpider(scrapy.Spider):
    name = 'oferty'

    cities = ['Warszawa', 'Krakow', 'Gdansk']

    start_urls = ['https://www.oferty.net/mieszkania/szukaj?ps%5Blocation%5D%5Btype%5D=1&ps%5Btype%5D=1&ps%5Btransaction%5D=1&ps%5Blocation%5D%5Btext%5D=Warszawa']

    def parse(self, response):
        # follow links to flat pages
        for href in response.css('td.cell_location>a::attr(href)'):
            yield response.follow(href, self.parse_flats)

        # follow pagination links
        for href in response.css('li.arrow.navigateNext a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_flats(self, response):
        Item = FlatItem()

        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()
        
        
        def extract_address_data(address_string: str):
            address_parts = [item.strip() for item in address_string.split(',')]

            # find district
            district = [item.replace('-', ' ') for item in address_parts 
                        if item.replace('-', ' ') in dzielnice_dict
                        ]
            if district:
                district = district[0]

            # find subdistrict
            subdistrict = [item for item in address_parts 
                           if item in dzielnice_dict[district]] if district else ''
                           
            if subdistrict:
                subdistrict = subdistrict[0]
                address_parts.remove(subdistrict)

            # find city
            city = [item for item in address_parts if item in self.cities][0]

            # find street name
            street = address_parts[-1]
            return city, district, subdistrict, street

        address_string = ''.join(response.xpath('//h1/text()').getall())
        Item['miasto'], Item['dzielnica'], Item['poddzielnica'], Item['ulica'] = extract_address_data(address_string)
        
        try:
            cena = extract_with_xpath('//h3/text()')
            cena = re.search(r'\bCena: (.*)\sPLN\b', cena).group(1).replace(' ','')
        except:
            pass

        try:
            cena_za_m2 = extract_with_xpath('//dl/dt[contains(text(), "Cena za m")]/following-sibling::dd[1]/text()')
            cena_za_m2 = re.findall(r'(\d+\s?\d+,?\d*)', cena_za_m2)[0].replace(',', '.').replace(" ", "")
        except:
            pass

        try:
            powierzchnia = extract_with_xpath('//dl/dt[contains(text(), "Powierzchnia użytkowa")]/following-sibling::dd[1]/text()')
            powierzchnia = re.findall(r'(\d+\s?\d+,?\d*)', powierzchnia)[0].replace(',', '.').replace(" ", "")
        except:
            pass

        Item['cena'] = cena
        Item['cena_za_m2'] = cena_za_m2
        Item['powierzchnia_uzytkowa'] = powierzchnia
        Item['liczba_pokoi'] = extract_with_xpath('//dl/dt[contains(text(), "Liczba pokoi")]/following-sibling::dd[1]/text()')
        Item['pietro'] = extract_with_xpath('//dl/dt[contains(text(), "Piętro")]/following-sibling::dd[1]/text()')
        Item['liczba_pieter'] = extract_with_xpath('//dl/dt[contains(text(), "Liczba pięter")]/following-sibling::dd[1]/text()')
        Item['rok_budowy'] = extract_with_xpath('//dl/dt[contains(text(), "Rok budowy")]/following-sibling::dd[1]/text()')
        Item['rynek_pierwotny'] = extract_with_xpath('//dl/dt[contains(text(), "Rynek pierwotny")]/following-sibling::dd[1]/text()')
        Item['url'] = response.request.url

        yield Item


# if __name__ == "__main__":
#     process = Crawl()
#     process.crawl(FlatsSpider)
#     process.start()