import scrapy
import re
import sqlite3

BASE_LINK = 'https://www.manobalsas.lt'
TEST_ID = 43

class PoliticiansSpider(scrapy.Spider):
    name = "politicians"

    def start_requests(self):
        self.conn = sqlite3.connect('balsas.db') 
        yield scrapy.Request(url=f'{BASE_LINK}/politikai/politikai.php', callback=self.parse)

    def parse(self, response):
        for party in response.css('div.party'):
            partyName = party.css('h2::text').get()
            for member in party.css('div.list li a'):
                memberName = member.css('::text').get()
                memberLink = member.attrib['href'].replace('..', BASE_LINK)
                yield response.follow(memberLink, self.parseMember, cb_kwargs=dict(politician={
                    'party': partyName,
                    'name': memberName,
                    'link': memberLink,
                })
        )
    
    def parseMember(self, response, politician):
        href = response.css('#more2 a').attrib['href']
        id = re.match('javascript:.+\((\d+)', href).group(1)
        politician['id'] = id
        self.insert(politician)

    def insert(self, p):
        sql = 'INSERT INTO politicians(id,name,party,link) VALUES(?,?,?,?)'
        cur = self.conn.cursor()
        cur.execute(sql, (p['id'], p['name'], p['party'], p['link']))
        self.conn.commit()
