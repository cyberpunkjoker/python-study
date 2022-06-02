# 学习 selenium 简单制作一个自动滚动，翻页功能
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# --------------------- 常量 ---------------------
SCROLL_SPEED = 2
SCROLL_TIME = 0.01
SITE_INFO = { # 不同浏览器的查找方式不同，目前只支持百度搜索 
  'baidu': {
    'search_site': 'https://www.baidu.com/',
    'input_elm': 's_ipt',
    'search_btn': 's_btn',
    'wait_dom': 'container',
    'next_dom': 'n'
  }
}
SEARCH_KEY = '前端性能测试'
SELECTED_SITE = 'baidu'
WAIT_TIME = 10
# ------------------------------------------------

# ------------------- 所需网页元素解构值 -------------------
search_site = SITE_INFO[SELECTED_SITE]['search_site'] 
search_input_elm = SITE_INFO[SELECTED_SITE]['input_elm']
search_btn = SITE_INFO[SELECTED_SITE]['search_btn']
wait_dom = SITE_INFO[SELECTED_SITE]['wait_dom']
next_dom = SITE_INFO[SELECTED_SITE]['next_dom']
# -------------------------------------------------------

# open site
opt = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=opt)
driver.get(search_site)

input_elem = driver.find_element_by_class_name(search_input_elm)
input_elem.send_keys(SEARCH_KEY)
driver.find_element_by_class_name(search_btn).click()

def to_next_page(): 
  node_list = driver.find_elements_by_class_name(next_dom)
  print(node_list)

  if (len(node_list) > 1):
    node_list[1].click()
  else:
    node_list[0].click()
  toScroll()

def loop_func(func, second, maxCount):
  count = 1
  while count < maxCount:
    print(count, maxCount)
    func()
    count += 1
    time.sleep(second)
  print('滚动到底层了')
  to_next_page()
def execFn(): 
  driver.execute_script(f"document.documentElement.scrollTop += {SCROLL_SPEED}")

def toScroll():
  # ------------------------ 等待dom节点加载完成 ------------------------
  try:
    element = WebDriverWait(driver, WAIT_TIME).until(
      EC.presence_of_all_elements_located((By.ID, wait_dom))
    )
  except:
    print("查询超时～～")
    driver.quit()
  
  total_height = driver.execute_script("return document.body.scrollHeight - window.screen.height + 50")
  print('执行滚动中～～')
  print(f'高为{total_height}')
  loop_func(execFn, SCROLL_TIME, total_height / SCROLL_SPEED)

toScroll()