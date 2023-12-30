# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import w3lib.html
import re


def remove_tag(value):
    value = re.sub(' +', ' ', value)
    value = w3lib.html.remove_tags(value)
    value = value.replace('NBSP', " & ")
    return value

def remove_tag_item(value):
    value = re.sub(' +', ' ', value)
    value = value.replace('\r', "")
    value = value.replace('\n', "")
    value = value.replace('\t', "")
    value = value.replace(' ', " & ")
    value = w3lib.html.remove_tags_with_content(value, ('pre', ))
    return w3lib.html.remove_tags(w3lib.html.remove_tags_with_content(value, ('style', )))

class ArticlescrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = scrapy.Field()
    title = scrapy.Field(serializer=remove_tag)
    article = scrapy.Field(serializer=remove_tag_item)
