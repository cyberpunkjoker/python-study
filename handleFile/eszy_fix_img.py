from pydoc import cli
from PIL import Image, ImageEnhance, ImageFilter
import os
import re
import time

base_path = 'python/handleFile/'

class HandelImage:
  '''
  用来处理图片的基本方法
  '''
  img = None
  url = ''
  new_img_url = ''
  base_tag = f'{base_path}editedImg'
  rot_path = ''

  def __init__(self, url):
    self.img = Image.open(url)
    self.url = url
    self.rot_path = self.__get_current_path()+ '/' + self.base_tag
    print(self.rot_path)
    # 先创建一个 放图片的 根目录
    if not os.path.exists(self.rot_path):
      os.makedirs(self.base_tag) 

  # 获取当前文件路径（绝对路径）
  def __get_current_path(self):
    return os.getcwd()

  # 判断是否有文件并创建文件夹
  def __make_dir(self, path):
    pull_path = self.rot_path + '/' + path  # 获取存储图片的路径
    if not os.path.exists(pull_path):
      os.makedirs(self.base_tag + '/' + path)

  # 获取图片名及后缀 -- 加入时间戳避免重复
  def __get_img_name(self):
    img_name = re.findall('[^/]+$', self.url)[0]
    arr = img_name.split('.')
    return arr[0] + str(int(time.time())) + '.' + arr[1]

  # 拷贝文件
  def __copy_sample(self):
    return self.img.copy()
  
  # 将操作后文件保存，并打印修改后信息
  def __to_save(self, sec_path, new_img, is_save = True):
    self.__make_dir(sec_path)
    # 存放路径
    save_path = f'{self.base_tag}/{sec_path}/{self.__get_img_name()}'
    
    if is_save:
      new_img.save(save_path)  #存储
    else:
      return save_path
    
    self.new_img_url = save_path   #存储图片地址
    new_img_info = self.get_img_info(new_img)
    print('缩略后的图片信息', new_img_info)

  # 获取图片基本信息：
    # 宽，高，大小，类型，位深
  def get_img_info(self, new_img = None):
    img_info = new_img if new_img else self.img
    img_url = self.new_img_url if new_img else self.url

    w = img_info.width
    h = img_info.height
    bitdepth = img_info.mode
    return {
      'w': w,
      'h': h,
      'size': os.stat(img_url).st_size,  
      'type': img_info.format,
      'bitdepth': bitdepth
    }

  # 展示图片
  def show_img(self):
    self.img.show()

  # 旋转图片
  def to_rotate_img(self, angle):
    self.img.rotate(angle).show()  #旋转

  # 生成缩略图
  def set_thumbnail(self, size):
    thumbnail_img = self.__copy_sample()
    thumbnail_img.thumbnail(size)  #缩放
    self.__to_save('thumbnail', thumbnail_img)

  # 生成剪裁图片
  def set_clip_img(self, sizeList):
    clip_img = self.img.crop(sizeList)  #剪裁
    self.__to_save('clip', clip_img)

  # 图片亮度调整
  def set_brightness(self, num):
    bright_img = ImageEnhance.Brightness(self.img).enhance(num)
    self.__to_save('bright', bright_img)

  # 粘贴图片
  def to_paste(self, url, paste_size, paste_position):
    paste_img = Image.open(url).resize(paste_size)
    orig_img_copy = self.__copy_sample()

    orig_img_copy.paste(paste_img, paste_position)
    self.__to_save('paste', orig_img_copy)

  # 滤镜效果
  def set_filter(self):
    filter_img = self.__copy_sample()
    save_path = self.__to_save('filter', filter_img, False)
    print(save_path)

    filter_img.filter(ImageFilter.CONTOUR).save(save_path)
    

handle_image = HandelImage('python/asset/img/dlam.jpeg')
handle_image.set_filter()
# handle_image.to_paste('./defaultAvatar.png', (100,100), (300,300))



####---------------------读取二进制文件---------------------####
# f = open('./dlam.jpeg', 'rb')
# print(f)