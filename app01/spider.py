import requests
import parsel
import csv
import  os
import pandas as pd
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar
headers = {
    'Cookie': '_ga=GA1.1.851974330.1701698064; ASP.NET_SessionId=5j15cdinvmmz5neoy0xcvepi; TEServer=TEIIS2; _ga_SZ14JCTXWQ=GS1.1.1701698064.1.1.1701700647.0.0.0',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0',
}

url = 'https://tradingeconomics.com/matrix'
resp = requests.get(url, headers=headers)
# 获取当前文件所在的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 拼接保存路径
save_path = os.path.join(current_directory, 'data_csv', '全球经济状况.csv')
def my_spider():
    with open(save_path, mode='w', encoding="ANSI", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Country', 'GDP', 'GDP Growth', 'Interest Rate', 'Inflation Rate', 'Jobless Rate', 'GovBudget', 'Debt/GDP', 'Current Account', 'Population'])

    selectors = parsel.Selector(resp.text)
    td_elements = selectors.css('tr > td')

    list_data = []
    # print('doing')
    for index, td in enumerate(td_elements):
        data = td.css('::text').get()
        list_data.append(data)
        if index % 10 == 9 :
            with open(save_path, mode='a', encoding="ANSI", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(list_data)
            list_data = []
# def show_csv():
#
#     # 准备数据
#     df = pd.read_csv(save_path)
#     countries = list(df['Country'])
#     gdp = list(df['GDP'])
#
#     # 创建柱状图实例
#     bar = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='100vw', height='100vh'))
#         .add_xaxis(countries[:50])  # 设置x轴数据
#         .add_yaxis("GDP", gdp[:50])  # 设置y轴数据和系列名称
#         .set_global_opts(
#             title_opts=opts.TitleOpts(title="GDP"),  # 设置图表标题
#             datazoom_opts=opts.DataZoomOpts(),  # 设置数据缩放
#             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
#         )
#     )
#
#     # 生成render.html
#     # 指定保存路径并生成HTML文件
#     save_pa = os.path.join(current_directory, 'templates', 'gdp_bar_chart.html')
#     bar.render(save_pa)
#     return 'gdp_bar_chart.html'

def show_csv(data_option):
    # 准备数据
    df = pd.read_csv(save_path)
    df = df.sort_values(by=data_option, ascending=False)
    countries = list(df['Country'])
    data = list(df[data_option])
    title = data_option

    # 创建柱状图实例
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='100vw', height='100vh'))
        .add_xaxis(countries[:50])
        .add_yaxis(title, data[:50])
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            # 添加以下配置选项来美化图表
            toolbox_opts=opts.ToolboxOpts(),  # 添加工具箱
            legend_opts=opts.LegendOpts(pos_right='10%', pos_bottom='5%'),  # 调整图例的位置
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter='{value}'),  # 设置y轴标签格式
                splitline_opts=opts.SplitLineOpts(is_show=True),  # 显示网格线
            ),
            visualmap_opts=opts.VisualMapOpts(is_show=False),  # 隐藏视觉映射组件
        )
    )
    # 生成render.html
    # 指定保存路径并生成HTML文件
    save_pa = os.path.join(current_directory, 'templates', 'gdp_bar_chart.html')
    bar.render(save_pa)
    return 'gdp_bar_chart.html'


# def show_csv(data_option):
#     # 准备数据
#     df = pd.read_csv(save_path)
#     df = df.sort_values(by=data_option, ascending=False)
#     countries = list(df['Country'])
#     data = list(df[data_option])
#     title = data_option
#
#     # 创建柱状图实例
#     bar = (
#         Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='100vw', height='100vh'))
#         .add_xaxis(countries[:50])  # 设置x轴数据
#         .add_yaxis(title, data[:50])  # 设置y轴数据和系列名称
#         .set_global_opts(
#             title_opts=opts.TitleOpts(title=title),  # 设置图表标题
#             datazoom_opts=opts.DataZoomOpts(),  # 设置数据缩放
#             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
#         )
#     )
#
#     # 生成render.html
#     # 指定保存路径并生成HTML文件
#     save_pa = os.path.join(current_directory, 'templates', 'gdp_bar_chart.html')
#     bar.render(save_pa)
#     return 'gdp_bar_chart.html'