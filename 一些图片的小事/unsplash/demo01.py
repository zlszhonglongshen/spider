import requests, json, time, sys,re
from contextlib import closing
from progressbar import *

class get_photos(object):
    def __init__(self):
        self.download_server = 'https://unsplash.com/photos/xxx/download?force=trues'
        self.target = 'http://unsplash.com/napi/feeds/home'
        self.headers ={'authorization':'Client-ID 72664f05b2aee9ed032f9f4084f0ab55aafe02704f8b7f8ef9e28acbec372d09',
            'x-unsplash-client': 'web'}
            ####=======跟原博主的header不一样，需要'x-unsplash-client'，verify=False可有可无========

    def get_ids(self,nums):
        '''先进入初始url，得到下一页url跟10张图片编码，然后循环多次下一页url得到多个图片编码，
        最后返回图片编码的list——photos_id'''
        photos_id = []
        req = requests.get(url=self.target, headers=self.headers)
        html = json.loads(req.text)
        next_page = html['next_page']
        for each in html['photos']:
            photos_id.append(each['id'])
        time.sleep(1)
        for i in range(nums):
            api=re.search(r'after=(.*)',next_page).group(1)
            next_page='https://unsplash.com/napi/feeds/home?after='+api
            ##=======‘https://api.unsplash.com/feeds/home?after=bbf729c0-4204-11e8-8080-800124f51fef’
             #next_page好像是不能直接打开的，得用那个域名才可以打开取得图片ID======================
            req = requests.get(url=next_page, headers=self.headers)
            html = json.loads(req.text)
            next_page = html['next_page']
            for each in html['photos']:
                photos_id.append(each['id'])
            time.sleep(1)
        return photos_id

    def download(self, photo_id, filename):
        '''传入ID改变url，利用closing跟iter_content下载图片'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
        target = self.download_server.replace('xxx', photo_id)
        with closing(requests.get(url=target, stream=True, headers=headers)) as r:
            with open('%d.jpg' % filename, 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

    def work(self,nums):
        '''搞了个进度条'''
        #=========可以用pycharm下载ProgressBar这个模块，要不直接去掉也行===============
        ids=self.get_ids(nums)
        bar = ProgressBar(widgets=[
            '正在下载图片   '
            ' [', Timer(), '] ',
            Percentage(),
            Bar(),
            ' (', AbsoluteETA(), ') ',
        ])
        shumu=0
        for id in bar(ids):
            self.download(id,shumu)
            shumu+=1

if __name__ == '__main__':
    gp = get_photos()
    gp.work(0)