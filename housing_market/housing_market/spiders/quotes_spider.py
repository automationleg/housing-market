import scrapy


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

        yield {
            'header': extract_with_css('//h1'), 
            'cena': extract_with_css('//h3'), 
            'cena za m2': extract_with_css('//dl/dt[contains(text(), "Cena za m")]/following-sibling::dd[1]'),
            'powierzchnia uzytkowa': extract_with_css('//dl/dt[contains(text(), "Powierzchnia użytkowa")]/following-sibling::dd[1]'),
            'liczba pokoi': extract_with_css('//dl/dt[contains(text(), "Liczba pokoi")]/following-sibling::dd[1]'),
            'pietro': extract_with_css('//dl/dt[contains(text(), "Piętro")]/following-sibling::dd[1]'),
            'liczba pieter': extract_with_css('//dl/dt[contains(text(), "Liczba pięter")]/following-sibling::dd[1]'),
            'rok budowy': extract_with_css('//dl/dt[contains(text(), "Rok budowy")]/following-sibling::dd[1]'),
            'rynek pierwotny': extract_with_css('//dl/dt[contains(text(), "Rynek pierwotny")]/following-sibling::dd[1]'),
            
        }