#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from tkinter import *
import pyperclip

keyLen = 4
key = (114514).to_bytes(length=keyLen, byteorder='big')

# 主窗口
root = Tk()
root.geometry('400x600+300+20')

inputText = Text(root, height=16)
inputText.size

outputText = Text(root, height=16)

def handleEncrypt():
  text = inputText.get('0.0','end')
  text = str(len(text)) + text
  oldBytes = text.encode(encoding='utf-16')
  print(oldBytes)
  index = 0
  res = ''
  for i in range(len(oldBytes)):
    res = ''.join([res, chr(oldBytes[i] ^ key[index])])
    index = (index + 1) % keyLen
  outputText.delete('1.0','end')
  if (res != None):
    outputText.insert('end', res)

def handleDecrypt():
  text = inputText.get('0.0','end')
  index = 0
  newBytes = bytearray(encoding='utf-16')
  for char in text:
    newBytes.append(ord(char) ^ key[index])
    index = (index + 1) % keyLen
  print(newBytes)
  res = newBytes.decode('utf-16')
  print(res)
  strLen = re.match(r'^\d+', res)[0]
  s = int(len(strLen))
  e = int(strLen) + s
  res = res[s:e]
  outputText.delete('1.0','end')
  if (res != None):
    outputText.insert('end', res)

def handleCopy():
  text = outputText.get('0.0', 'end')
  pyperclip.copy(text)

encryptBtn = Button(root, text='加密', width=10, height=2, command=handleEncrypt)
decryptBtn = Button(root, text='解密', width=10, height=2, command=handleDecrypt)
copyBtn = Button(root, text='复制', width=10, height=2, command=handleCopy)

# 将控件放入窗口
inputText.pack()
encryptBtn.pack()
decryptBtn.pack()
copyBtn.pack()
outputText.pack()

# 进入消息循环
root.mainloop()
