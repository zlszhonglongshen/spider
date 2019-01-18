# -*- coding:utf-8 -*-
from lxml import html
import requests

proxies = {
    "https": "219.138.58.13:3128",
}
for i in range(1, 135999):
    url = 'http://db.pharmcube.com/database/cfda/detail/cfda_cn_instrument/'
    url1 = url + str(i)
    print(i)
    try:
        r1 = requests.get(url1, proxies=proxies).text
        s = requests.session()
        s.keep_alive = False
        r1 = html.fromstring(r1)
    except:
        pass
    try:
        zch = r1.xpath("//tbody/tr[1]/td[2]/text()")
        yzz = r1.xpath("//tbody/tr[2]/td[2]/text()")
        yzch = r1.xpath("//tbody/tr[3]/td[2]/text()")
        zchbz = r1.xpath("//tbody/tr[4]/td[2]/text()")
        gszw = r1.xpath("//tbody/tr[5]/td[2]/text()")
        gsyw = r1.xpath("//tbody/tr[6]/td[2]/text()")
        dzzw = r1.xpath("//tbody/tr[7]/td[2]/text()")
        dzyw = r1.xpath("//tbody/tr[8]/td[2]/text()")
        cpzw = r1.xpath("//tbody/tr[9]/td[2]/text()")
        cpyw = r1.xpath("//tbody/tr[10]/td[2]/text()")
        spzw = r1.xpath("//tbody/tr[11]/td[2]/text()")
        spyw = r1.xpath("//tbody/tr[13]/td[2]/text()")
        jxzw = r1.xpath("//tbody/tr[14]/td[2]/text()")
        ggzw = r1.xpath("//tbody/tr[15]/td[2]/text()")
        bzggzw = r1.xpath("//tbody/tr[16]/td[2]/text()")
        sccszw = r1.xpath("//tbody/tr[17]/td[2]/text()")
        t1 = r1.xpath("//tbody/tr[19]/td[2]/text()")
        t2 = r1.xpath("//tbody/tr[20]/td[2]/text()")
        t3 = r1.xpath("//tbody/tr[21]/td[2]/text()")
        t4 = r1.xpath("//tbody/tr[22]/td[2]/text()")
        t5 = r1.xpath("//tbody/tr[23]/td[2]/text()")
        t6 = r1.xpath("//tbody/tr[24]/td[2]/text()")

    except:

        zch = yzz = yzch = zchbz = gszw = gsyw = dzzw = dzyw = cpzw = cpyw = spzw = spyw = jxzw = ggzw = bzggzw = sccszw = t1 = t2 = t3 = t4 = t5 = t6 = 'None'
        continue
        print('None')

    output = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},\n'.format(zch, yzz, yzch, zchbz, gszw,
                                                                                           gsyw, dzzw, dzyw, cpzw, cpyw,
                                                                                           spzw, spyw, jxzw, ggzw,
                                                                                           bzggzw, sccszw, t1, t2, t3,
                                                                                           t4, t5, t6)
    print(output)
    with open('yaojianjuqicai.csv', 'a+') as f:
        try:
            f.write(output)
        except:
            print('no')
            f.write('None')