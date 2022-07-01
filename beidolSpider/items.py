# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# div class='jobsearch-SerpJobCard ...' 部分一致。ページに15個ほど。
# 下記すべての項目が取れるわけではない

class IndeedRankingItem(scrapy.Item):
    # define the fields for your item here like:
    
    # 検索結果ページにだいたいある項目
    today = scrapy.Field()        # 検索日
    ranking = scrapy.Field()      # ページ表示順位
    condition = scrapy.Field()    # 検索条件
    uid = scrapy.Field()          # uid
    url = scrapy.Field()          # 求人詳細ページに飛ぶurl
    jobTitle = scrapy.Field()     # 職名。職種ではない
    location = scrapy.Field()     # 場所
    company = scrapy.Field()      # 会社
    tags = scrapy.Field()         # タグのリスト
    salaryText = scrapy.Field()   # 給与
    jobTypeLabelsWrapper = scrapy.Field() # 就業形態。パートとか正社員とか
    jobCardShelf = scrapy.Field() # indeed側のメリットマーク的なやつ。簡単応募とか
    date = scrapy.Field()         # 掲載日
    summary = scrapy.Field()      # 求人概要
    title = scrapy.Field()
    
    # 珍しい項目
    cmiJobCategory_item = scrapy.Field()  # カードのトップに載る職種
    ratingsDisplay = scrapy.Field()       # 求人会社に対するレーティング
    
    # bool でいいかもしれない項目
    moreloc = scrapy.Field()      # その他勤務地、url。
    new = scrapy.Field()          # 新着フラグ 
    sponsoredGray = scrapy.Field()        # スポンサーフラグ
    
    # 遷移先の求人情報ページにおいて
    jobDescriptionText = scrapy.Field()   # 原稿本文。htmlタグのパターンが多い。
    
    # バイトルテレアポ用
    # company
    # company url
    tel = scrapy.Field()
    company1 = scrapy.Field()
    company2 = scrapy.Field()    
    category1 = scrapy.Field()
    category2 = scrapy.Field()
    salaryNmHour = scrapy.Field()
    salaryNmMonth = scrapy.Field()
    workingTime = scrapy.Field()

    
    
    # kaidenheiden用
    category = scrapy.Field()
    postDate = scrapy.Field()
    
class townworkItem(scrapy.Item):
    
    title = scrapy.Field()
    detailed_syokusyu = scrapy.Field()
    detailed_taisyo = scrapy.Field()
    detailed_taigu = scrapy.Field()
    detailed_hatarakikata = scrapy.Field()
    company = scrapy.Field()
    condition = scrapy.Field()
    today = scrapy.Field()
    url = scrapy.Field()
    jobTags = scrapy.Field()