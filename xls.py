import xlwt
import time

def newExcel(sheetName):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheetName)
    return workbook, sheet

def writeExcel(sheet, row, column, value):
    sheet.write(row, column, value)
    pass

def saveExcel(path, workbook):
    workbook.save(path)
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("[{}]一条记录已写入Excel，已成功保存！".format(t))
    pass

def initExcel(sheet):
    writeExcel(sheet, 0, 0, "序号")
    writeExcel(sheet, 0, 1, "品牌")
    writeExcel(sheet, 0, 2, "型号")
    writeExcel(sheet, 0, 3, "品牌标题")
    writeExcel(sheet, 0, 4, "描述")
    writeExcel(sheet, 0, 5, "适用机型")

def writeItem(sheet, row, brand, model, productTitle, description, compitableModel, url_now):
    writeExcel(sheet, row, 0, row)
    writeExcel(sheet, row, 1, brand)
    writeExcel(sheet, row, 2, model)
    writeExcel(sheet, row, 3, productTitle)
    writeExcel(sheet, row, 4, description)
    writeExcel(sheet, row, 5, compitableModel)
    writeExcel(sheet, row, 6, url_now)