import requests
import json

url = "https://fanyi.baidu.com/v2transapi"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}

formdata = {
    "from": "zh",
    "to": "en",
    "query": "雨真大",
    "transtype": "translang",
    "simple_means_flag": "3",
    "sign": "259011.463090",
    "token": "cde9d112d87d70a1ad33b2a5649c5a6d",
}

res_text = requests.post(url=url, data=formdata, headers=headers).text
print(res_text)


