# TMDB TOP1000 电影数据爬取与可视化分析

## 项目简介

本项目基于 Python 实现 TMDB（The Movie Database）电影数据的自动爬取、清洗、统计分析与可视化展示。

系统通过爬取 TMDB 网站电影排行榜数据，获取电影名称、评分、类型、上映时间、时长、Tagline 以及简介等信息，并保存至 CSV 文件中。随后利用 Pandas 与 Matplotlib 对数据进行多维度分析，生成可视化图表，帮助用户了解电影评分分布、类型特征以及时间趋势等信息。

---

# 项目功能

## 1. 电影数据爬取

自动获取 TMDB 网站电影数据。

采集内容包括：

* 电影名称
* 电影评分
* 电影类型
* 上映日期
* 电影时长
* Tagline
* 电影简介

支持：

* 分页爬取
* 自动重试
* 断点续爬
* 数据去重

---

## 2. 数据存储

将采集结果保存至 CSV 文件。

目录结构：

```text
csv_data/
├── movies.csv
└── visited_ids.txt
```

其中：

movies.csv

用于保存电影数据。

visited_ids.txt

用于记录已爬取电影ID，避免重复采集。

---

## 3. 数据清洗

使用 Pandas 对数据进行预处理：

* 评分转数值类型
* 时长转数值类型
* 日期格式转换
* 提取上映年份
* 缺失值处理

---

## 4. 数据统计分析

实现以下统计分析：

### 各类型电影平均评分分析

统计不同类型电影的平均评分。

例如：

* 剧情片
* 犯罪片
* 动画片
* 战争片

等类型的评分表现。

---

### 电影评分分布分析

分析：

* 高分电影数量
* 中分电影数量
* 低分电影数量

观察整体评分分布情况。

---

### 电影时长与评分关系分析

研究：

电影时长是否影响评分。

采用散点图展示：

```text
X轴：电影时长
Y轴：电影评分
```

---

### 电影类型占比分析

统计：

* 动作片
* 剧情片
* 喜剧片
* 科幻片
* 犯罪片

等类型占全部电影中的比例。

---

### 上映年份趋势分析

统计：

* 每年电影数量变化
* 每年平均评分变化

观察电影发展趋势。

---

# 技术栈

## 数据采集

* Requests
* lxml
* XPath
* Regex

---

## 数据处理

* Pandas
* NumPy

---

## 数据可视化

* Matplotlib

---

## 数据存储

* CSV

---

# 项目结构

```text
TMDB-Movie-Analysis/
│
├── spider.py                 # 数据爬虫
├── analysis.py               # 数据分析
│
├── csv_data/
│   ├── movies.csv
│   └── visited_ids.txt
│
├── data/
│   ├── movies_plot.png
│   ├── movies_plot1.png
│   ├── movies_plot2.png
│   ├── movies_plot3.png
│   └── movies_plot4.png
│
└── README.md
```

---

# 环境要求

Python 3.9+

推荐：

```bash
Python 3.10+
```

---

# 安装依赖

```bash
pip install requests
pip install pandas
pip install matplotlib
pip install lxml
pip install urllib3
```

或者：

```bash
pip install -r requirements.txt
```

requirements.txt：

```text
requests
pandas
matplotlib
lxml
urllib3
```

---

# 运行方式

## 1. 爬取电影数据

执行：

```bash
python spider.py
```

运行后将自动：

* 获取电影列表
* 获取电影详情
* 保存数据到 CSV

输出：

```text
电影名：The Shawshank Redemption
评分：95
类型：Drama/Crime
上映时间：1994-09-23
时长：142
```

---

## 2. 数据分析

执行：

```bash
python analysis.py
```

系统将自动生成以下图表：

### 图1

各类型电影平均评分 Top20

```text
movies_plot.png
```

---

### 图2

电影评分分布直方图

```text
movies_plot1.png
```

---

### 图3

电影时长与评分关系图

电影类型分布饼图

```text
movies_plot2.png
```

---

### 图4

年份趋势分析（非连续年份）

```text
movies_plot3.png
```

---

### 图5

年份趋势分析（连续年份）

```text
movies_plot4.png
```

---

# 核心实现

## 自动重试机制

使用：

```python
Retry
HTTPAdapter
```

实现请求失败自动重试。

支持：

* ConnectionError
* Timeout
* 500错误
* 502错误
* 503错误
* 504错误

---

## 断点续爬

利用：

```text
visited_ids.txt
```

记录已采集电影ID。

实现：

* 中断后继续运行
* 避免重复爬取
* 提高效率

---

## XPath解析

使用：

```python
lxml.html
```

解析页面结构。

提取：

* 标题
* 类型
* 评分
* 简介
* 上映日期

等信息。

---

# 分析结果示例

通过数据分析可以发现：

1. 剧情类电影整体评分较高；

2. 高评分电影主要集中在 80~95 分区间；

3. 电影时长与评分不存在明显线性关系；

4. 剧情、犯罪、动作类电影占比较高；

5. 2000 年以后电影数量明显增长。

---

# 项目特色

✅ TMDB电影数据采集

✅ 自动重试机制

✅ 断点续爬

✅ XPath网页解析

✅ Pandas数据清洗

✅ Matplotlib数据可视化

✅ 多维度统计分析

✅ 完整的数据分析流程

---

# 作者

项目名称：

TMDB TOP1000电影数据爬取与可视化分析

技术方向：

Python爬虫 / 数据分析 / 数据可视化

开发工具：

PyCharm + Python + Pandas + Matplotlib
