# -*- coding: utf-8-*-
from asyncio import gather
from datetime import date, timedelta
from module.crawler.exceptions import *
from tqdm import tqdm
import httpx
import re
from bs4 import BeautifulSoup
from module.crawler.writer import Writer
import asyncio
import os

# 참고 :
# News summary crawler : https://github.com/Dong-Jun-Shin/News_summary_crawler/tree/main
# Crawler Source : lumyjuwon/KoreaNewsCrawler

class Preprocessor(object):
    special_symbol = re.compile('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$&▲▶◆◀■【】\\\=\(\'\"]')
    content_pattern = re.compile(
        '본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가function  flash removeCallback|tt|앵커 멘트|xa0')

    @classmethod
    def clear_content(cls, text):
        # 기사 본문에서 필요없는 특수문자 및 본문 양식 제거
        newline_symbol_removed_text = text.replace('\\n', '').replace('\\t', '').replace('\\r', '')
        special_symbol_removed_content = re.sub(cls.special_symbol, ' ', newline_symbol_removed_text)
        end_phrase_removed_content = re.sub(cls.content_pattern, '', special_symbol_removed_content)
        blank_removed_content = re.sub(' +', ' ', end_phrase_removed_content).lstrip()  # 공백 에러 삭제
        reversed_content = ''.join(reversed(blank_removed_content))  # 기사 내용을 reverse
        content = ''
        for i in range(0, len(blank_removed_content)):
            # reverse 된 기사 내용중, ".다"로 끝나는 경우 기사 내용이 끝난 것이기 때문에 기사 내용이 끝난 후의 광고, 기자 등의 정보는 다 지움
            if reversed_content[i:i + 2] == '.다':
                content = ''.join(reversed(reversed_content[i:]))
                break
        return content

    @classmethod
    def clear_headline(cls, text):
        # 기사 제목의 특수문자들을 제거
        newline_symbol_removed_text = text.replace('\\n', '').replace('\\t', '').replace('\\r', '')
        special_symbol_removed_headline = re.sub(cls.special_symbol, '', newline_symbol_removed_text)
        return special_symbol_removed_headline


class ArticleCrawler(object):
    # Naver 뉴스기사 수집
    def __init__(self):
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105}  # '오피니언': 110
        self.selected_categories = []
        self.df_list = {}
        self.date = None

    def set_category(self, *args):
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args

    @staticmethod
    async def get_url_data(url, max_tries=15):
        try:
            remaining_tries = int(max_tries)
            async with httpx.AsyncClient() as client:
                while remaining_tries > 0:
                    try:
                        response = await client.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                        response.raise_for_status()
                        return response
                    except httpx.HTTPError:
                        await asyncio.sleep(5)
                        remaining_tries -= 1
            raise ResponseTimeout()
        except ResponseTimeout:
            return None

    async def get_one_page(self, target_urls):
        # 기사 url 형식
        try:
            request = await self.get_url_data(target_urls)
            if request is None:
                return None
            document = BeautifulSoup(request.content, 'html.parser')

            # html - newsflash_body - type06_headline, type06
            # 각 페이지에 있는 기사들 가져오기
            temp_post = document.select('.newsflash_body .type06_headline li dl')
            temp_post.extend(document.select('.newsflash_body .type06 li dl'))
            # 각 페이지에 있는 기사들의 url 저장
            # 해당되는 page에서 모든 기사들의 URL을 post_urls 리스트에 넣음
            post_urls = [line.a.get('href') for line in temp_post]
            return post_urls

        except ResponseTimeout as e:
            # get_url_data에서 ResponseTimeout 예외가 발생한 경우, 해당 페이지 크롤링을 건너뜁니다.
            print(f"Skipped URL: {target_urls}, Reason: {e}")
            return None

        except Exception as e:
            # 기타 예외 발생 시 해당 페이지 크롤링을 건너뜁니다.
            print(f"Skipped URL: {target_urls}, Reason: {e}")
            return None

    async def crawling(self, category_name):

        # Multi Process PID
        print(category_name + " PID: " + str(os.getpid()))
        # 어제 기사 추출
        yesterday = (date.today()) - timedelta(days=1)
        self.date = yesterday
        # 모든 페이지 탐색
        cnt_page = 1
        # 프로그레스 바 설정
        pbar = tqdm(desc=f"Crawling {category_name}", unit="page")
        writer = Writer(article_category=category_name, date=yesterday)

        # df에 추가할 리스트 생성
        naver_news_headline = []
        naver_news_time = []
        naver_news_company = []
        naver_news_url = []
        naver_news_contents = []
        naver_news_imgurl = []

        last_urls = []
        MAIN_URL = "https://news.naver.com/main"
        while True:
            # 신문 개제 기사에 대한 것들만 수집
            url_format = f'{MAIN_URL}/list.naver?mode=LSD&sid1={self.categories.get(category_name)}&mid=sec&listType=summary&date={str(yesterday.year) + str(yesterday.month).zfill(2) + str(yesterday.day).zfill(2)}&page={cnt_page}'
            post_urls = await self.get_one_page(url_format)

            if post_urls is None or not post_urls or post_urls == last_urls:
                print("마지막 페이지 입니다.")
                break

            for content_url in post_urls:  # 기사 url
                # 크롤링 대기 시간
                await asyncio.sleep(0.5)  # await 추가하여 비동기적으로 실행

                # 기사 HTML 가져옴
                try:
                    request_content = await self.get_url_data(content_url)  # await 추가하여 비동기적으로 실행
                    if request_content is None:
                        print("링크를 불러올 수 없습니다.")
                        break
                    document_content = BeautifulSoup(request_content.content, 'html.parser')
                except ResponseTimeout as e:
                    raise e
                except Exception as e:
                    raise e

                try:
                    # 기사 제목 가져옴
                    tag_headline = document_content.find_all('h2', {'class': 'media_end_head_headline'})
                    # 스포츠 기사 대응 코드 (수정 필요)
                    if not tag_headline:
                        tag_headline = document_content.find_all('h4', {'class': 'title'})
                    if not tag_headline:
                        continue

                    # 뉴스 기사 제목 초기화
                    text_headline = ''
                    text_headline = text_headline + Preprocessor.clear_headline(
                        str(tag_headline[0].find_all(text=True)))
                    text_headline = text_headline.replace('속보', '[속보] ')
                    # 공백일 경우 기사 제외 처리
                    if not text_headline:
                        raise Exception('Not found article headline')

                    # 기사 본문 가져옴
                    tag_content = document_content.find_all('div', {'id': 'newsct_article'})
                    # 스포츠 기사 대응 코드 (수정 필요)
                    if not tag_content:
                        tag_content = document_content.find_all('div', {'id': 'newsEndContents'})
                    if not tag_content:
                        continue
                    # 뉴스 기사 본문 초기화
                    text_sentence = ''
                    text_sentence = text_sentence + Preprocessor.clear_content(str(tag_content[0].find_all(text=True)))

                    # 원문의 길이가 길 경우 앞에 10줄로 대체
                    orig_contents = text_sentence.split('. ')
                    if len(orig_contents) > 5:
                        text_sentence = '.'.join(orig_contents[:10])
                    else:
                        text_sentence = '.'.join(orig_contents)
                    # 공백일 경우 기사 제외 처리
                    # if not text_sentence:
                    #     print("Skipped Headline: " + text_headline)

                    # 본문 이미지
                    img_src = document_content.find_all('img', {'id': 'img1'})
                    img_description = document_content.find_all('em', {'class': 'img_desc'})

                    # 사진 대신 동영상일 경우, 대응 코드
                    if not img_src:
                        img_src = ['No Image']

                    img_content = str(img_src[0]).replace('class="_LAZY_LOADING" ', '').replace('data-src',
                                                                                                'src').replace('\n', '')
                    if img_description:
                        img_content = img_content + str(img_description[0])

                    # img 태그 안의 url만 추출
                    cond = re.compile('(?<=src=).+ ').search(img_content)
                    if cond:
                        img_content = cond.group().strip().replace('"', '').split()[0]

                    # 기사 언론사 가져옴
                    tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                    if not tag_company:
                        tag_company = document_content.find_all('meta', {'property': 'og:article:author'})

                    # 언론사 초기화
                    text_company = ''
                    text_company = text_company + str(tag_company[0].get('content'))
                    if text_company.find(' | 네이버') != -1:
                        text_company = text_company.replace(' | 네이버', '')

                    # 공백일 경우 기사 제외 처리
                    if not text_company:
                        raise Exception('Not found article author')

                    # 기사 시간대 가져옴
                    time = re.findall(
                        '<span class="media_end_head_info_datestamp_time _ARTICLE_MODIFY_DATE_TIME" data-modify-date-time="(.*)">(.*)</span>',
                        request_content.text)
                    if not time:
                        time = re.findall(
                            '<span class="media_end_head_info_datestamp_time _ARTICLE_DATE_TIME" data-date-time="(.*)">(.*)</span>',
                            request_content.text)

                    time = '-' if not time else time[0][1]

                    naver_news_headline.append(text_headline)
                    naver_news_time.append(time)
                    naver_news_company.append(text_company)
                    naver_news_url.append(content_url)
                    naver_news_contents.append(text_sentence)
                    naver_news_imgurl.append(img_content)

                    del time, text_company, text_sentence, text_headline, img_content
                    del tag_company, tag_content, tag_headline, request_content, document_content

                # UnicodeEncodeError
                except Exception as ex:
                    del request_content, document_content
                    raise ex

            # print(f"현재 수집 페이지 {cnt_page} \n{category_name} urls are generated \n{url_format}")
            cnt_page += 50
            last_urls = post_urls
            # 프로그레스 바 업데이트
            pbar.update(1)

        # 진행바 완료 메시지 출력
        pbar.close()
        tqdm.write("Crawling completed for category: " + category_name)

        self.df_list[category_name] = writer.make_dataframe(naver_news_time, category_name, naver_news_headline,
                                                            naver_news_company, naver_news_contents, naver_news_url,
                                                            naver_news_imgurl)

    async def start(self):
        # MultiProcess 크롤링 시작
        tasks = [self.crawling(category_name, ) for category_name in self.selected_categories]
        await gather(*tasks)
        print('+----------------Done-------------------+')

