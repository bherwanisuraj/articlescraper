import scrapy
import pandas as pd
import time
import w3lib

import re
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from articlescrapper.items import ArticlescrapperItem

input = pd.read_excel(r'C:\Users\bherw\OneDrive\Desktop\Suraj\Test\Blackcoffer\articlescrapper\articlescrapper\spiders\Input.xlsx')
# urls = input['URL'].to_numpy()
# uids = input['URL_ID']

class ArticlespiderSpider(scrapy.Spider):
    urls = input['URL'].to_numpy()
    uids = input['URL_ID']
    id = 0
    name = "articlespider"
    allowed_domains = ["insights.blackcoffer.com"]
    # start_urls = [url for url in urls]


    #['https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the-economy-environment-infrastructure-and-city-life-by-the-year-2040-2/']#["https://insights.blackcoffer.com"]

    # def start_requests(self):
    #     urls = "https://insights.blackcoffer.com/rise-of-cyber-crime-and-its-effects/"
    #     yield scrapy.Request(urls, meta=dict(
    #         playwright = True,
    #         playwright_include_page = True,
    #         playwright_page_methods = [
    #             PageMethod('wait_for_selector', 'div.td-post-content'),
    #         ],
    #     ))

    def start_requests(self):
        # for url in self.urls:
        #     url = "https://insights.blackcoffer.com/covid-19-environmental-impact-for-the-future/"
        #     code = SeleniumRequest(url=url, callback=self.parse, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'td-post-content')))
        #     print(f"Code _____________________________{type(code)}")
        #     print(f"Code _____________________________{code}")
        #     print(code.body)
        #     yield code
        #     break

        for url, uid in zip(self.urls, self.uids):
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=EC.presence_of_element_located((By.CLASS_NAME, 'td-post-content')),
                meta={'uid': uid}
            )


    def parse(self, response):

        # print(f"Type {type(response.status)}")

        if response.status == 404:
            self.logger.warning(f"404 Not Found for URL: {response.url}")
            # Handle 404 response here, for example, by logging or storing the URL in a separate list
        # print(f"Type #########{response.status}")

        # if response.status == 200:

        # articleItem = ArticlescrapperItem()
        #
        # articleItem['uid'] = self.uids[self.id]
        # # print(articleItem['uid'])
        # articleItem['title'] = response.css('h1').get()
        # # print(articleItem['title'])
        # articleItem['article'] = response.css('div.td-post-content').get()
        #
        # # print(self.uids[self.id] + "--------------------------------------------------------")
        #
        # # file = open(f"articles/{uids[id]}", 'w')
        # # file = open(f"articles/{articleItem['uid']}.txt", 'w+', encoding="utf-8")
        # # file.write(articleItem['title'] + " " + articleItem['article'])
        # # file.close()
        # self.id += 1
        # yield articleItem
        # # time.sleep(1)
        #
        # # else:
        # #     self.id += 1

        else:
            articleItem = ArticlescrapperItem()

            articleItem['uid'] = response.meta['uid']

            articleItem['title'] = response.css('h1::text').get()
            articleItem['title'] = re.sub(' +', ' ', articleItem['title'])
            articleItem['title'] = w3lib.html.remove_tags(articleItem['title'])
            articleItem['title'] = articleItem['title'].replace('NBSP', " & ")
            articleItem['article'] = response.css('div.td-post-content').get()
            articleItem['article'] = re.sub(' +', ' ', articleItem['article'])
            articleItem['article'] = articleItem['article'].replace('\r', "")
            articleItem['article'] = articleItem['article'].replace('\n', "")
            articleItem['article'] = articleItem['article'].replace('\t', "")
            articleItem['article'] = articleItem['article'].replace(' ', " & ")
            articleItem['article'] = w3lib.html.remove_tags_with_content(articleItem['article'], ('pre',))
            articleItem['article'] = w3lib.html.remove_tags(w3lib.html.remove_tags_with_content(articleItem['article'], ('style',)))



            yield articleItem

            # file = open(f"articles/{articleItem['uid']}", 'w')
            file = open(f"articles/{articleItem['uid']}.txt", 'w+', encoding="utf-8")
            file.write(articleItem['title'] + " " + articleItem['article'])
            file.close()



