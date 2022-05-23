import requests
import ssl
from lxml import etree
from fake_ip import *


def get(url): # 给定url，返回响应
    # 爬虫基本参数设置
    ssl._create_default_https_context = ssl._create_unverified_context
    URL = "https://pellet-stove-parts-4less.com"
    return fakeIPGet(URL + url)

def findAllBrand(url): # 查找所有品牌
    res = get(url)
    html = etree.HTML(res.text)
    result = [html.xpath('//div[@class=" manufacturer-image-navigation"]/a/@href'),
              html.xpath('//div[@class=" manufacturer-image-navigation"]/a/@title')]
    print("started......")
    return result

def findAllModel(brand, url): # 给定品牌和url，查找所有型号
    res = get(url)
    html = etree.HTML(res.text)
    result = [html.xpath('//div[@class=" manufacturer-image-navigation"]/a/@href'),
              html.xpath('//div[@class=" manufacturer-image-navigation"]/a/@title')]
    print("正在搜索 " + brand + " 品牌下的所有产品......")
    return brand, result

def findAllProduct(model, url):
    res = get(url)
    html = etree.HTML(res.text)
    result = html.xpath('//a[@class="productitem--image-link"]/@href')
    print("正在搜索型号" + model + "......")
    return model, result

def findAllItem(url):
    res = get(url)
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
    tempRes_description = html.xpath('//div[@class="tabPanel"]//div[@id="description-content" and @role="tabpanel" and @aria-labelledby="description-content"]/span/b/text()')
    description = ""
    if len(tempRes_description) > 0:
        description = description + tempRes_description[0]
        temp_descriptionList = html.xpath('//div[@class="tabPanel"]//div[@id="description-content" and @role="tabpanel" and @aria-labelledby="description-content"]/ul[@style="margin-top: 5px;"]/li/text()')
        for i in range(len(temp_descriptionList)):
            description = description + "\n" + temp_descriptionList[i]

    # 适用机型
    compatibleModels = ""
    temp_ul = html.xpath('//div[@class="tabContainer"]/div[@class="tabPanel"]//div[@id="description-content" and @role="tabpanel" and @aria-labelledby="description-panel-content"]/div/ul')
    for ul in temp_ul:
        modelName = ul.xpath('./p[@class="ac-compat-stove-manufacturer"]/text()')
        if(len(modelName)) == 0:
            continue
        compatibleModels = compatibleModels + modelName[0] + ":\n"
        modelList = ul.xpath('./li[@class="ac-compat-stove-model"]/text()')
        if(len(modelList)) == 0:
            continue
        for item in modelList:
            str = item.replace("  ", "").replace("\n", "").replace("\t", "")
            compatibleModels = compatibleModels + str + "\n"
    return 1, [productTitle, description, compatibleModels, url]

