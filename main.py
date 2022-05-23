import time

from Threading import *
import threading
from xls import *

def function(brand, url, workbook, path, i, flag, bug_flag, bug_flag_out):
    sheet = workbook.add_sheet("{}".format(i))
    initExcel(sheet)
    if i == 41 or i == 48:
        return
    fc_ip = thr_ip()
    row = 1
    brand, result_model = fc_ip.findAllModel(brand, url)
    for j in range(len(result_model[0])):  # 爬取第三层(对所有型号，获得其所有产品)
        if j == 0:
            continue
        model, result_product = fc_ip.findAllProduct(result_model[1][j], result_model[0][j])
        k = 0
        while k < len(result_product): # 爬取第四层(对所有产品，获得对应数据)
            if row <= bug_flag[i]:
                row = row + 1
                bug_flag_out[i] = bug_flag[i]
                k = k + 1
                continue
            work, ans = fc_ip.findAllItem(result_product[k])
            bug_flag_out[i] = bug_flag_out[i] + 1
            if work == 1:
                writeItem(sheet, row, brand, model, ans[0], ans[1], ans[2], ans[3])
                saveExcel(path, workbook)
                print("bugflag", bug_flag_out)
                row = row + 1
            k = k + 1
    print("线程{}已结束".format(i))
    flag[i] = 1

def main():
    bug_flag = []
    # fakeIPGet.ip = getIP()
    path = "result.xls"
    workbook = xlwt.Workbook()
    # 爬取第一层(获得所有品牌)
    main_ip = thr_ip()
    result_brand = main_ip.findAllBrand("/pages/pellet-stove-parts-by-manufacturer")
    i = 0
    flag = [0] * len(result_brand[0])
    bug_flag = [0] * 49
    bug_flag_out = [0] * len(result_brand[0])

    num_working = 0
    while i < len(result_brand[0]):  # 爬取第二层(对所有品牌，获得其所有型号)
        time.sleep(1)
        thr = threading.Thread(target=function, args=(result_brand[1][i], result_brand[0][i], workbook, path, i, flag, bug_flag, bug_flag_out))
        thr.start()
        i = i + 1
        num_working = num_working + 1
        '''else:
            print("当前运行的线程数为{}，将在20秒后尝试添加".format(len(threading.enumerate())), fakeIPGet.ip)
            for index in range(len(flag)):
                if flag[index] == 1:
                    print("线程{}已完成".format(index))
                    num_working = num_working - 1
                    flag[index] = 2
            time.sleep(20)'''

    saveExcel(path, workbook)

if __name__ == '__main__':
    main()