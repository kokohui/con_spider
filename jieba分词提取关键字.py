import jieba
import jieba.analyse

setence = '斜跨公文包厂家直销 公文包生产厂 公文包厂家直销 百丽威箱包'
keywords = jieba.analyse.extract_tags(setence, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns'))
print(keywords[0][0])

for item in keywords:
    print(item[0], item[1])