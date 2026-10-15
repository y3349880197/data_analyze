import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # macOS 自带中文字体
plt.rcParams['axes.unicode_minus'] = False              # 解决负号显示成方块

df = pd.read_csv('data/sales.csv', usecols=['订单号', '产品类别', '产品名称', '销售数量', '单价', '收货城市', '支付方式', '订单日期'])

figure, axes = plt.subplots(nrows=2, ncols=2, figsize=(30, 15))

#统计每天销售额变化 折线图
def sales_change():
    df['销售额'] = df['销售数量'] * df['单价']
    df['订单日期'] = pd.to_datetime(df['订单日期'])
    sales_num = df.groupby('订单日期')['销售额'].sum()

    min_date = sales_num.index.min()
    max_date = sales_num.index.max()
    full_dates = pd.date_range(start=min_date, end=max_date, freq='D')

    sales_num = sales_num.reindex(full_dates, fill_value=0)

    date = sales_num.index.tolist()
    sales = sales_num.values.tolist()

    axes_1: Axes = axes[0][0]
    axes_1.plot(date, sales)
    axes_1.set_title('每天销售额变化图', fontsize=20)
    axes_1.set_xlabel('订单日期')
    axes_1.set_ylabel('销售额')
    axes_1.set_xticks(date[::10])



#对比不同城市的累积销售数量 柱状图
def sales_countries_change():
    sales_countries = df.groupby('收货城市')['销售数量'].sum()

    countries = sales_countries.index.tolist()
    sales = sales_countries.values.tolist()

    axes_2: Axes = axes[0][1]
    axes_2.bar(countries, sales)
    axes_2.set_title('不同城市的累积销售数量图', fontsize=20)
    axes_2.set_xlabel('城市')
    axes_2.set_ylabel('销售数量')


#不同产品类型对应的订单比例 饼状图
def sales_type():
    type_order = df.groupby('产品类别')['销售数量'].sum()

    type = type_order.index.tolist()
    order = type_order.values.tolist()

    axes_3: Axes = axes[1][0]
    axes_3.pie(order, labels=type, autopct='%1.1f%%')
    axes_3.set_title('不同产品类型对应的订单比例图', fontsize=20)
    axes_3.legend(loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.1))

#不同支付方式对应的订单比例 饼状图
def sales_pay_type():
    pay_type_order = df.groupby('支付方式')['销售数量'].sum()

    pay_type = pay_type_order.index.tolist()
    order = pay_type_order.values.tolist()

    axes_4: Axes = axes[1][1]
    axes_4.pie(order, labels=pay_type, autopct='%1.1f%%')
    axes_4.set_title('不同支付方式对应的订单比例图', fontsize=20)
    axes_4.legend(loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.06))

if __name__ == '__main__':
    sales_change()
    sales_countries_change()
    sales_type()
    sales_pay_type()

    plt.savefig('data/03.png')
    plt.show()
