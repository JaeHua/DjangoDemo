import requests
import parsel
import csv
import  os
import pandas as pd
from django.db import connection
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar
from app01.models import Country
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
# def my_spider():
#     with open(save_path, mode='w', encoding="ANSI", newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['Country', 'GDP', 'GDP Growth', 'Interest Rate', 'Inflation Rate', 'Jobless Rate', 'GovBudget', 'Debt/GDP', 'Current Account', 'Population'])
#
#     selectors = parsel.Selector(resp.text)
#     td_elements = selectors.css('tr > td')
#
#     list_data = []
#     # print('doing')
#     for index, td in enumerate(td_elements):
#         data = td.css('::text').get()
#         list_data.append(data)
#         if index % 10 == 9 :
#             with open(save_path, mode='a', encoding="ANSI", newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(list_data)
#             list_data = []
#主键置1
def reset_auto_increment(model):
    model.objects.all().delete()

    table_name = model._meta.db_table
    cursor = connection.cursor()
    cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1")
    cursor.close()
def my_spider():
    reset_auto_increment(Country)
    selectors = parsel.Selector(resp.text)
    td_elements = selectors.css('tr > td')

    list_data = []
    for index, td in enumerate(td_elements):
        data = td.css('::text').get()

        # 处理每个属性字段
        if index % 10 == 0:
            name = data
            list_data.append(name)
        elif index % 10 == 1:
            gdp = float(data) if data else 0.0  # 处理空值
            list_data.append(gdp)
        elif index % 10 == 2:
            gdp_growth = float(data) if data else 0.0  # 处理空值
            list_data.append(gdp_growth)
        elif index % 10 == 3:
            interest_rate = float(data) if data else 0.0  # 处理空值
            list_data.append(interest_rate)
        elif index % 10 == 4:
            inflation_rate = float(data) if data else 0.0  # 处理空值
            list_data.append(inflation_rate)
        elif index % 10 == 5:
            jobless_rate = float(data) if data else 0.0  # 处理空值
            list_data.append(jobless_rate)
        elif index % 10 == 6:
            gov_budget = float(data) if data else 0.0  # 处理空值
            list_data.append(gov_budget)
        elif index % 10 == 7:
            debt_gdp = float(data) if data else 0.0  # 处理空值
            list_data.append(debt_gdp)
        elif index % 10 == 8:
            current_account = float(data) if data else 0.0  # 处理空值
            list_data.append(current_account)
        elif index % 10 == 9:
            population = float(data) if data else 0.0  # 处理空值
            list_data.append(population)

            try:
                country = Country(
                    name=list_data[0],
                    gdp=list_data[1],
                    gdp_growth=list_data[2],
                    interest_rate=list_data[3],
                    inflation_rate=list_data[4],
                    jobless_rate=list_data[5],
                    gov_budget=list_data[6],
                    debt_gdp=list_data[7],
                    current_account=list_data[8],
                    population=list_data[9],
                )
                country.save()
            except ValueError as e:
                print(f"Error saving data: {e}")

            list_data = []
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
#         .add_xaxis(countries[:50])
#         .add_yaxis(title, data[:50])
#         .set_global_opts(
#             title_opts=opts.TitleOpts(title=title),
#             datazoom_opts=opts.DataZoomOpts(),
#             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
#             # 添加以下配置选项来美化图表
#             toolbox_opts=opts.ToolboxOpts(),  # 添加工具箱
#             legend_opts=opts.LegendOpts(pos_right='10%', pos_bottom='5%'),  # 调整图例的位置
#             yaxis_opts=opts.AxisOpts(
#                 axislabel_opts=opts.LabelOpts(formatter='{value}'),  # 设置y轴标签格式
#                 splitline_opts=opts.SplitLineOpts(is_show=True),  # 显示网格线
#             ),
#             visualmap_opts=opts.VisualMapOpts(is_show=False),  # 隐藏视觉映射组件
#         )
#     )
#     # 生成render.html
#     # 指定保存路径并生成HTML文件
#     save_pa = os.path.join(current_directory, 'templates', 'gdp_bar_chart.html')
#     bar.render(save_pa)
#     return 'gdp_bar_chart.html'

def show_csv(data_option):
    # 从数据库中获取数据
    countries = []
    data = []
    queryset = Country.objects.order_by(data_option).reverse()  # 获取前50条数据，按照指定字段降序排序
    for country in queryset:
        countries.append(country.name)
        data.append(getattr(country, data_option))

    # 创建柱状图实例
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width='100vw', height='100vh'))
        .add_xaxis(countries)
        .add_yaxis(data_option, data)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=data_option),
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
    save_path = os.path.join(current_directory, 'templates', 'gdp_bar_chart.html')
    bar.render(save_path)
    return 'gdp_bar_chart.html'

def show_country_data(name_):
    data = Country.objects.filter(name__contains=name_)

    if not data.exists():
        error_message = f"Country '{name_}' not found."
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
        html_content = "<html><head>"
        html_content += "<style>"
        html_content += "body {"
        html_content += "    display: flex;"
        html_content += "    justify-content: center;"
        html_content += "    align-items: center;"
        html_content += "    height: 100vh;"
        html_content += "}"
        html_content += "table {"
        html_content += "    border-collapse: collapse;"
        html_content += "    width: 70%;"
        html_content += "}"
        html_content += "th, td {"
        html_content += "    padding: 8px;"
        html_content += "    text-align: left;"
        html_content += "    border-bottom: 1px solid #ddd;"
        html_content += "    border-right: 1px solid #ddd;"
        html_content += "}"
        html_content += "th {"
        html_content += "    background-color: #f2f2f2;"
        html_content += "}"
        html_content += "tr:last-child td {"
        html_content += "    border-bottom: none;"
        html_content += "}"
        html_content += "td:last-child {"
        html_content += "    border-right: none;"
        html_content += "}"
        html_content += ".search-result {"
        html_content += "    background-color: #ffffcc;"
        html_content += "}"
        html_content += "</style>"
        html_content += "</head><body>"
        html_content += "<table>"
        html_content += "<tr><th>Country</th><th>GDP</th><th>GDP Growth</th><th>Interest Rate</th><th>Inflation Rate</th><th>Jobless Rate</th><th>Government Budget</th><th>Debt to GDP</th><th>Current Account</th><th>Population</th></tr>"

        for da in data:
            html_content += "<tr class='search-result'>"
            html_content += "<td>{}</td>".format(da.name)
            html_content += "<td>{}</td>".format(da.gdp)
            html_content += "<td>{}</td>".format(da.gdp_growth)
            html_content += "<td>{}</td>".format(da.interest_rate)
            html_content += "<td>{}</td>".format(da.inflation_rate)
            html_content += "<td>{}</td>".format(da.jobless_rate)
            html_content += "<td>{}</td>".format(da.gov_budget)
            html_content += "<td>{}</td>".format(da.debt_gdp)
            html_content += "<td>{}</td>".format(da.current_account)
            html_content += "<td>{}</td>".format(da.population)
            html_content += "</tr>"

        html_content += "</table>"
        html_content += "</body></html>"
        save_pa = os.path.join(current_directory, 'templates', 'special_country_data.html')
        with open(save_pa, 'w') as file:
            file.write(html_content)
        return 'special_country_data.html'