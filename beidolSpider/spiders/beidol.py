import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from beidolSpider.items import IndeedRankingItem
import datetime, re

salaryReHour = re.compile(r"時給(.+?)円")
salaryReMonth = re.compile(r"月給(.+?)円")

def getSalary(salaryStr):

    # test
    resHour = re.search(salaryReHour,salaryStr)
    resMonth = re.search(salaryReMonth,salaryStr)
    salaryNmHour, salaryNmMonth = None, None

    if resHour:
        salaryNmHour = resHour.group(1)
    if resMonth:
        salaryNmMonth = resMonth.group(1)

    return salaryNmHour, salaryNmMonth

class KeywordsindeedSpider(scrapy.Spider):
    
    name = 'beidol'
    allowed_domains = ['www.baitoru.com']
    
    def start_requests(self):

        start_urls = [#'https://www.baitoru.com/kanto/jlist/tokyo',
                      #'https://www.baitoru.com/kanto/jlist/kanagawa',
                      #'https://www.baitoru.com/kanto/jlist/chiba',
                      #'https://www.baitoru.com/kanto/jlist/saitama',
                      #'https://www.baitoru.com/kansai/jlist/shiga/clerk/btp1-btp5/srt2/',
            #"https://www.baitoru.com/kanto/jlist/tokyo/23ku-23kuigai/nerimaku-higashikurumeshi/driver-driversassistant-substitutedriving/srt2/",
            #"https://www.baitoru.com/kanto/jlist/tokyo-kanagawa-chiba-saitama/food/",
            "https://www.baitoru.com/kanto/jlist/saitama/caremanager-facilitycare-specialelderlynursinghome-geriatrichealthservices-grouphome-nursinghome-elderlyhousing-dayservice-careworker/btp3/shain/",
                     ]
        
        # 20 records/page
        #for p in list(range(2,21)):
        for p in list(range(2,8)):
            #start_urls.append(f'https://www.baitoru.com/kanto/jlist/tokyo/page{p}')
            #start_urls.append(f'https://www.baitoru.com/kanto/jlist/kanagawa/page{p}')
            #start_urls.append(f'https://www.baitoru.com/kanto/jlist/chiba/page{p}')
            #start_urls.append(f'https://www.baitoru.com/kanto/jlist/saitama/page{p}')
            start_urls.append(f'https://www.baitoru.com/kanto/jlist/saitama/caremanager-facilitycare-specialelderlynursinghome-geriatrichealthservices-grouphome-nursinghome-elderlyhousing-dayservice-careworker/btp3/page{p}/shain/')
            #start_urls.append(f'https://www.baitoru.com/kanto/jlist/tokyo-kanagawa-chiba-saitama/food/page{p}/')

        
        for url in start_urls:
            
            yield scrapy.Request(url=url, callback=self.parse)
        



    def parse(self, response):
        # cards = response.xpath('//article[@class="list-jobListDetail"]')
        # バイト
        cards = response.xpath('//div[contains(@id,"link_job_detail_pc_jlist_all_")]')
    
        
        for card in cards:
            item = IndeedRankingItem()
            
            detailedUrl =  'https://www.baitoru.com' + card.xpath('.//div[@class="pt02"]//a').attrib['href']
            item['today'] = datetime.date.today()
            item['title'] = card.xpath('.//ul[@class="ul01"]//span/text()').get()
            item['category1'] = card.xpath('.//div[@class="pt03"]/dl[1]//li/span[1]/text()').extract_first()
            item['category2'] = card.xpath('.//div[@class="pt03"]/dl[1]//li/text()[2]').extract_first().strip()
            salaryText = card.xpath('.//div[@class="pt03"]/dl[2]//li/em/text()').get()
            item['salaryText'] = salaryText
            # numHour,numMonth = getSalary(salaryText)
            # item['salaryNmHour'] = numHour
            # item['salaryNmMonth'] = numMonth
            item['workingTime'] = "".join([e.strip() for e in card.xpath('.//div[@class="pt03"]/dl[3]//li//text()').extract() if len(e.strip()) > 0])
            item['location'] =  "".join([e.strip() for e in card.xpath('.//ul[@class="ul02"]//li//text()').extract() if len(e.strip()) > 0])
            item['url'] = detailedUrl
            # pt08が動的になってるからこのまま取れない感じ？
            # item['company'] = card.xpath('.//div[@class="pt08"]//li[@class="li02"]/a').attrib['data-obo_saki']
            # item['tel'] = card.xpath('.//div[@class="pt08"]//li[@class="li02"]/a').attrib['data-obo_tel']
            # item['teltime'] = card.xpath('.//div[@class="pt08"]//li[@class="li02"]/a').attrib['data-tel_obo_time']

                        
            yield scrapy.Request(detailedUrl,
                                 callback=self.parse_detail,
                                 meta={'item':item})
            
    
    def parse_detail(self,response):
        
        item = response.meta['item']
        
        telephoneNumber = response.xpath('//div[contains(@id,"contents")]//a[contains(@class,"tel")]').attrib['data-obo_tel']
        company2 = response.xpath('//div[contains(@id,"contents")]//div[@class="detail-entryInfo"]//dl[@class="dl01"]//dd//text()').extract_first()
        company1 = response.xpath('//div[contains(@id,"contents")]//div[@class="detail-companyInfo"]//div[@class="pt02"]//dd//text()').extract()
            
        item['tel'] = telephoneNumber.strip()
        item['company1'] = [x for x in company1 if len(x.strip()) > 0][0]
        item['company2'] = company2.strip()
        

        yield item
