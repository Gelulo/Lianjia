# -*- coding: utf-8 -*-
import scrapy
from lianjiaSpider.settings import headers
import time, random, os
from urllib import request
from lianjiaSpider.items import lianjiaSpiderItem
class LianjiaSpider(scrapy.Spider):
    name = 'Lianjia'
    allowed_domains = ['lianjia.com']
    # start_urls = ['http://lianjia.com/']

#重新定义抓取地址
    def start_requests(self):
        start_urls = []
        for page in range(1,3):
            url = "https://bj.lianjia.com/zufang/chaoyang/pg{}".format(page)
            start_urls.append(url)
        for start_url in start_urls:
            yield scrapy.Request(url=start_url, headers=headers, callback=self.parse, dont_filter=True)
    def parse(self, response):
        # print(response.body.decode("utf-8"))
        infos = response.xpath("//div[@class='content__list']/div[@class='content__list--item']")
        # print(infos)
        for info in infos:
            # print(info)
            #获取房屋的名字
            house_title = info.xpath(".//p[@class='content__list--item--title twoline']/a/text()").extract()
            house_title = house_title[0].strip().replace(' ','')
            print(house_title)

            #获取房屋详情链接
            house_href = info.xpath(".//p[@class='content__list--item--title twoline']/a/@href").extract()
            house_href = "https://bj.lianjia.com"+house_href[0]
            # print(house_href)

            #获取房源位置
            house_add = info.xpath(".//p[@class='content__list--item--des']/a/text()").extract()
            house_add = '-'.join(house_add)
            # print(house_add)
            # time.sleep(random.choice([0,1,1,2,2,3,4,5]))
            yield scrapy.Request(url=house_href, headers=headers, callback=self.detail_parse, dont_filter=True, meta={"house_title":house_title,"house_href":house_href,"house_add":house_add})
    def detail_parse(self,response):
        #获取房屋详细信息
        infos = response.xpath("//div[@class='content clear w1150']")
        # print(infos)
        for info in infos:
            #获取房屋编号
            house_nums = info.xpath(".//i[@class='house_code']/text()").extract()
            house_num = house_nums[0].split("：")[-1]
            # print(house_num)
            #获取房屋价格
            house_price = info.xpath(".//p[@class='content__aside--title']/span/text()").extract()
            house_price = house_price[0]+"元/月"
            # print(house_price)
            #获取房屋具体信息
            house_infos = info.xpath(".//p[@class='content__article__table']//span/text()").extract()
            #获取出租方式
            house_style = house_infos[0]
            #获取厅室信息
            house_tingshi = house_infos[1]
            #获取房屋面积
            house_size = house_infos[2]
            #房屋朝向
            house_direction = house_infos[3]
            # print(house_style,"--",house_tingshi,"--",house_size,"--",house_direction)

            #图片地址
            house_imgdir = '/home/tlxy/Dome/lianjiaSpider/lianjia_img/'+response.meta['house_title']
            # print(house_imgdir)

            #进行数据存储
            item = lianjiaSpiderItem()

            item["house_title"] = response.meta["house_title"]
            item["house_href"] = response.meta["house_href"]
            item["house_add"] = response.meta["house_add"]
            item["house_num"] = house_num
            item["house_price"] = house_price
            item["house_style"] = house_style
            item["house_tingshi"] = house_tingshi
            item["house_size"] = house_size
            item["house_direction"] = house_direction
            item["house_imgdir"] = house_imgdir

            yield item

            # #图片信息处理
            # house_imgurls = info.xpath(".//div[@class='content__article__slide__item']/img/@src").extract()
            # # print(house_imgurl)
            # if len(house_imgurls) !=0:
            #     for down_url in house_imgurls:
            #         #图片名称
            #         img_name = str(time.time()) + '.jpg'
            #         if not os.path.exists(house_imgdir):
            #             os.makedirs(house_imgdir)
            #
            #         request.urlretrieve(down_url,house_imgdir+"/"+img_name)
            #         print(down_url)
