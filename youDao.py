import requests

url = "https://fanyi.baidu.com/v2transapi"

headers = {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}

data = {
"from": "zh",
"to": "en",
"query": "辉哥真帅",
"transtype": "enter",
"simple_means_flag": "3",
"sign": "488025.233832",
"token": "cde9d112d87d70a1ad33b2a5649c5a6d",
}

res_text = requests.post(url=url, data=data, headers=headers).text
print(res_text)


# print(response.content.decode('unicode_escape')) # 中文转码

# token: 'cde9d112d87d70a1ad33b2a5649c5a6d',
#     systime: '1565329589520',
