import time
import leveldb
from urllib.parse import quote_plus
import re
import json
import itertools
import sys
import requests
from queue import Queue
from threading import Thread
URL_BASE = 'http://s.m.taobao.com/search?q={}&n=200&m=api4h5&style=list&page={}'
def url_get(url):
  # print('GET ' + url)
  header = dict()
  header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
  header['Accept-Encoding'] = 'gzip,deflate,sdch'
  header['Accept-Language'] = 'en-US,en;q=0.8'
  header['Connection'] = 'keep-alive'
  header['DNT'] = '1'
  #header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
  header['User-Agent'] = 'Mozilla/12.0 (compatible; MSIE 8.0; Windows NT)'
  return requests.get(url, timeout = 5, headers = header).text
def item_thread(cate_queue, db_cate, db_item):
  while True:
    try:
      cate = cate_queue.get()
      post_exist = True
      try:
        state = db_cate.Get(cate.encode('utf-8'))
        if state != b'OK': post_exist = False
      except:
        post_exist = False
      if post_exist == True:
        print('cate-{}: {} already exists ... Ignore'.format(cate, title))
        continue
      db_cate.Put(cate.encode('utf-8'), b'crawling')
      for item_page in itertools.count(1):
        url = URL_BASE.format(quote_plus(cate), item_page)
        for tr in range(5):
          try:
            items_obj = json.loads(url_get(url))
            break
          except KeyboardInterrupt:
            quit()
          except Exception as e:
            if tr == 4: raise e
        if len(items_obj['listItem']) == 0: break
        for item in items_obj['listItem']:
          item_obj = dict(
            _id = int(item['itemNumId']),
            name = item['name'],
            price = float(item['price']),
            query = cate,
            category = int(item['category']) if item['category'] != '' else 0,
            nick = item['nick'],
            area = item['area'])
          db_item.Put(str(item_obj['_id']).encode('utf-8'),
                json.dumps(item_obj, ensure_ascii = False).encode('utf-8'))
        print('Get {} items from {}: {}'.format(len(items_obj['listItem']), cate, item_page))
        if 'nav' in items_obj:
          for na in items_obj['nav']['navCatList']:
            try:
              db_cate.Get(na['name'].encode('utf-8'))
            except:
              db_cate.Put(na['name'].encode('utf-8'), b'waiting')
      db_cate.Put(cate.encode('utf-8'), b'OK')
      print(cate, 'OK')
    except KeyboardInterrupt:
      break
    except Exception as e:
      print('An {} exception occured'.format(e))
def cate_thread(cate_queue, db_cate):
  while True:
    try:
      for key, value in db_cate.RangeIter():
        if value != b'OK':
          print('CateThread: put {} into queue'.format(key.decode('utf-8')))
          cate_queue.put(key.decode('utf-8'))
      time.sleep(10)
    except KeyboardInterrupt:
      break
    except Exception as e:
      print('CateThread: {}'.format(e))
if __name__ == '__main__':
  db_cate = leveldb.LevelDB('./taobao-cate')
  db_item = leveldb.LevelDB('./taobao-item')
  orig_cate = '正装'
  try:
    db_cate.Get(orig_cate.encode('utf-8'))
  except:
    db_cate.Put(orig_cate.encode('utf-8'), b'waiting')
  cate_queue = Queue(maxsize = 1000)
  cate_th = Thread(target = cate_thread, args = (cate_queue, db_cate))
  cate_th.start()
  item_th = [Thread(target = item_thread, args = (cate_queue, db_cate, db_item)) for _ in range(5)]
  for item_t in item_th:
    item_t.start()
  cate_th.join()