import urllib.request  
import urllib.parse  
import json 

# 百度翻译方法
def baidu_translate(content,type=1):
    '''实现百度翻译'''
    baidu_url = 'http://fanyi.baidu.com/basetrans'
    data = {}

    data['from'] = 'en'
    data['to'] = 'zh'
    data['query'] = content
    data['transtype'] = 'translang'
    data['simple_means_flag'] = '3'
    data['sign'] = '94582.365127'
    data['token'] = 'ec980ef090b173ebdff2eea5ffd9a778'
    data = urllib.parse.urlencode(data).encode('utf-8')

    headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}
    baidu_re = urllib.request.Request(baidu_url, data, headers)
    baidu_response = urllib.request.urlopen(baidu_re)
    baidu_html = baidu_response.read().decode('utf-8')
    target2 = json.loads(baidu_html)

    trans = target2['trans']
    ret = ''
    for i in range(len(trans)):
        ret += trans[i]['dst'] + '\n'

    return ret

baidu_translate("吃饭 了")