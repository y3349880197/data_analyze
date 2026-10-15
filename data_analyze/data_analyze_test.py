import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # macOS 自带中文字体
plt.rcParams['axes.unicode_minus'] = False              # 解决负号显示成方块

df = pd.read_csv('data/films.csv')

figure, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 18))

#每一年上映电影数量变化图
def films_num_change():
    axes_1: Axes = axes[0][0]


    nums_count = df.groupby('年份')['年份'].count().dropna()
    min_year = nums_count.index.min()
    max_year = nums_count.index.max()
    full_years = range(min_year, max_year + 1)
    nums_count = nums_count.reindex(full_years, fill_value=0)

    year = nums_count.index.tolist()
    num = nums_count.values.tolist()

    axes_1.plot(year, num)
    axes_1.set_title('每一年上映电影数量变化图', fontsize=20)
    axes_1.set_xlabel('年份')
    axes_1.set_ylabel('数量')
    axes_1.set_xticks(year[::8])


#不同语言电影数量
def films_language_num():
    axes_2: Axes = axes[0][1]

    s = df.groupby('语言')['语言'].count().dropna().to_dict()

    languages = []
    num = []

    for key, value in s.items():
        languages.append(key)
        num.append(value)

    axes_2.bar(languages, num)
    axes_2.set_title('不同语言电影数量', fontsize=20)
    axes_2.set_xlabel('语言', fontsize=8)
    axes_2.set_ylabel('数量')

#不同类型电影数量
def films_type_num():
    axes_3: Axes = axes[1][0]

    type_dict = {}

    for item in df['类型'].dropna():
        for t in item.replace(' ', '').split('/'):
            type_dict[t] = type_dict.get(t, 1) + 1

    types = list(type_dict.keys())
    nums = list(type_dict.values())

    axes_3.bar(types, nums)
    axes_3.set_title('不同类型电影数量', fontsize=20)
    axes_3.set_xlabel('电影类型')
    axes_3.set_ylabel('数量')

#各部电影评分的比例
def films_score_percent():
    axes_4: Axes = axes[1][1]

    percent_count = df.groupby('评分')['评分'].count()

    total = percent_count.sum()

    large_count = percent_count.loc[percent_count >= total*0.06]
    small_count = percent_count.loc[percent_count < total*0.06]

    if small_count.shape[0] > 0:
        large_count['其他'] = small_count.sum()

    percents = large_count.index.tolist()
    scores = large_count.values.tolist()

    axes_4.pie(scores, labels=percents, autopct='%1.1f%%')
    axes_4.set_title('电影评分的比例', fontsize=20)
    axes_4.legend(loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.1))



if __name__ == '__main__':
    # 每一年上映电影数量变化图-->折线图
    films_num_change()

    # 不同语言电影数量-->柱状图
    films_language_num()

    # 不同类型电影数量-->柱状图
    films_type_num()

    # 各部电影评分的比例-->饼状图
    films_score_percent()

    plt.savefig('data/02.png')

    plt.show()