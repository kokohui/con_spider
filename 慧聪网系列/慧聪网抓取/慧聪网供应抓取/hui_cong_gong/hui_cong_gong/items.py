import scrapy


class HuiCongGongItem(scrapy.Item):

    one_class_name = scrapy.Field()
    one_class_id = scrapy.Field()
    two_class_name = scrapy.Field()
    two_class_id = scrapy.Field()
    tree_class_name = scrapy.Field()
    tree_class_id = scrapy.Field()
