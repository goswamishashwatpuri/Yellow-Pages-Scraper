# -*- coding: utf-8 -*-
import scrapy

class PagesSpider(scrapy.Spider):
    name = 'pages'
    allowed_domains = ['yellowpages.com']
    current_row_number = 0
    

    def __init__(self, niche='', location=''):
        niche = input('enter the niche : ')
        location = input('enter the location : ')
        self.niche = '+'.join(niche.split(' '))
        self.location = '+'.join(location.split(' '))
        self.number_of_rows = input("Number of Rows you want to fetch : ")
        if self.number_of_rows == '':
            self.number_of_rows = 30
        else :
            self.number_of_rows = int(self.number_of_rows)    

    def start_requests(self):
        yield scrapy.Request(
            url= f'http://www.yellowpages.com/search?search_terms={self.niche}&geo_location_terms={self.location}',
            callback= self.parse,
        )    
        

    def parse(self, response):

        if self.current_row_number < self.number_of_rows:

            results = response.xpath("//div[@class='info']")

            for result in results:
                tagsxpath = result.xpath(".//div/div[@class='categories']/a[1 <= position() and position() <= last()]")
                addressxpath = result.xpath(".//div/p[@class='adr']/following-sibling::div")

                title = result.xpath(".//h2/a/span/text()").get()
                tags = (', '.join ( tag.xpath(".//text()").get() for tag in tagsxpath ) ).strip()
                website = result.xpath(".//div/div[@class='links']/a/@href").get()
                address = ( ' '.join ( addressline.xpath(".//text()").get() for addressline in addressxpath) ).strip()
                contact = result.xpath(".//descendant::div[@class ='phones phone primary']/text()").get()

                #user_ag = response.request.headers['User-Agent']
                #print(user_ag)

                info = {
                    "Title"   : title,
                    "Tags"    : tags,
                    "Website" : website,
                    "Address" : address,
                    "Contact" : contact,
                    
                }
                self.current_row_number += 1
                yield info
            
            #next_page = 'https://www.yellowpages.com{}'.format(response.xpath("//a[@class='next ajax-page']/@href").get()) 
            #print('\n\n\n\n',next_page,'\n\n\n\n')
            #if next_page :
                #  yield scrapy.Request (
                #      url= next_page,
                #      callback= self.parse,
                #  )

            yield response.follow(
                url= response.xpath("//a[@class='next ajax-page']/@href").get(),
                callback= self.parse
            )