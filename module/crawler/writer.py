import pandas as pd
class Writer(object):
    def __init__(self,article_category, date):
        # 데이터 수집일자도 추가해야함.
        self.date = date
        self.header = ["date", 'category', "title", "company", "contents", "articles_url","img_url"]
        self.category = article_category
        self.df = None

    def make_dataframe(self, time, category, text_headline,
                       text_company, text_sentence, content_url, img_content):

        self.df = pd.DataFrame({"date": time,
                  'category': category,
                  "title": text_headline,
                  "company": text_company,
                  "contents":  text_sentence,
                  "articles_url": content_url,
                  "img_url":  img_content
                  })

        return self.df

