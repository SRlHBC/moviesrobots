"""
TMBDTOP1000电影榜单统计分析
功能: 对TMBD TOP1000电影数据进行多维度可视化分析
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


def load_and_clean_data(filepath='csv_data/movies.csv'):
    """
    加载并清洗数据

    参数:
        filepath: CSV文件路径

    返回:
        清洗后的DataFrame
    """
    df = pd.read_csv(filepath)

    # 转换数据类型
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['时长'] = pd.to_numeric(df['时长'], errors='coerce')
    df['上映时间'] = pd.to_datetime(df['上映时间'], errors='coerce')
    df['年份'] = df['上映时间'].dt.year

    return df


def plot_genre_avg_score(df, save_path='data/movies_plot.png', top_n=20):
    """
    绘制各类型电影平均评分Top N柱状图

    参数:
        df: DataFrame数据
        save_path: 图片保存路径
        top_n: 展示前N个类型
    """
    # 配置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 按类型分组，计算平均评分
    type_avg = df.groupby('类型')['score'].mean().sort_values(ascending=False)

    # 创建图表
    plt.figure(figsize=(12, 6))
    type_avg.head(top_n).plot(kind='bar', color='skyblue')
    plt.title(f'各类型电影平均评分 Top {top_n}', fontsize=16)
    plt.xlabel('电影类型', fontsize=12)
    plt.ylabel('平均评分', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # 保存图片
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.show()

    print(f"图表已保存至: {save_path}")


def plot_score_distribution(df, save_path='data/movies_plot1.png', bins=50):
    """
    绘制电影评分分布直方图

    参数:
        df: DataFrame数据
        save_path: 图片保存路径
        bins: 直方图柱数
    """
    # 配置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建图表
    plt.figure(figsize=(16, 5))
    plt.hist(df['score'].dropna(), bins=bins, edgecolor='black', alpha=0.7)
    plt.title('电影评分分布', fontsize=16)
    plt.xlabel('评分', fontsize=12)
    plt.ylabel('电影数量', fontsize=12)
    plt.xticks(range(0, 101, 10))
    plt.yticks(range(0, 101, 10))

    # 保存图片
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.show()

    print(f"图表已保存至: {save_path}")


def plot_scatter_and_pie(df, save_path='data/movies_plot2.png', top_n=8):
    """
    绘制散点图(时长vs评分)和饼图(类型分布)

    参数:
        df: DataFrame数据
        save_path: 图片保存路径
        top_n: 饼图展示前N个类型
    """
    # 配置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 拆分类型列用于饼图统计
    df['类型'] = df['类型'].fillna('')
    df['类型列表'] = df['类型'].str.split('/')
    df_exploded = df.explode('类型列表')
    type_counts = df_exploded['类型列表'].value_counts()

    # 创建子图布局
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 子图1: 散点图(时长 vs 评分)
    scatter_data = df.dropna(subset=['时长', 'score'])
    ax1.scatter(scatter_data['时长'], scatter_data['score'], alpha=0.5, color='coral')
    ax1.set_title('电影时长与评分的关系', fontsize=14)
    ax1.set_xlabel('时长(分钟)', fontsize=12)
    ax1.set_ylabel('评分', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.3)

    # 子图2: 饼图(类型分布)
    top_types = type_counts.head(top_n)
    others = type_counts.iloc[top_n:].sum()
    if others > 0:
        top_types['其他'] = others

    ax2.pie(top_types.values, labels=top_types.index, autopct='%1.1f%%', startangle=90)
    ax2.set_title(f'电影类型分布(前{top_n}类)', fontsize=14)
    ax2.axis('equal')
    ax2.legend(loc='upper right', bbox_to_anchor=(1.2, 1))

    plt.tight_layout()

    # 保存图片
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.show()

    print(f"图表已保存至: {save_path}")


def plot_yearly_trends(df, save_path='data/movies_plot3.png'):
    """
    绘制每年平均评分趋势和电影数量柱状图(非连续年份)

    参数:
        df: DataFrame数据
        save_path: 图片保存路径
    """
    # 配置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 聚合数据
    year_avg = df.groupby('年份')['score'].mean().dropna().sort_index()
    year_count = df['年份'].value_counts().sort_index()

    # 创建子图布局
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 子图1: 折线图(平均评分趋势)
    ax1.plot(year_avg.index, year_avg.values, marker='o', linestyle='-', color='coral', linewidth=2)
    ax1.set_title('不同年份上映电影的平均评分趋势', fontsize=14)
    ax1.set_xlabel('年份', fontsize=12)
    ax1.set_ylabel('平均评分', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_xticks(range(1930, 2050, 10))
    ax1.set_yticks(range(0, 101, 20))
    ax1.set_xlim(1930, 2030)

    # 子图2: 柱状图(每年电影数量)
    ax2.bar(year_count.index, year_count.values, width=0.8, color='coral', edgecolor='black')
    ax2.set_title('每年上映电影数量', fontsize=14)
    ax2.set_xlabel('年份', fontsize=12)
    ax2.set_ylabel('电影数量', fontsize=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.6)
    ax2.set_xticks(range(1930, 2050, 10))
    ax2.set_xlim(1930, 2030)

    plt.tight_layout()

    # 保存图片
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.show()

    print(f"图表已保存至: {save_path}")


def plot_yearly_trends_continuous(df, save_path='data/movies_plot4.png'):
    """
    绘制每年平均评分趋势和电影数量柱状图(连续年份)

    参数:
        df: DataFrame数据
        save_path: 图片保存路径
    """
    # 配置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 聚合原始数据
    year_avg_raw = df.groupby('年份')['score'].mean().dropna()
    year_count_raw = df['年份'].value_counts()

    # 构造连续年份范围
    min_year = int(df['年份'].min())
    max_year = int(df['年份'].max())
    all_years = range(min_year, max_year + 1)

    # 重新索引，填充缺失值
    year_avg = year_avg_raw.reindex(all_years)
    year_count = year_count_raw.reindex(all_years, fill_value=0)

    # 创建子图布局
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 子图1: 折线图(平均评分趋势)
    ax1.plot(year_avg.index, year_avg.values, marker='o', linestyle='-', color='coral', linewidth=2)
    ax1.set_title('不同年份上映电影的平均评分趋势', fontsize=14)
    ax1.set_xlabel('年份', fontsize=12)
    ax1.set_ylabel('平均评分', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_xticks(range(min_year, max_year + 1, 10))
    ax1.set_xlim(min_year, max_year)
    ax1.set_yticks(range(0, 101, 20))

    # 子图2: 柱状图(每年电影数量)
    ax2.bar(year_count.index, year_count.values, width=0.8, color='coral', edgecolor='black')
    ax2.set_title('每年上映电影数量', fontsize=14)
    ax2.set_xlabel('年份', fontsize=12)
    ax2.set_ylabel('电影数量', fontsize=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.6)
    ax2.set_xticks(range(min_year, max_year + 1, 10))
    ax2.set_xlim(min_year, max_year)

    plt.tight_layout()

    # 保存图片
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.show()

    print(f"图表已保存至: {save_path}")


def main():
    """
    主函数: 执行所有分析流程
    """
    print("=" * 60)
    print("TMBDTOP1000电影榜单统计分析")
    print("=" * 60)

    # 1. 加载数据
    print("\n[1/6] 正在加载数据...")
    df = load_and_clean_data()
    print(f"✓ 数据加载完成，共 {len(df)} 条记录")
    print(f"  数据列: {list(df.columns)}")

    # 2. 生成图表1: 各类型电影平均评分Top 20
    print("\n[2/6] 正在生成各类型电影平均评分Top 20...")
    plot_genre_avg_score(df)

    # 3. 生成图表2: 电影评分分布
    print("\n[3/6] 正在生成电影评分分布图...")
    plot_score_distribution(df)

    # 4. 生成图表3: 时长vs评分散点图 + 类型分布饼图
    print("\n[4/6] 正在生成时长-评分关系图和类型分布图...")
    plot_scatter_and_pie(df)

    # 5. 生成图表4: 年度趋势分析(非连续)
    print("\n[5/6] 正在生成年份趋势图(非连续)...")
    plot_yearly_trends(df)

    # 6. 生成图表5: 年度趋势分析(连续)
    print("\n[6/6] 正在生成年份趋势图(连续)...")
    plot_yearly_trends_continuous(df)

    print("\n" + "=" * 60)
    print("✓ 所有分析完成！图表已保存至 data/ 目录")
    print("=" * 60)


if __name__ == '__main__':
    main()
