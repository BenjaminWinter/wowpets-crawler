# -*- coding: utf-8 -*-
import scrapy
import json

class PetsSpider(scrapy.Spider):
    name = 'pet'
    pets = []
    def start_requests(self):
        url = 'https://worldofwarcraft.com/en-gb/character/{}/{}/collections/pets'.format(self.realm, self.char)
        yield scrapy.Request(url=url, callback=self.parse)

        #undermine_url = 'https://theunderminejournal.com/#eu/{}/category/battlepets'.format(self.targetrealm)


    def parse(self, response):
        print('Parsing pets')
        self.pets = response.css('.Pet--hover:not([disabled])').css('.Pet-name::text').extract()
        self.pets = [self.trimtolower(x) for x in self.pets]
        undermine_url='https://theunderminejournal.com/api/category.php?house=188&id=battlepets'

        yield scrapy.FormRequest(url=undermine_url, callback=self.parse_undermine)

    def parse_undermine(self, response):
        print('Parsing Undermine')
        obj = json.loads(response.body)['results'][0]['data']
        filtered = []
        for x in obj:
            for y in obj[x]:
                data = obj[x][y]
                if self.trimtolower(data['name_enus']) in self.pets:
                    filtered.append({
                        'name': data['name_enus'],
                        'price': data['avgprice']
                    })
        print('*****************\n\r\n\r')
        print(json.dumps(sorted(filtered, key=lambda k: -k['price']), indent=1))
        print('*****************\n\r\n\r')
        pass

    def trimtolower(self, string):
        return ''.join(e for e in string if e.isalnum())