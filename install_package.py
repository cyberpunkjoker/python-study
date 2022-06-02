import re
import os
from threading import Thread

def read_text(read_path):
  with open(read_path, 'r') as file:
    data = file.readlines()
    package_list = []
    for i in data:
      pattern = re.compile('==')
      if (pattern.search(i)):
        arr = i.split('==')
        package_list.append({'name': arr[0], 'version': arr[1]})
  return package_list

def exe_cmd(*, cmd):
  os.system(cmd)

def to_checked():
  os.system('pip3 list')

def main() -> None:
  ###------------------- 获取本机已经安装的 pip 包
  os.system("pip3 freeze > installedPackage.txt")
  installed_package = read_text('installedPackage.txt')
  ###------------------- 读取项目所需要的 pip 包
  need_package = read_text('asset/txt-log/needPackage.txt')
  to_install_list = []

  for need in need_package:
    flag = False
    for installed in installed_package:
      if (need['name'] == installed['name']):
        flag = True
    if (not flag):
      to_install_list.append(need['name'])

  print(f'你需要安装的包为{to_install_list}')

  for package in to_install_list:
    Thread(target=exe_cmd, kwargs={'cmd': f'pip3 install {package}'}).start(),

  to_checked()

if __name__ == '__main__':
  main()