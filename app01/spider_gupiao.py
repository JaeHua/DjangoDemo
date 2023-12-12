import requests
import csv
import pandas as pd
import os

from django.http import HttpResponse
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar

headers = {
    'Cookie': "device_id=e40f9e10e75cea02ba56c6fe11f7b24d; s=c411o3x2dj; cookiesu=751702187038670; xq_a_token=a97fa15a5bb947c53ed434a6c0364dd03f36962c; xq_r_token=457987e3f3df9d22b53ad50b975087ff84ee9a79; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcwNDU4NzkwNCwiY3RtIjoxNzAyMjA2NjA4ODM1LCJjaWQiOiJkOWQwbjRBWnVwIn0.Drz-xZza94f9oq2sbbpdrirKju-gBTaUqz5WJFM4PyjYS9d6YICw5k4dn3RmXPv0CxGOy74uxuoUQPPHMU2V2kPkqGKg4O6mGBpsARu88aLo8nQ7gM0qtKjm7AbPqHeqZvhskhPpuWb0cvcyDHEsIpQVRudpWuBpLflqTnt20JF5cbDQrPRD25KeAXdSgIgUmyO6v9xk7dosKBO_sJHlIYry9b8QQDvqTdVCHYZ7jvvraUOvWHp2znM17oQkpSj4zZZwu5lIbJ9opzJEQXgVFuwZzqZNnFathxjSqr1ooK2WXbidnNcmmeN-f-xv5KWjTZq8MRcCUGwrXcvNO4DWSQ; u=751702187038670; Hm_lvt_1db88642e346389874251b5a1eded6e3=1702187040,1702187346,1702206655; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1702207260"
    ,
    'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0"
}
# 获取当前文件所在的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 拼接保存路径
save_path = os.path.join(current_directory, 'data_csv','股票行情.csv')

def spider_gupiao():
    with open(save_path, mode='w', encoding="ANSI", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['symbol', 'name', 'current', 'chg', 'percent', 'current_year_percent', 'volume', 'amount', 'turnover_rate',
             'pe_ttm', 'dividend_yield', 'market_capital'])
    url = f"https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=200&order=desc&order_by=amount&exchange=CN&market=CN&type=sha"
    response = requests.get(url, headers=headers)
    json_data = response.json()
    data_list = json_data['data']['list']
    for data in data_list:
        data1 = data['symbol']
        data2 = data['name']
        data3 = data['current']
        data4 = data['chg']
        data5 = data['percent']
        data6 = data['current_year_percent']
        data7 = data['volume']
        data8 = data['amount']
        data9 = data['turnover_rate']
        data10 = data['pe_ttm']
        data11 = data['dividend_yield']
        data12 = data['market_capital']
        # print(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12)
        data_list = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12]
        with open(save_path, mode='a', encoding="ANSI", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_list)


def visualize_category(data_category):
    df = pd.read_csv(save_path, encoding='ANSI')
    df = df.fillna(0)
    # 使用Pyecharts生成条形图
    print('----doing----')
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='100vw', height='100vh'))
        .add_xaxis(list(df['name']))
        .add_yaxis(data_category, list(df[data_category]))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f'{data_category} Distribution'),
            datazoom_opts=opts.DataZoomOpts(),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            toolbox_opts=opts.ToolboxOpts(),  # 添加工具箱
            legend_opts=opts.LegendOpts(pos_right='10%', pos_bottom='5%'),  # 调整图例的位置
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter='{value}'),  # 设置y轴标签格式
                splitline_opts=opts.SplitLineOpts(is_show=True),  # 显示网格线
            ),
            visualmap_opts=opts.VisualMapOpts(is_show=False),  # 隐藏视觉映射组件
        )
    )
    save_pa = os.path.join(current_directory, 'templates', 'sth_distribution_chart.html')
    print('doing2')
    bar.render(save_pa)  # 将图表保存为HTML文件，也可以使用render_notebook在Jupyter中显示
    return 'sth_distribution_chart.html'


def visualize_stock_data(stock_name):
    save_path = os.path.join(current_directory, 'data_csv', '股票行情.csv')
    df = pd.read_csv(save_path, encoding='ANSI')
    data = df[df['name'] == stock_name].iloc[:, 2:].squeeze()
    save_pat = os.path.join(current_directory, 'templates', '404.html')

    if data.empty:
        error_message = f"Stock '{stock_name}' not found."
        error_html = f'''
            <html>
            <head>
                <title>Error</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f5f5f5;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }}
                    .error-container {{
                        text-align: center;
                        padding: 40px;
                        background-color: #ffffff;
                        border-radius: 5px;
                        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        font-size: 24px;
                        margin-bottom: 20px;
                        text-transform: uppercase;
                        color: #333333;
                        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
                    }}
                    p {{
                        font-size: 18px;
                        color: #666666;
                    }}
                    .error-image {{
                        margin-top: 40px;
                    }}
                    .error-image img {{
                        max-width: 300px;
                    }}
                  .error-link {{
    margin-top: 20px;
    border: 1px solid #333333;
    display: inline-block;
    padding: 10px 20px;
    border-radius: 5px;
}}

.error-link a {{
    color: #333333;
    text-decoration: none;
    font-weight: bold;
}}
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h1>{error_message}</h1>
                    <p>Please check the stock name and try again.</p>
                    <div class="error-image">
                        <img src="https://cdn.pixabay.com/photo/2017/02/12/21/29/false-2061131_1280.png" alt="Error Image">
                    </div>
                    <div class="error-link">
                         <p>will return homepage in <span id="countdown">3</span> seconds。</p>
                    </div>
                </div>
                <script>
    var count = 3;
    var countdownElement = document.getElementById('countdown');

    function countdown() {{
        countdownElement.textContent = count;
        count--;

        if (count < 0) {{
            window.location.href = '/';
        }} else {{
            setTimeout(countdown, 1000);
      }}
    }}

    setTimeout(countdown, 1000);
</script>
            </body>
            </html>
        '''

        save_path = os.path.join(current_directory, 'templates', '404.html')
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(error_html)

        return '404.html'
    else:
        # 美化数据
        beautified_data = data.apply(lambda x: f'{x:,.2f}')  # 将数据格式化为带千位分隔符和两位小数的字符串

        # 生成美化的列表
        html_list = []
        for index, value in beautified_data.items():
            html_list.append(f'<li style="padding: 20px; background-color: #f2f2f2; border: 1px solid #ccc; border-radius: 5px; font-family: Arial; font-size: 16px; color: #333333; box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);"><b><span style="font-weight: bold; color: #000000;">{index}:</span></b> <span style="font-style: italic; color: #ff0000; text-decoration: underline;">{value}</span></li>')

        save_pa = os.path.join(current_directory, 'templates', 'data.html')

        # 将html_list渲染为HTML文件
        with open(save_pa, 'w', encoding='utf-8') as file:
            file.write('<html>\n')
            file.write('<head>\n')
            file.write('<style>\n')
            file.write('body {\n')
            file.write('  font-family: Arial, sans-serif;\n')
            file.write('  background-color: #f5f5f5;\n')
            file.write('  display: flex;\n')
            file.write('  justify-content: center;\n')
            file.write('  align-items: center;\n')
            file.write('  height: 100vh;\n')
            file.write('}\n')
            file.write('ul {\n')
            file.write('  list-style-type: none;\n')
            file.write('  padding: 0;\n')
            file.write('}\n')
            file.write('li {\n')
            file.write('  margin: 10px;\n')
            file.write('  padding: 20px;\n')
            file.write('  background-color: #ffffff;\n')
            file.write('  border-radius: 5px;\n')
            file.write('  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);\n')
            file.write('}\n')
            file.write('h1 {\n')
            file.write('  text-align: center;\n')
            file.write('  margin-bottom: 20px;\n')
            file.write('  text-transform: uppercase;\n')
            file.write('  color: #333333;\n')
            file.write('  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);\n')
            file.write('}\n')
            file.write('</style>\n')
            file.write('</head>\n')
            file.write('<body>\n')
            file.write(f'<h1><span style="font-family: Arial; font-size: 30px; color: black;">{stock_name}</span></h1>\n')
            file.write('<ul>\n')
            file.write('\n'.join(html_list))
            file.write('\n</ul</body>\n')
            file.write('</html>')

        return 'data.html'

#
# # 示例使用
# spider_gupiao(1)
#
# df = pd.read_csv('沪股行情.csv', encoding='ANSI')
# df = df.fillna(0)
# visualize_category('current')  # 可视化流通市值
# visualize_stock_data('招商银行')  # 可视化指定股票数据

