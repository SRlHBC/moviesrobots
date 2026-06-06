import os
import requests
import csv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
from lxml import html
import re
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
    raise_on_status=False,   # 不立即抛出状态码异常
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)
TMBD_BASE_URL = 'https://www.themoviedb.org'
TMBD_TOP_URL = 'https://www.themoviedb.org/movie/top-rated'
TMBD_TOP_URL2 = 'https://www.themoviedb.org/discover/movie/items'


def extract_movie_id(url):
    """从电影详情页 URL 中提取数字 ID"""
    match = re.search(r'/movie/(\d+)', url)
    return match.group(1) if match else None
def get_movie_info(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            # 每次重试都创建一个新的 Session 或直接使用全局 session
            response = session.get(url, timeout=15)   # 使用你定义的全局 session
            response.raise_for_status()
            document = html.fromstring(response.text)

            # 标题
            title_list = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
            title = title_list[0].strip() if title_list else ''

            # 类型
            genre_list = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="genres"]/a/text()')
            genre = '/'.join(genre_list) if genre_list else ''

            # tagline
            tagline_list = document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/h3[1]/text()')
            tagline = tagline_list[0].strip() if tagline_list else ''

            # 简介
            overview_list = document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/div/p/text()')
            overview = overview_list[0].strip() if overview_list else ''

            # 上映时间
            release_date_list = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="release"]/text()')
            release_date = release_date_list[0].strip() if release_date_list else ''

            # 时长
            runtime_list = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="runtime"]/text()')
            runtime = runtime_list[0].strip() if runtime_list else ''

            # 评分
            score_class_list = document.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/div/span/@class')

            movie_info = {
                '电影名': title,
                'score': get_score(score_class_list),
                '类型': genre,
                '上映时间': get_release_date(release_date),
                '时长': get_runtime(runtime),
                'tagline': tagline,
                '简介': overview
            }
            return movie_info

        except (requests.ConnectionError, requests.Timeout) as e:
            print(f"请求失败 (尝试 {attempt+1}/{max_retries}): {url} - {e}")
            if attempt == max_retries - 1:
                print(f"达到最大重试次数，跳过该电影: {url}")
                return None
            # 指数退避：1, 2, 4 秒
            time.sleep(2 ** attempt)

    return None
def get_genre(genre_list):
    if not genre_list:
        return ''
        # 先将列表拼成一个字符串，如 "冒险 动画 家庭 奇幻"
    combined = ' '.join(genre_list)
    # 将空格、顿号、逗号、“和”替换为 /
    cleaned = re.sub(r'\s*[,，、和]\s*', '/', combined)
    return cleaned
def get_runtime(runtime):
    h = 0
    m = 0
    #
    if runtime:
        h_time=re.search(r'(\d+)h', runtime)
        m_time=re.search(r'(\d+)m', runtime)
        # print(h_time.group(0))
        # print(h_time.group(1))
        h=int(h_time.group(1)) if h_time else 0
        m=int(m_time.group(1)) if m_time else 0
    return  h*60+m

def get_score(score_class_list):
    score = ''
    if score_class_list:
        class_str = score_class_list[0]
        if '-r' in class_str:
            # score = class_str.split('-r')[1]
            score = re.search(r'\d+', class_str).group()  # 正则表达式
    return  score
def get_release_date(release_date):
    if release_date:
        release_date = re.search(r'\d{4}-\d{2}-\d{2}', release_date).group()
    return  release_date
def main():
    session.headers.update({
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    csv_file = 'csv_data/movies.csv'
    # 存储已爬取过的电影 ID
    crawled_ids = set()

    # 如果 CSV 文件已存在，读取已爬取的数据
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)  # 跳过表头
            except StopIteration:
                pass
            for row in reader:
                # 假设电影名在第一列，但最好存储 ID（可惜 CSV 中没有 ID 列）
                # 我们只能通过 URL 回忆，或者你可以在 CSV 中加一列 'id'
                # 但更简单的是：在爬取时同时记录 ID 到另一个文件（如 crawled.txt）
                # 这里推荐额外维护一个记录文件
                pass
        # 更好的办法：单独维护一个已爬取 ID 的文本文件
    else:
        # 确保目录存在
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    # ----- 更稳健的方案：单独维护一个 visited_ids.txt 文件 -----
    visited_file = 'csv_data/visited_ids.txt'
    if os.path.exists(visited_file):
        with open(visited_file, 'r', encoding='utf-8') as vf:
            crawled_ids = set(line.strip() for line in vf if line.strip())

    # 打开 CSV 文件（追加模式）
    with open(csv_file, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 如果文件为空，则写入表头
        if os.path.getsize(csv_file) == 0:
            writer.writerow(['电影名', 'score', '类型', '上映时间', '时长', 'tagline', '简介'])
        for page_num in range(1, 51):
            # 分页请求
            if page_num == 1:
                response = requests.get(TMBD_TOP_URL, timeout=60)
            else:
                data = (
                    f'air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug='
                    f'&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false'
                    f'&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}'
                    f'&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte='
                    f'&release_date.lte=2026-12-04&show_me=everything&sort_by=popularity.desc'
                    f'&vote_average.gte=0&vote_average.lte=10&vote_count.gte=0&watch_region=CN'
                    f'&with_genres=&with_keywords=&with_networks=&with_origin_country='
                    f'&with_original_language=&with_watch_monetization_types=&with_watch_providers='
                    f'&with_release_type=&with_runtime.gte=0&with_runtime.lte=400'
                )
                response = requests.post(TMBD_TOP_URL2, data=data, timeout=60)

            document = html.fromstring(response.text)
            movie_list = document.xpath('//*[@class="media-list-results contents"]/div')

            # 遍历当前页电影
            for movie in movie_list:
                movie_urls = movie.xpath('./div/div/a/@href')
                if not movie_urls:
                    continue
                movie_url = TMBD_BASE_URL + movie_urls[0]
                movie_id = extract_movie_id(movie_url)

                # 检查是否已经爬取过
                if movie_id and movie_id in crawled_ids:
                    print(f"跳过已爬取电影 ID: {movie_id}")
                    continue

                movie_info = get_movie_info(movie_url)
                if movie_info is None:
                    continue

                # 写入 CSV
                writer.writerow([movie_info['电影名'], movie_info['score'], movie_info['类型'],
                                 movie_info['上映时间'], movie_info['时长'], movie_info['tagline'], movie_info['简介']])
                # 记录已爬取 ID
                if movie_id:
                    crawled_ids.add(movie_id)
                    with open(visited_file, 'a', encoding='utf-8') as vf:
                        vf.write(movie_id + '\n')
                    print(f" 电影名：{movie_info['电影名']} ,评分: {movie_info['score']},类型: {movie_info['类型']},上映时间 :{movie_info['上映时间']},时长: {movie_info['时长']},tagline{movie_info['tagline']},简介: {movie_info['简介']}")

                    # 可选：强制刷新缓冲区
                    f.flush()

    print("所有数据已保存到 csv_data/movies.csv")

if __name__ == '__main__':
    main()