from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from ..items import ExpansysItem
from ..pipelines import ExpansysPipeline
from datetime import datetime

class ExpansysSpider(CrawlSpider):

    name = 'expansys'
    allowed_domains = ['expansys.com.sg']
    start_urls = ['http://www.expansys.com.sg/mobile-phones']
    #rules = [Rule(LxmlLinkExtractor(allow=''),callback='parse_item',follow=True)]    
    
    rules = (Rule(LxmlLinkExtractor(allow=(''), restrict_xpaths=('//a[@class="next"]',)), callback="parse_items", follow= True),)
    
    item = ExpansysItem()
    
    pipeline = set([
        ExpansysPipeline
    ])
    
    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jayjay="wewewe"
        item = ExpansysItem()
        for r in response.xpath('//html'):
            item['title'] = r.xpath('//h1[@itemprop="name"]/text()').extract()
            item['urls'] =  r.xpath('//link/@href')[0].extract()
            item['price'] = r.xpath('//span[@itemprop="price"]/text()').extract()
            #item['currency'] = r.xpath('//p[@id="price"]/meta/@content').extract()
            item['sku']=r.xpath('//ul[@class="product-sku"]/li/span/@content').extract()
            #item['category'] =r.xpath('//ul[@id="breadcrumbs"]//span/text()').extract()
            items.append(item)
        return(items)