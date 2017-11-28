# -*- coding: utf-8 -*-

from fiftyonejob.items import FiftyOneJobItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
import datetime
import re

class FiftySpider(RedisCrawlSpider):
    name = 'fifty'
    redis_key = 'jobspider:start_urls'
    allowed_domains = ['51job.com']

    rules = (
        Rule(LinkExtractor(allow=r'search.51job.com/jobsearch/search_result.php'),follow=True),
        Rule(LinkExtractor(allow=r'list/.*?(.html)$'),follow=True),    #职位列表页
        Rule(LinkExtractor(allow=r'jobs.51job.com/.*?/\d+.html'),callback='parse_item',follow=True), #详情页
    )

    def parse_item(self, response):
        # print(response.url)
        item = FiftyOneJobItem()
        url = response.url
        enterprise_name = response.xpath('//p[@class="cname"]/a/text()').extract()[0]
        pname = response.xpath('//*[@class="cn"]/h1/text()').extract()[0]
        money = response.xpath('//*[@class="cn"]/strong/text()').extract()[0]
        money = self.format_money(money)
        smoney = money[0]
        emoney = money[1]
        plocation = response.xpath('//*[@class="cn"]/span/text()').extract()[0]
        parea = response.xpath('//*[@class="bmsg inbox"]/p/text()').extract()[1]
        parea = self.format(parea)
        pattern_experience = re.compile(r'class="i1"></em>(.*)</span')
        pattern_education = re.compile(r'class="i2"></em>(.*)</span')
        pattern_pnumber = re.compile(r'class="i3"></em>(.*)</span')
        pattern_date = re.compile(r'class="i4"></em>(.*)</span')
        experience = pattern_experience.search(response.text)
        experience = self.get_re(experience)
        position_education = pattern_education.search(response.text)
        position_education = self.get_re(position_education)
        pnumber = pattern_pnumber.search(response.text)
        pnumber = self.get_re(pnumber)
        date_pub = pattern_date.search(response.text)
        date_pub = self.get_re(date_pub)
        date_pub = date_pub.strip('发布')
        tags = response.xpath('//*[@class="mt10"]/p[2]/span/text()')[1:].extract()
        tags = '、'.join(tags)
        advantage = response.xpath('//*[@class="t2"]/span/text()').extract()
        advantage = '、'.join(advantage)
        jobdesc = ''.join(response.xpath('//*[@class="bmsg job_msg inbox"][1]/text()').extract())
        jobdesc = self.format(jobdesc)
        company_profile = ''.join(response.xpath('//*[@class="tmsg inbox"]/text()').extract())
        company_profile = self.format(company_profile)
        crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')

        item['url'] = url
        item['enterprise_name'] = enterprise_name
        item['pname'] = pname
        item['smoney'] = smoney
        item['emoney'] = emoney
        item['plocation'] = plocation
        item['parea'] = parea
        item['experience'] = experience
        item['position_education'] = position_education
        item['pnumber'] = pnumber
        item['date_pub'] = date_pub
        item['tags'] = tags
        item['advantage'] = advantage
        item['jobdesc'] = jobdesc
        item['company_profile'] = company_profile
        item['crawl_time'] = crawl_time
        item['ptype'] = 0
        yield item

     # 格式化字符串
    def format(self,data):
        return data.strip().replace('\n','').replace('\t','')

    # 没有匹配到结果 则返回空
    def getValue(self, data):
        return data if data else ''

    def get_re(self,data):
        if data:
            data = data.group(1)
        else:
            data = ''
        return data

    # 薪资格式化处理 全部月薪资为基准
    def format_money(self,data):
        if data:
            if '万以上/年' in data:
                smoney = float(data.strip('万以上/年'))*10000/12
                emoney = 0
            elif '万以上/月' in data:
                smoney = float(data.strip('万以上/月'))*10000
                emoney = 0
            elif '万/年' in data:
                smoney = float(data.strip('万/年').split('-')[0])*10000/12
                emoney = float(data.strip('万/年').split('-')[1])*10000/12

            elif '万/月' in data:
                smoney = float(data.strip('万/月').split('-')[0])*1000
                emoney = float(data.strip('万/月').split('-')[1])*1000
            elif '千/月' in data:
                smoney = float(data.strip('千/月').split('-')[0])*1000
                emoney = float(data.strip('千/月').split('-')[1])*1000
            else:
                smoney,emoney = 0
            return smoney,emoney
        else:
            smoney,emoney = 0
        return smoney,emoney
