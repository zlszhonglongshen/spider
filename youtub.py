       #coding:utf-8
import urllib2
import urllib
import cookielib
import json
import re


class GetUrl():
    def __init__(self, youtube_url):
        self.youtube_url = youtube_url
        # self.proxy_handler = urllib2.ProxyHandler({"http" : 'http://ip:port'})
        # self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()), self.proxy_handler)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        self.values = {
            'mediaurl':youtube_url,
            'service':'YouTube',
            'ref':'',
            'lang':'en',
            'client_urlmap':'none',
            'addon_urlmap':'',
            'cookie':'',
            'addon_cookie':'',
            'addon_title':'',
            'ablock':'1',
            'clientside':'1',
            'addon_page':'none',
            'addon_browser':'',
            'addon_version':'',
            'filetype':'MP4',
            'format':'',
            'audiovol':'0',
            'audiochannel':'2',
            'audiobr':'128'
        }

    def get_choose(self):
        data = urllib.urlencode(self.values)
        url = 'http://www.clipconverter.cc/check.php'
        request = urllib2.Request(url, data)
        response = self.opener.open(request)
        self.video_info = json.loads(response.read())
        return json.dumps(self.video_info.get('url'))


    def get_statusurl(self, choose):
        self.values['url'] = self.video_info['url'][choose]['url']
        self.values['verify'] = self.video_info['verify']
        self.values['videoid'] = self.video_info['videoid']
        self.values['server'] = self.video_info['server']
        self.values['filename'] = self.video_info['filename']
        self.values['id3-artist'] = self.video_info['id3artist']
        self.values['id3-title'] = self.video_info['id3title']
        data = urllib.urlencode(self.values)
        url = 'http://www.clipconverter.cc/check.php'
        request = urllib2.Request(url, data)
        response = self.opener.open(request)
        url = 'http://www.clipconverter.cc/convert/' + json.loads(response.read())['hash'] + '/?ajax'
        response = self.opener.open(url)
        pattern = re.compile('var statusurl = "(.*?)"', re.S)
        statusurl = re.findall(pattern, response.read())[0]
        return statusurl

    def get_status(self, statusurl):
        response = self.opener.open(statusurl)

        def handle(r_str):
            json_r_str=json.loads(r_str[1:-1])
            d={}
            d['status']={}
            d['status']['step'] = json_r_str['status']['@attributes']['step']
            d['status']['percent'] = json_r_str['status']['@attributes'].get('percent', '100')
            d['downloadurl'] = json_r_str.get("downloadurl")
            return json.dumps(d)
        return handle(response.read())