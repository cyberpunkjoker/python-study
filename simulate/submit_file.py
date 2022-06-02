import json
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from openpyxl import Workbook, load_workbook

# 设置高度误差值，（避免图片不太正）
MISTAKE = 35

'''
利用，网页免费使用 百度 ocr
'''
class BaiduOcr:
  def __init__(self) -> None:
    self.IMAGE_PATH = f'{os.path.dirname(__file__)}/images'
    self.driver = None
    self.baidu_ocr_path = 'https://ai.baidu.com/tech/ocr_others/handwriting'
    self.img_list = []
    self.text_list = []

    # 先获取所有图片路径
    self.get_img_file()
    print(self.img_list)

  # 开启浏览器
  def setUp(self):
    opt = webdriver.ChromeOptions()
    self.driver = webdriver.Chrome(options=opt)
    self.driver.get(self.baidu_ocr_path)
   
    for path in self.img_list:
      self.to_submit(path)

  # 获取制定文件中的图片
  def get_img_file(self):
    for item in os.listdir(self.IMAGE_PATH):
      self.img_list.append(f'{self.IMAGE_PATH}/{item}')

  def to_submit(self, path):
    # 需要等待demo展示完成之后请求，不然会被替换掉
    time.sleep(2)
    self.driver.find_element(By.CLASS_NAME, 'image-local-input').send_keys(path)

    time.sleep(1)
    self.get_text_info()

  def get_text_info(self):
    # ---------------- 需等待加载动画不展示了，再获取文本 -------------------------------
    try:
      element = WebDriverWait(self.driver, 10).until_not(
        EC.visibility_of_element_located((By.CLASS_NAME, 'tech-recognition-scan'))
      )
    except:
      print("查询超时～～")
      self.driver.execute_script("alert('查询超时')")
    # -----------------------------------------------------------------------------

    img_info = json.loads(self.driver.execute_script("let str = '';document.querySelector('.demo-json-content').childNodes.forEach(i => str += (i.nodeValue || i.innerHTML));return str"))
    # 设置第一个的位置
    top_position = img_info['words_result'][0]['location']['top']
    text_info = { top_position: [] }

    for item in img_info['words_result']:
      text = item['words']
      # 换行处理
      if (item['location']['top'] - top_position >= 10):
        top_position = item['location']['top']
        text_info[top_position] = [text]
      else:
        text_info[top_position].append(text)

    self.text_list.append(text_info)
    print(self.text_list)

'''
写入 txt 的操作，因为ocr 可能有误差，建议先在txt 上修改格式
'''
class WirteTxt:
  def __init__(self, ctx_list) -> None:
    self.ctx_list = ctx_list
    self.save_path = f'{os.path.dirname(__file__)}/ocr_translate.txt'

    # self.make_dir()
  
  def make_dir(self):
    if not os.path.exists(self.save_path):
      os.makedirs(self.save_path)
  
  def wirte_txt(self):
    with open(self.save_path, 'w') as f:
      for table in self.ctx_list:
        for row in table.values():
          row_str = ''
          for col in row:
            row_str += str(col) + "---"
          f.write(row_str + '\r\n')
        f.write('\r\n')


class WirteExcel:
  def __init__(self) -> None:
    self.txt_path = f'{os.path.dirname(__file__)}/ocr_translate.txt'
    self.excel_path = f'{os.path.dirname(__file__)}/accessInfo.xlsx'
    self.excel_list = []

  def readTxt(self):
    with open(self.txt_path, encoding='utf-8') as f:
      for line in f:
        inner_arr = []
        for cel in line.split('---'):
          inner_arr.append(cel)
        inner_arr = inner_arr[0:-1]
        if len(inner_arr) > 0:
          self.excel_list.append(inner_arr)
    self.write_excel()

  def write_excel(self):
    pass



if __name__ == "__main__":
  ocr = BaiduOcr()
  ocr.setUp()

  wirte = WirteTxt(ocr.text_list)
  wirte.wirte_txt()

  excel_opt = WirteExcel()
  excel_opt.write_excel()

  