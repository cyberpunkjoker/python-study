# 处理 office 相关文件
import datetime

from openpyxl import Workbook, load_workbook

base_url = 'python/office/testResult/'  ##### --测试 office 文件存储位置--

wb = Workbook()
print(wb.sheetnames)
ws = wb.active
print(ws)

ws['A1'] = 42
ws.append([1,2,3])
ws['A2'] = datetime.datetime.now()

wb.save(f"{base_url}sample.xlsx")