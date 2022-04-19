import asyncio
from email.mime import base
import json
import os

import aiofile
import aiohttp


base_path = 'python/creeper/'

async def download_img(session, url, name, type):
  async with session.get(url, ssl=False) as resp:
    if resp.status == 200:
      data = await resp.read()
      async with aiofile.async_open(f'{base_path}creeperImage/{name}.{type}', 'wb') as file:
        await file.write(data)

async def fetch_img(query_word):
  async with aiohttp.ClientSession(headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
  }) as session:
    for page in range(1):
      async with session.get(
        url=f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=7801775386626368502&ipn=rj&ct=201326592&is=''&fp=result&fr=''&word={query_word}&queryWord={query_word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=''&st=-1&z=''&ic=0&hd=''&latest=''&copyright=''&s=''&se=''&tab=''&width=''&height=''&face=0&istype=2&qc=''&nc=1&expermode=''&nojc=''&isAsync=''&pn={10 + 10*(page-1)}&rn=30&gsm=3c&1649939241935=",
        ssl=False
      ) as resp:
        if resp.status == 200:
          json_str = await resp.text()
          res = json.loads(json_str)
          for item in res['data']:
            await download_img(session, item['middleURL'], item['fromPageTitleEnc'], item['type'])

def main():
  if not os.path.exists('creeperImage'):
    os.makedirs(f'{base_path}creeperImage')
  loop = asyncio.get_event_loop()
  loop.run_until_complete(fetch_img('code'))
  loop.close()

if __name__ == '__main__':
  main()
  pass