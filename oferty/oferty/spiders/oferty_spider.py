import scrapy
import re
from .dzielnice import dzielnice_dict

class WarsawDistricts(scrapy.Spider):
    name = 'districts'

    # url to get all warsaw districts
    start_urls = ['https://www.oferty.net/mieszkania,warszawa']
    


class QuotesSpider(scrapy.Spider):
    name = 'oferty'

    start_urls = ['https://www.oferty.net/mieszkania/szukaj?ps%5Blocation%5D%5Btype%5D=1&ps%5Btype%5D=1&ps%5Btransaction%5D=1&ps%5Blocation%5D%5Btext%5D=Warszawa']

    def parse(self, response):
        # follow links to flat pages
        for href in response.css('td.cell_location>a::attr(href)'):
            yield response.follow(href, self.parse_flats)

        # follow pagination links
        for href in response.css('li.arrow.navigateNext a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_flats(self, response):
        def extract_with_css(query):
            return response.xpath(query).get(default='').strip()
        
        def extract_location(query, adtype):
            extracted = response.xpath(query).get(default='').split(',')

            address_string = [item.strip() for item in extracted]
            district = [item for item in address_string if (item in dzielnice_dict) or (item.replace(' ','-') in dzielnice_dict)]
            if district:
                district = district[0]
                address_string.remove(district)
                
            subdistrict = [item for item in address_string if item in dzielnice_dict[district]] if district else ''
            if subdistrict:
                subdistrict = subdistrict[0]
                address_string.remove(subdistrict)
            
            miasto = [item for item in address_string if item == 'Warszawa']
            if miasto:
                miasto = miasto[0]
                address_string.remove(miasto)
            
            ulica = address_string[0]
            if adtype == 'miasto':
                return miasto
            if adtype == 'dzielnica':
                 return district
            if adtype == 'poddzielnica':
                 return subdistrict                 
            if adtype == 'ulica':
                return ulica



        def extract_prices(query):
            extracted = response.xpath(query).get(default='').split(',')
            return re.findall(r'(\d+\s?\d+,?\d*)', extracted)[0].replace(',', '.').replace(" ", "")


        yield {
            'miasto': extract_location('string(//h1)','miasto'), 
            'dzielnica': extract_location('string(//h1)','dzielnica'), 
            'poddzielnica': extract_location('string(//h1)','poddzielnica'), 
            'ulica': extract_location('string(//h1)','ulica'), 
            'cena': re.findall(r'(\d+\s?\d+)', extract_with_css('//h3/text()'))[1].replace(',', '.').replace(" ", ""), 
            'cena za m2': re.findall(r'(\d+\s?\d+,?\d*)', extract_with_css('//dl/dt[contains(text(), "Cena za m")]/following-sibling::dd[1]/text()'))[0].replace(',', '.').replace(" ", ""),
            'powierzchnia uzytkowa': re.findall(r'(\d+\s?\d+,?\d*)', extract_with_css('//dl/dt[contains(text(), "Powierzchnia użytkowa")]/following-sibling::dd[1]/text()'))[0].replace(',', '.').replace(" ", ""),
            'liczba pokoi': extract_with_css('//dl/dt[contains(text(), "Liczba pokoi")]/following-sibling::dd[1]/text()'),
            'pietro': extract_with_css('//dl/dt[contains(text(), "Piętro")]/following-sibling::dd[1]/text()'),
            'liczba pieter': extract_with_css('//dl/dt[contains(text(), "Liczba pięter")]/following-sibling::dd[1]/text()'),
            'rok budowy': extract_with_css('//dl/dt[contains(text(), "Rok budowy")]/following-sibling::dd[1]/text()'),
            'rynek pierwotny': extract_with_css('//dl/dt[contains(text(), "Rynek pierwotny")]/following-sibling::dd[1]/text()'),
            
        }