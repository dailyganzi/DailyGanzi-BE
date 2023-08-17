from konlpy.tag import Okt
from konlpy.tag import Kkma
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np

# 참고
# 키워드 추출 요약 알고리즘 (TextRank) : https://lovit.github.io/nlp/2019/04/30/textrank/

class SentenceTokenizer(object):
    def __init__(self, path):
        self.path = path
        self.kkma = Kkma()
        self.okt = Okt()
        # 불용어 사전 파일을 읽어와서 불용어 사전 구성
        with open(f'{self.path}/module/extractor/stopword.txt', 'r', encoding='utf-8') as f:
            self.stopwords = set(f.read().splitlines())

    # 문장 토큰화
    def sentences(self, text):
        sentences = self.kkma.sentences(text)
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                if idx > 0:
                    sentences[idx - 1] += (' ' + sentences[idx])
                sentences[idx] = ''
        return sentences

    # 명사 단어 추출
    def get_nouns(self, sentences):
        nouns = []
        for sentence in sentences:
            if sentence != '':
                nouns.append(' '.join([noun for noun in self.okt.nouns(str(sentence))
                                       if noun not in self.stopwords and len(noun) > 1]))
        return nouns

class GraphMatrix(object):
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []

    def build_sent_graph(self, sentence):
        try:
            tfidf_mat = self.tfidf.fit_transform(sentence)
            if tfidf_mat.shape[1] == 0:
                return None
            self.graph_sentence = np.dot(tfidf_mat.toarray(), tfidf_mat.toarray().T)
            return self.graph_sentence
        except ValueError:
            return None

    def build_words_graph(self, sentence):
        try:
            cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
            if cnt_vec_mat.shape[1] == 0:
                return None, None
            vocab = self.cnt_vec.vocabulary_
            return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word]: word for word in vocab}
        except ValueError:
            return None, None

class Rank(object):
    def get_ranks(self, graph, d=0.85):
        try:
            A = graph
            matrix_size = A.shape[0]
            for id in range(matrix_size):
                A[id, id] = 0
                link_sum = np.sum(A[:, id])
                if link_sum != 0:
                    A[:, id] /= link_sum
                A[:, id] *= -d
                A[id, id] = 1

            B = (1 - d) * np.ones((matrix_size, 1))
            ranks = np.linalg.solve(A, B)
            return {idx: r[0] for idx, r in enumerate(ranks)}

        except Exception :
            return None

class TextRank(object):
    def __init__(self, text, path):
        try:
            self.sent_tokenize = SentenceTokenizer(path)
            self.sentences = self.sent_tokenize.sentences(text)
            self.nouns = self.sent_tokenize.get_nouns(self.sentences)

            # 그래프
            self.graph_matrix = GraphMatrix()
            self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
            self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)
            self.rank = Rank()

            # 문장 중요도 파악
            self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
            if self.sent_rank_idx is not None:
                self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k],
                                                   reverse=True)
            else:
                print(text)
                self.sorted_sent_rank_idx = []

            # 키워도 중요도 파악
            self.word_rank_idx = self.rank.get_ranks(self.words_graph)
            if self.word_rank_idx is not None:
                self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k],
                                                   reverse=True)
            else:
                print(text)
                self.sorted_word_rank_idx = []

        except Exception as e:
            print(f"An error occurred in TextRank initialization: {e}")
            self.sentences = []
            self.nouns = []
            self.graph_matrix = None
            self.sent_graph = None
            self.words_graph = None
            self.idx2word = {}
            self.rank = None
            self.sent_rank_idx = {}
            self.sorted_sent_rank_idx = []
            self.word_rank_idx = {}
            self.sorted_word_rank_idx = []

    def summarize(self, sent_num=1):
        summary = []
        index = []
        for idx in self.sorted_sent_rank_idx[:sent_num]:
            index.append(idx)

        index.sort()
        for idx in index:
            cleaned_sentence = self.preprocess(self.sentences[idx])
            summary.append(cleaned_sentence)
        return summary

    def preprocess(self, text):
        reversed_text = text[::-1]  # 기사 내용을 reverse
        end_index = reversed_text.find('.다')
        if end_index != -1:
            cleaned_content = reversed_text[end_index:len(reversed_text)][::-1]
        else:
            cleaned_content = text
        return cleaned_content

    def keywords(self, word_num=10):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)

        if rank_idx is None:
            return []  # 빈 리스트 반환하거나, 다른 적절한 처리 수행

        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)

        keywords = []
        index = []
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)

        for idx in index:
            keywords.append(self.idx2word[idx])
        return keywords
