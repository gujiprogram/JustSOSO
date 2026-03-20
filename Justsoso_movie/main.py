import base64
import io
import math
import re
import threading
from flask_cors import CORS
from flask import Flask, request, jsonify
import time
import urllib
from urllib.parse import quote
import logging
import random
import aiohttp
import asyncio
import requests
from PySide2.QtCore import QObject, QThread
import pymysql

# 使用flask进行api封装
app = Flask(__name__)
# 跨域
CORS(app)

data = []  # 声明全局变量 data 作为结果存储列表


@app.route('/movie', methods=['POST'])
def crawl_movie():
    search_keyword = request.get_json().get('search_keyword')
    if search_keyword:
        # print(search_keyword)
        thread = threading.Thread(target=lambda: store_result(search_keyword))
        thread.start()
        thread.join()  # 等待异步任务完成
        return jsonify(data)
    else:
        return jsonify({'success': False, 'message': 'Missing search_keyword parameter'}), 400


max_wait_time = 10

# 模拟多个UA
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.37',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61',
]

# 随机选择一个UA
selected_user_agent = random.choice(user_agents)

headers = {
    'User-Agent': selected_user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Referer': 'https://www.zhihu.com',  # 更改Referer为不同的网站
    'Cookie': 'YOUR_COOKIE_HERE',
}


class Crawl(QObject):

    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=max_wait_time) as response:
                return await response.text()

    async def Crawl_Start(self, search_keyword, crawl_thread):

        found_resource = False  # 添加一个标志，用于标记是否找到资源

        backup_urls = ['https://yunpan1.fun/', 'https://yunpan1.cc/', 'https://yunpan1.xyz/', 'https://yunpan1.com/']

        T1 = time.perf_counter()
        for base_url in backup_urls:
            # print(crawl_thread.stop_requested)
            if crawl_thread.stop_requested:
                # print("退出")
                break
            try:
                search_url = f'{base_url}?q={search_keyword}'
                # 发送异步 GET 请求获取网页内容
                response = await self.fetch(search_url)
                if "<!doctype html>" in response:
                    # print(search_url)
                    break
                else:
                    continue
                    # print("开始尝试备用地址")
            except asyncio.TimeoutError:
                # 请求超时异常处理
                # print(f"请求超时，限制时间: {max_wait_time}秒")
                # print("开始尝试备用地址")
                continue
            except Exception as e:
                continue
                # 异常处理，比如连接超时等情况
                # print(f"连接地址时出现异常: {base_url}, 错误信息: {str(e)}")

        T2 = time.perf_counter()

        # print(f'获取网页请求耗时：{T2 - T1}秒')

        # 检查响应状态码
        if "<!doctype html>" in response:
            found_resource = True
            T1 = time.perf_counter()
            # 使用正则表达式匹配href后面的网址和<h2>标签中的文本
            pattern = re.compile(r'<a href="([^"]+)"[^>]*>([^<]+)</a>')
            links = re.findall(pattern, response)
            T2 = time.perf_counter()
            # print(f'寻找详情链接耗时：{T2 - T1}秒')

            i = 0

            tasks = []
            texts = []

            for link in links:
                href = link[0]
                text = link[1].strip().replace(" ", "").replace("\n", "")

                if search_keyword not in text:
                    continue

                texts.append(text)
                tasks.append(self.fetch(href))

            for future in asyncio.as_completed(tasks):
                # print(crawl_thread.stop_requested)
                if crawl_thread.stop_requested:
                    # print("退出")
                    break

                try:
                    response_new = await asyncio.wait_for(future, timeout=max_wait_time)
                    # 正常处理已完成的任务
                    T1 = time.perf_counter()
                    pattern = re.compile(
                        r'<a href="(https://[^"]+)" rel="ugc noopener nofollow" target="_blank" rel="ugc noopener nofollow" target="_blank">')
                    matches = re.findall(pattern, response_new)
                    T2 = time.perf_counter()
                    # print(f'访问一个详情页面并获取电影链接耗时：{T2 - T1}秒')

                    # 设置进度条
                    i += 1
                    value = i / len(texts) * 100
                    # print(texts[i - 1] + " " + str(matches))
                    hyperlink = ""
                    for url in matches:
                        # print(url)
                        if "quark" in url:
                            icon_path = "YOUR_ICON_PATH/kuake.png"
                        elif "aliyundrive" in url:
                            icon_path = "YOUR_ICON_PATH/ali.jpg"
                        elif "baidu" in url:
                            icon_path = "YOUR_ICON_PATH/baidu.png"
                        else:
                            icon_path = "YOUR_ICON_PATH/wangpan.png"

                        hyperlink += f'<br><div><img src="{icon_path}" alt="Icon"> <a href="{url}" target="_blank">{url}</a></div>'

                    # print(hyperlink)

                except asyncio.TimeoutError:
                    continue
                    # print("任务超时，放弃处理该任务")

    def crawl_movie_links(self, search_keyword, crawl_thread):
        # 创建一个事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # 运行异步任务
            loop.run_until_complete(self.Crawl_Start(search_keyword, crawl_thread))
        finally:
            # 取消设置事件循环
            asyncio.set_event_loop(None)


class Crawl_kkszn(QObject):

    def Crawl_Start(self, search_keyword):

        # 模拟多个UA
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.37',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61',
        ]

        # 随机选择一个UA
        selected_user_agent = random.choice(user_agents)
        # print(selected_user_agent)
        headers = {
            "User-Agent": selected_user_agent,
            "Origin": "http://kkszn.com",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Cookie": "YOUR_COOKIE_HERE"
        }

        self.movie_kkszn = []
        ################################################################################################################
        # 桔子搜索url
        try:
            url_juzi = 'http://kkszn.com/v/api/getJuzi'
            params = {
                'name': search_keyword,
                'token': 'YOUR_TOKEN_HERE'
            }

            response_juzi = requests.post(url_juzi, params=params, headers=headers)
            response_juzi.raise_for_status()  # 检查请求是否成功

            data_juzi = response_juzi.json()
            list_items = data_juzi.get('list', [])

            for item in list_items:
                title = item['question'].replace('\n', '')
                pattern_url = r"链接(?:：|:)(.*?)$"

                url = re.search(pattern_url, item['answer'])
                movie_info = {
                    'name': title,
                    'url': url.group(1) if url else None,
                    'size': '未知',
                }
                self.movie_kkszn.append(movie_info)

        except requests.exceptions.RequestException as e:
            # 在这里处理异常情况，例如记录日志或者跳过处理
            # print("桔子搜索错误:", e)
            # 这里可以选择跳过后续处理或者采取其他措施
            pass

        #################################################################################################################
        # Dyfx搜索url
        url_dyfx = 'http://kkszn.com/v/api/getDyfx'
        params = {
            'name': search_keyword,
            'token': 'YOUR_TOKEN_HERE'
        }

        try:
            response_dyfx = requests.post(url_dyfx, params=params, headers=headers)
            response_dyfx.raise_for_status()  # 检查请求是否成功

            data_dyfx = response_dyfx.json()
            list_items = data_dyfx.get('list', [])

            for item in list_items:
                title = item['question'].replace('\n', '')
                url = item['answer'].replace('链接：', '')

                movie_info = {
                    'name': title,
                    'url': url,
                    'size': '未知',
                }
                self.movie_kkszn.append(movie_info)

        except requests.exceptions.RequestException as e:
            # 在这里处理异常情况，例如记录日志或者跳过处理
            # print("Dyfx搜索错误:", e)
            # 这里可以选择跳过后续处理或者采取其他措施
            pass

        # Web搜索url
        url_web = 'http://kkszn.com/v/api/sortWeb'
        params = {
            'name': search_keyword,
            'token': 'YOUR_TOKEN_HERE',
            'tabN': 'movie_test',
            'topNo': 10,
            'whr': 'question like "%{}%"'.format(search_keyword),
            'orderBy': 'isTop DESC, date_time',
            'orderType': 'DESC',
            'keys': 'question,answer,isTop,id'
        }

        try:
            response_web = requests.post(url_web, params=params, headers=headers)
            response_web.raise_for_status()  # 检查请求是否成功

            data_web = response_web.json()
            list_items = data_web.get('list', [])

            for item in list_items:
                title = item['question'].replace('\n', '')
                pattern_url = r"链接：(.*?)$"

                url = re.search(pattern_url, item['answer'])

                movie_info = {
                    'name': title,
                    'url': url.group(1) if url else None,
                    'size': '未知',
                }
                self.movie_kkszn.append(movie_info)

        except requests.exceptions.RequestException as e:
            # 在这里处理异常情况，例如记录日志或者跳过处理
            # print("Web搜索错误:", e)
            # 这里可以选择跳过后续处理或者采取其他措施
            pass


class Crawl_pansearch(QObject):

    async def fetch_data(self, url, params, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                return await response.json()

    async def deal_task(self, task_list):
        done, pending = await asyncio.wait(task_list, timeout=None)
        return done

    async def Crawl_Start(self, search_keyword):

        url_encoded_keyword = quote(search_keyword)

        url = "https://www.pansearch.me/_next/data/szGA5qnP2NW2Divz6Rdfa/search.json?"

        # 模拟多个UA
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.37',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61',
        ]

        # 随机选择一个UA
        selected_user_agent = random.choice(user_agents)
        # print(selected_user_agent)
        headers = {
            "User-Agent": selected_user_agent,
            "Referer": "https://www.pansearch.me/search?keyword=" + url_encoded_keyword,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cookie": "YOUR_COOKIE_HERE",
        }

        self.movie_pansearch = []
        all_data = []

        params = {
            "keyword": search_keyword,
            "offset": 0
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # 检查请求是否成功

            data = response.json()
            total = data['pageProps']['data']['total']

            if total == 0:
                # print("未找到资源！")
                return

            total = math.ceil(total / 10)

            task_list = []
            for i in range(total):
                params = {
                    "keyword": search_keyword,
                    "offset": 10 * i
                }
                task = asyncio.create_task(self.fetch_data(url, params, headers))
                task_list.append(task)

            done = await self.deal_task(task_list)

            # 处理所有完成的任务的结果
            for task in done:
                data = task.result()
                items = data['pageProps']['data']['data']
                all_data.extend(items)

            # 匹配名称和url
            for item in all_data:
                if "大小：" in item["content"]:
                    pattern_movie = r"(?:名称|标题)：(.*?)\n"
                    movie = re.search(pattern_movie, item["content"])
                    if movie:
                        # 去除匹配结果中的标签
                        cleaned_movie = [re.sub(r"<.*?>", "", movie.group(1))]
                    else:
                        cleaned_movie = [""]
                    pattern_url = r"<a class=\"resource-link\" target=\"_blank\" href=\"(.*?)\">"
                    url = re.search(pattern_url, item["content"])
                    pattern_GB = r"大小：(.*?)\n"
                    GB = re.search(pattern_GB, item["content"])
                    if cleaned_movie and cleaned_movie[0] != "" and url and url.group(1) != "" and GB and GB.group(
                            1) != "":
                        if search_keyword in cleaned_movie[0]:
                            # 创建一个字典，保存电影信息
                            movie_info = {
                                'name': cleaned_movie,
                                'url': url.group(1),
                                'size': GB.group(1)
                            }
                            # 将电影信息字典添加到列表中
                            self.movie_pansearch.append(movie_info)

        except requests.exceptions.RequestException as e:
            # 在这里处理异常情况，例如记录日志或者跳过处理
            # print("pansearch错误:", e)
            # 这里可以选择跳过后续处理或者采取其他措施
            pass


# 获取电影信息，名字，演员，年份，豆瓣评分，海报
class MovieInfo():

    def __init__(self, keyword, show_detail_error=False):

        self._UserAgents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0",
            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"
        ]
        self.keyword = keyword
        self.show_detail_error = show_detail_error
        self.url = "https://movie.douban.com/subject/" + str(self.find_ID())

        self.check_url()

        self.get_title()
        self.get_context()
        self.get_describe()
        self.get_bgimg_content()
        self.get_rate_star()
        self.get_rate_detail()

    def check_url(self):
        if not self.show_detail_error:
            # 增加 UserAgent
            headers = {"user-agent": random.choice(self._UserAgents)}

            try:
                r = requests.get(self.url, headers=headers)
                self._text = r.text
            except Exception as e:
                # print("豆瓣url访问失败:", e)
                self.show_detail_error = True

    def get_title(self):

        if not self.show_detail_error:
            self.alias_name = ''
            try:

                info_pattern = re.compile(r'<div id="info">(.*?)</div>', re.S)
                movie_info = re.search(info_pattern, self._text).group(0)
                self.alias_name = re.findall(r"<span class=\"pl\">又名:</span> (.*?)<br/>", movie_info)

            except BaseException:
                logging.warning('标题获取失败 默认为空')

    def get_context(self):
        if not self.show_detail_error:
            self.context = ''
            try:
                self.context = re.findall(r"<meta property=\"og:description\" content=\"(.*?)\" />", self._text,
                                          re.DOTALL)

            except BaseException:
                logging.warning('内容描述获取失败 默认为空')

    def get_describe(self):

        if not self.show_detail_error:
            self.describe = ''

            try:
                info_pattern = re.compile(r'<div id="info">(.*?)</div>', re.S)

                movie_info = re.search(info_pattern, self._text).group(0)
                movie_time = re.search(r"片长:</span>.*?<span .*?>(.*?)</span>",
                                       movie_info,
                                       re.S).group(1)

                movie_type = re.findall(r"<span property=\"v:genre\">(.*?)</span>", movie_info)

                directors = re.findall(r"<a href=.*? rel=\"v:directedBy\">(.*?)</a>", movie_info, re.S)

                actors = re.findall(r"<a href=.*? rel=\"v:starring\">(.*?)</a>", movie_info, re.S)

                releasedate = re.findall(r"<span property=\"v:initialReleaseDate\" content=.*?>(.*?)</span>",
                                         movie_info,
                                         re.S)

                self.describe = ' / '.join([movie_time,
                                            ' / '.join(movie_type),
                                            ' / '.join(['%s(导演)' % director for director in directors]),
                                            ' / '.join(actors[:5]),
                                            ' / '.join(releasedate)])
            except BaseException:
                logging.warning('概述获取失败 默认为空')

    def get_bgimg_content(self):

        if not self.show_detail_error:
            self.bgimg_content = ''
            try:
                bgimg_url = re.search(r"<a class=\"nbgnbg\".*?<img src=\"(.*?)\" title=\"点击看更多海报\".*?</a>",
                                      self._text,
                                      re.S).group(1)

                self.bgimg_content = bgimg_url

            except BaseException:
                logging.warning('背景图获取失败 默认为空')

    def get_rate_star(self):
        if not self.show_detail_error:
            self.rate = ''
            self.star_rate = 00
            self.rating_people = ''

            try:
                rate_star_pattern = re.compile(
                    r"<div class=\"rating_self clearfix\" typeof=\"v:Rating\">(.*?)<div class=\"ratings-on-weight\">",
                    re.S)
                rate_star_content = re.search(rate_star_pattern, self._text).group(1)
                self.rate = re.findall(r"property=\"v:average\">(.*?)</strong>", rate_star_content, re.S)[0]

                self.star_rate = re.findall(r"<div class=\"ll bigstar bigstar(\d+)\"></div>", rate_star_content)[0]
                self.rating_people = re.findall(r"<span property=\"v:votes\">(\d+)</span>人评价", rate_star_content)[0]
            except BaseException:
                logging.warning('评分获取失败 默认为空')

    def get_rate_detail(self):

        if not self.show_detail_error:
            self.star_rate_details = []
            self.betterthan = []

            try:
                rate_detail_pattern = re.compile(
                    r"<div class=\"ratings-on-weight\">(.*?)<div id=\"interest_sect_level\"",
                    re.S)

                rate_detail_content = re.search(rate_detail_pattern, self._text).group(1)

                self.star_rate_details = re.findall(r"<span class=\"rating_per\">(.*?)%</span>", rate_detail_content)

                self.betterthan = re.findall(r"<a href=\"/typerank?.*?\">(.*?)</a><br/>", rate_detail_content)
                if self.betterthan:
                    self.betterthan = ["好于 %s" % i for i in self.betterthan]
            except BaseException:
                logging.warning('评分详情获取失败 默认为空')

    # 根据电影名称找到对应的豆瓣ID
    def find_ID(self):
        douban_id = None  # 设置默认值为None

        try:
            url1 = 'https://movie.douban.com/j/subject_suggest?q='
            url2 = urllib.parse.quote(self.keyword)  # 对关键词进行URL编码
            url = url1 + url2  # 拼接URL

            # print(url)
            # 增加 UserAgent
            headers = {"user-agent": random.choice(self._UserAgents)}

            response = requests.get(url, headers=headers)
            html_content = response.text  # 获取HTML内容

            # 使用正则表达式提取第一个电影的 ID
            id_pattern = re.compile(r'"id":"(\d+)"')
            id_match = id_pattern.search(html_content)
            if id_match:
                douban_id = id_match.group(1)

        except Exception as e:
            # print('豆瓣ID查找失败:', e)
            self.show_detail_error = True
        if douban_id is None:
            # print('豆瓣ID为空')
            self.show_detail_error = True

        return douban_id  # 返回douban_id


def store_result(search_keyword):
    global data  # 声明 data 为全局变量
    result = StartCrawl(search_keyword)  # 尝试进行爬取
    data = result  # 如果成功，更新全局变量 data


# 在其他地方调用 store_result 函数并处理返回的 data

def StartCrawl(search_keyword):
    # 查看插入数据库是否成功
    flag = False
    # 获取电影豆瓣信息
    movie_base = MovieInfo(search_keyword)
    if movie_base.show_detail_error:
        # print("未找到豆瓣资源！")
        return {'success': flag, 'message': "没有找到豆瓣资源"}

    # crawl_object = Crawl()
    crawl_object2 = Crawl_pansearch()
    crawl_object3 = Crawl_kkszn()
    # crawl_object.Crawl_Start(search_keyword)

    # 创建事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(crawl_object2.Crawl_Start(search_keyword))
    # 关闭事件循环
    loop.close()

    crawl_object3.Crawl_Start(search_keyword)

    # 初始化一个集合，用于记录已经添加过的链接
    added_links = set()
    # print(crawl_object2.movie_pansearch)

    if not crawl_object2.movie_pansearch and not crawl_object3.movie_kkszn:
        # print("未找到相关资源！")
        return {'success': flag, 'message': "没有找到该资源"}

    else:
        # 发送请求获取图片数据
        response = requests.get(movie_base.bgimg_content)

        # 检查请求是否成功
        if response.status_code == 200:
            # 将图片的二进制数据转换为 BytesIO 对象
            image_data = io.BytesIO(response.content)

            # 将字节串转换为Base64编码的字符串
            poster_base64 = base64.b64encode(response.content).decode('utf-8')

            url = 'http://YOUR_SERVER_HOST:8000/poster/'
            files = {'poster': (search_keyword + '.jpg', image_data, 'image/jpeg')}
            data = {'search_keyword': search_keyword}

            response = requests.post(url, files=files, data=data)
            data = response.json()
            if data['success']:
                print('Image uploaded successfully')
            else:
                print('Failed to upload image:', data['errors'])
        else:
            print(f"下载图片失败，状态码：{response.status_code}")

    # 打开数据库连接
    try:
        db = pymysql.connect(
            host='YOUR_DB_HOST',
            user='YOUR_DB_USER',
            passwd='YOUR_DB_PASSWORD',
            port=3306,
            db='YOUR_DB_NAME'
        )
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # print('连接成功！')
    except pymysql.Error as e:
        print(f"连接数据库错误: {e}")

    movie_all_info = crawl_object2.movie_pansearch + crawl_object3.movie_kkszn

    # 遍历每个电影信息，创建 JSON 对象并存储在列表中
    # movie_json_list = []

    for movie_info in movie_all_info:
        resource_name = movie_info['name'][0]
        # 确保资源名称中存在搜索关键词
        if search_keyword not in resource_name:
            resource_name = search_keyword + resource_name
        # 检查是否已经存在相同的链接
        if movie_info['url'] not in added_links:
            # 判断 network 字段的值
            if 'ali' in movie_info['url']:
                network = '阿里'
            elif 'baidu' in movie_info['url']:
                network = '百度'
            elif 'quark' in movie_info['url']:
                network = '夸克'
            elif 'xunlei' in movie_info['url']:
                network = '迅雷'
            else:
                network = None

            # SQL 插入语句
            sql = """INSERT INTO movies_movie (search_keyword, name, alias, description, detail, rate, link, size, access, network)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            if network != None:

                # # 创建电影 JSON 对象
                # movie_json = {
                #     'search_keyword': search_keyword,
                #     'name': movie_info['name'],
                #     'alias': movie_base.alias_name,
                #     'description': movie_base.context,
                #     'detail': movie_base.describe,
                #     'rate': movie_base.rate,
                #     'url': movie_info['url'],
                #     'size': movie_info['size'],
                #     'access': True,
                #     'network': network,
                # }
                # movie_json_list.append(movie_json)

                try:
                    # 执行 SQL 插入语句
                    cursor.execute(sql, (search_keyword, movie_info['name'], movie_base.alias_name, movie_base.context,
                                         movie_base.describe, movie_base.rate, movie_info['url'],
                                         movie_info['size'], True, network))
                    # 提交到数据库执行
                    db.commit()
                    # print('数据插入成功！')
                    flag = True
                except pymysql.Error as e:
                    # 如果发生错误则回滚
                    db.rollback()
                    # print(f'数据插入错误: {e}')
            # 将链接添加到已添加链接集合中
            added_links.add(movie_info['url'])

    # 关闭游标和数据库连接
    cursor.close()
    db.close()

    # 返回json数据
    return {'success': flag}


if __name__ == '__main__':
    # search_keyword = input("请输入需要搜索的电影名字：\n")
    app.run(host='0.0.0.0')

    # movie_base = MovieInfo(search_keyword)
    # # # print(movieinfo.title_name)
    # # # print(movieinfo.alias_name)
    # ## print(movie_base.context)
    # # # print(movieinfo.describe)
    # # # print(movieinfo.bgimg_content)
    # # # print(movieinfo.rate)
    # # # print(movieinfo.rating_people)
    #
    # # crawl_object1 = Crawl()
    # crawl_object2 = Crawl_pansearch()
    # crawl_object3 = Crawl_kkszn()
    #
    # crawl_object3.Crawl_Start(search_keyword)
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(crawl_object2.Crawl_Start(search_keyword))
    #
    # # 初始化一个集合，用于记录已经添加过的链接
    # added_links = set()
    #
    # # 发送请求获取图片数据
    # response = requests.get(movie_base.bgimg_content)
    #
    # # 检查请求是否成功
    # if response.status_code == 200:
    #     # 将图片的二进制数据写入文件
    #     with open(search_keyword + '.jpg', 'wb') as f:
    #         f.write(response.content)
    #
    #     url = 'http://127.0.0.1:8000/poster/'
    #     files = {'poster': open(search_keyword + '.jpg', 'rb')}
    #     data = {
    #         'search_keyword': search_keyword,
    #     }
    #
    #     response = requests.post(url, files=files, data=data)
    #     data = response.json()
    #     if data['success']:
    #         # print('Image uploaded successfully')
    #     else:
    #         # print('Failed to upload image:', data['errors'])
    # else:
    #     # print(f"下载图片失败，状态码：{response.status_code}")
    #
    # # 打开数据库连接
    # try:
    #     db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='justsoso')
    #     # 使用 cursor() 方法创建一个游标对象 cursor
    #     cursor = db.cursor()
    #     # print('连接成功！')
    # except pymysql.Error as e:
    #     # print(f"连接数据库错误: {e}")
    #
    # movie_all_info = crawl_object2.movie_pansearch + crawl_object3.movie_kkszn
    #
    # # 遍历每个电影信息
    # for movie_info in movie_all_info:
    #     resource_name = movie_info['name'][0]
    #     # 确保资源名称中存在搜索关键词
    #     if search_keyword not in resource_name:
    #         resource_name = search_keyword + resource_name
    #     # 检查是否已经存在相同的链接
    #     if movie_info['url'] not in added_links:
    #         # 判断 network 字段的值
    #         if 'ali' in movie_info['url']:
    #             network = '阿里'
    #         elif 'baidu' in movie_info['url']:
    #             network = '百度'
    #         elif 'quark' in movie_info['url']:
    #             network = '夸克'
    #         elif 'xunlei' in movie_info['url']:
    #             network = '迅雷'
    #         else:
    #             network = None
    #
    #         # SQL 插入语句
    #         sql = """INSERT INTO movies_movie (search_keyword, name, alias, description, detail, rate, link, size, access, network)
    #                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    #
    #         if network != None:
    #             try:
    #                 # 执行 SQL 插入语句
    #                 cursor.execute(sql, (search_keyword, movie_info['name'], movie_base.alias_name, movie_base.context,
    #                                      movie_base.describe, movie_base.rate, movie_info['url'],
    #                                      movie_info['size'], True, network))
    #                 # 提交到数据库执行
    #                 db.commit()
    #                 # print('数据插入成功！')
    #             except pymysql.Error as e:
    #                 # 如果发生错误则回滚
    #                 db.rollback()
    #                 # print(f'数据插入错误: {e}')
    #         # 将链接添加到已添加链接集合中
    #         added_links.add(movie_info['url'])
    #
    # # 关闭游标和数据库连接
    # cursor.close()
    # db.close()