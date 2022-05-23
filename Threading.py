import time

from fake_ip import *
from lxml import etree
import random

class thr_ip:
    def __init__(self):
        self.ip = getIP()
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("[{}]创建了新线程，ip为{}".format(t, self.ip))

    def fakeIPGet(self, url):
        time.sleep(random.uniform(2, 5))
        ip = self.ip
        username = '1207937423'
        password = 'dmi2p7ps'
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
        }
        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": ip},
            "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": ip}
        }

        try:
            response = requests.get(url, proxies=proxies, headers=headers)
            return response
        except Exception as e:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("[{}]代理ip ".format(t) + ip + "产生异常，即将更换ip.", 'Exception:', str(e))
            time.sleep(random.random() * 5)
            self.ip = getIP()
            return self.fakeIPGet(url)

    def get(self, url):  # 给定url，返回响应
        # 爬虫基本参数设置
        # ssl._create_default_https_context = ssl._create_unverified_context
        URL = "https://pellet-stove-parts-4less.com"
        return self.fakeIPGet(URL + url)

    def findAllBrand(self, url):  # 查找所有品牌
        res = self.get(url)
        html = etree.HTML(res.text)
        result = [html.xpath('//div[@class=" manufacturer-image-navigation"]/a/@href'),
                  html.xpath('//div[@class=" manufacturer-image-navigation"]/a/@title')]
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("[{}]started".format(t))
        return result

    def findAllModel(self, brand, url):  # 给定品牌和url，查找所有型号
        res = self.get(url)
        html = etree.HTML(res.text)
        result = [html.xpath('//div[@class=" manufacturer-image-navigation"]/a/@href'),
                  html.xpath('//div[@class=" manufacturer-image-navigation"]/a/@title')]
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("[{}]正在搜索 ".format(t) + brand + " 品牌下的所有产品......")
        return brand, result

    def findAllProduct(self, model, url):
        res = self.get(url)
        html = etree.HTML(res.text)
        result = html.xpath('//a[@class="productitem--image-link"]/@href')
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("[{}]正在搜索型号".format(t) + model + "......")
        return model, result

    def findAllItem(self, url):
        res = self.get(url)
        html = etree.HTML(res.text)
        # 去除价格小于$20.00的产品
        tempRes_money = html.xpath('//span[@class="money"]/text()')
        money = tempRes_money[0].replace("\n", "").replace("$", "").replace(" ", "")
        if float(money) < 20.00:
            return 0, []
        # 产品标题
        tempRes_productTitle = html.xpath('//h1[@class="product-title"]/text()')
        productTitle = tempRes_productTitle[0].replace("\n", "").replace("\t", "").replace("  ", "")
        # 描述
        tempRes_description = html.xpath(
            '//div[@class="tabPanel"]//div[@id="description-content" and @role="tabpanel" and @aria-labelledby="description-content"]/span/b/text()')
        description = ""
        if len(tempRes_description) > 0:
            description = description + tempRes_description[0]
            temp_descriptionList = html.xpath(
                '//div[@class="tabPanel"]//div[@id="description-content" and @role="tabpanel" and @aria-labelledby="description-content"]/ul[@style="margin-top: 5px;"]/li/text()')
            for i in range(len(temp_descriptionList)):
                description = description + "\n" + temp_descriptionList[i]
        # 适用机型
        compatibleModels = ""
        temp_ul = html.xpath(
            '//div[@class="tabContainer"]/div[@class="tabPanel"]//div[@id="description-content" and @role="tabpanel" and @aria-labelledby="description-panel-content"]/div/ul')
        for ul in temp_ul:
            modelName = ul.xpath('./p[@class="ac-compat-stove-manufacturer"]/text()')
            if (len(modelName)) == 0:
                continue
            compatibleModels = compatibleModels + modelName[0] + ":\n"
            modelList = ul.xpath('./li[@class="ac-compat-stove-model"]/text()')
            if (len(modelList)) == 0:
                continue
            for item in modelList:
                str = item.replace("  ", "").replace("\n", "").replace("\t", "")
                compatibleModels = compatibleModels + str + "\n"
        return 1, [productTitle, description, compatibleModels, url]


