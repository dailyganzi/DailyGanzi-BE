import pandas as pd
import re
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from module.extractor.keywordextractor import TextRank

class NewsDuplicateProcessor:
    def __init__(self, df):
        self.df = df

    def remove_quoted_text(self, text):
        text = text.replace('“', '"').replace('”', '"')

        pattern = r"[가-힣]+\s[가-힣]+\s[가-힣]+\s[가-힣]+\s기자"
        pattern2 = r"\s사진 영상 제보 받습니다"

        text = re.sub(pattern, "", text)
        text = re.sub(pattern2, "", text)

        return re.sub(r'"[^"]+"', '', text)

    def preprocess_dataframe(self, df):
        df['contents'] = df['contents'].fillna('')
        df = df[df['img_url'] != "No Image"].drop_duplicates(['contents'], keep='last')
        df['contents'] = df['contents'].str.lower()
        df['contents'] = df['contents'].apply(self.remove_quoted_text)
        return self.df.reset_index(drop=True)

    # 중복된 기사 내용 제거
    def preprocess_and_remove_duplicates(self):
        self.df = self.preprocess_dataframe(self.df)
        tfidf_vectorizer = TfidfVectorizer(
            analyzer='word',
            min_df=2,
            max_df=0.8,  # 조정된 값
            ngram_range=(4, 6),
            max_features=6000,
            smooth_idf=True,
            sublinear_tf=True,
        )

        print("Tokenizing and calculating TF-IDF...")
        tfidf_matrix_reduced = tfidf_vectorizer.fit_transform(
            [str(val) for val in self.df['contents'] if val is not np.nan])

        print("Calculating ...")
        cosine_sim = cosine_similarity(tfidf_matrix_reduced, tfidf_matrix_reduced)

        is_duplicate = np.zeros((tfidf_matrix_reduced.shape[0], tfidf_matrix_reduced.shape[0]), dtype=bool)

        for i in tqdm(range(cosine_sim.shape[0])):
            for j in range(i + 1, cosine_sim.shape[0]):
                if cosine_sim[i][j] >= 0.7:
                    is_duplicate[i][j] = True

        unique_duplicates = sorted(set(np.where(is_duplicate)[1]))
        self.df = self.df.drop(index=unique_duplicates).reset_index(drop=True)
        print("\nDone .")
        return self.df


class NewsTextRankProcessor:
    def __init__(self, data, file_path):
        self.df = data
        self.path = file_path

    def process_document(self, content):
        try:
            textrank = TextRank(content,self.path)
            sentences = textrank.summarize()
            keywords = textrank.keywords()

            if sentences is None or keywords is None:
                return pd.Series({'sentences': [], 'keywords': []})
            return pd.Series({'sentences': sentences, 'keywords': keywords})

        except Exception as e:
            print(f"An error occurred in process_document: {e}")
            return pd.Series({'sentences': [], 'keywords': []})

    def calculate_keyword_ranking(self, df):
        try:
            df = df[df['keywords'].apply(lambda x: bool(x))]
            if df.empty:
                raise ValueError("No valid keywords found.")

            all_keywords = [keyword for keywords_list in df['keywords'] for keyword in keywords_list]
            keyword_counts = Counter(all_keywords)
            ranked_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
            return ranked_keywords

        except Exception as e:
            print(f"An error occurred in calculate_keyword_ranking: {e}")
            return []

    def category_frequency(self):
        category_keywords = {}
        for category in self.df['category'].unique():
            category_df = self.df[self.df['category'] == category]
            keyword_ranking = self.calculate_keyword_ranking(category_df)
            category_keywords[category] = keyword_ranking
        return category_keywords

    def get_most_common_keywords(self, top_n=10):
        category_keywords = self.category_frequency()
        all_keywords = [keyword for keywords_list in category_keywords.values() for keyword, _ in keywords_list]
        keyword_counts = Counter(all_keywords)
        most_common_keywords = keyword_counts.most_common(top_n)
        return most_common_keywords
    def filter_data_with_keywords(self, min_keywords=2, top_n_keywords=3):
        category_keywords = self.category_frequency()
        keyword_tree = {}
        for category, keywords in category_keywords.items():
            if len(keywords) >= min_keywords:
                selected_keywords = [keyword for keyword, _ in keywords[:top_n_keywords]]
                category_df = self.df[(self.df['category'] == category) & (
                    self.df['keywords'].apply(lambda x: any(keyword in x for keyword in selected_keywords)))]

                # 이 부분에서 최대 3개의 행만 선택하여 저장
                keyword_tree[category] = {}
                for keyword in selected_keywords:
                    keyword_df = category_df[category_df['keywords'].apply(lambda x: keyword in x)]

                    # 다른 키워드 value에 포함되지 않는지 확인
                    is_unique = True
                    for other_keyword, other_df in keyword_tree[category].items():
                        if other_keyword != keyword and not other_df.empty:
                            if keyword_df.equals(other_df):
                                is_unique = False
                                break

                    if is_unique:
                        keyword_tree[category][keyword] = keyword_df

        # print(keyword_tree)
        return keyword_tree

    # 데이터 확인용
    def print_keywords(self, num_keywords=50):
        ranked_keywords = self.calculate_keyword_ranking(self.df)
        for keyword, count in ranked_keywords[:num_keywords]:
            print(f"Keyword: {keyword}, Count: {count}")

    def start(self):
        print("Starting keyword extraction...")
        tqdm.pandas()
        self.df[['sentences', 'keywords']] = self.df['contents'].progress_apply(self.process_document)
        self.df = self.df.dropna().reset_index(drop=True)
        num_rows = self.df.shape[0]

        print(f"Number of processed rows: {num_rows}")
        print(self.df.shape)
        self.print_keywords()

