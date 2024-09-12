import sqlite3
import scrapy
import re

BASE_LINK = 'https://www.manobalsas.lt'
TEST_ID = 43

class AnswersSpider(scrapy.Spider):
    name = "answers"

    def start_requests(self):
        self.conn = sqlite3.connect('balsas.db')
        cursor = self.conn.cursor()
        for row in cursor.execute('SELECT id FROM politicians;').fetchall():
            tst_id = TEST_ID
            pol_id = row[0]
            yield scrapy.Request(url=f'{BASE_LINK}/politikai/atsakymu_lentele.php?pol_id={pol_id}&tst={tst_id}&all=1', callback=self.parse, cb_kwargs=dict(tst_id=tst_id, pol_id=pol_id))
        cursor.close()
    
    def parse(self, response, tst_id, pol_id):
        for columns in chunk(response.css('td'), 8):
            question = columns[0].css('::text').get()
            q_id = int(question.split('.')[0])
            strongYes = len(columns[1].css('img')) > 0
            maybeYes = len(columns[2].css('img')) > 0
            yesNo = len(columns[3].css('img')) > 0
            maybeNo = len(columns[4].css('img')) > 0
            strongNo = len(columns[5].css('img')) > 0
            dontKnow = len(columns[6].css('img')) > 0
            comment = columns[7].css('::text').get()
            answer = 0
            if strongYes:
                answer = 5
            elif maybeYes:
                answer = 4
            elif yesNo:
                answer = 3
            elif maybeNo:
                answer = 2
            elif strongNo:
                answer = 1
            elif dontKnow:
                answer = 0
            else:
                answer = 0
            
            self.insert(pol_id, tst_id, q_id, answer, comment)

    def insert(self, pol_id, tst_id, q_id, answer, comment):
        sql = 'INSERT INTO answers(pol_id, tst_id, q_id, answer, comment) VALUES(?,?,?,?,?)'
        cur = self.conn.cursor()
        cur.execute(sql, (pol_id, tst_id, q_id, answer, comment))
        self.conn.commit()

def chunk(list, size):
    for i in range(0, len(list), size):
        yield list[i:i + size]