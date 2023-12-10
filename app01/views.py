from django.shortcuts import render,HttpResponse
from . import spider,spider_gupiao
# Create your views here.
def index(request):
    return render(request, 'index.html')

def run_spider(request):
    # print(['python', 'spider.py'])
    spider.my_spider()
    data_option = request.GET.get('data_option')
    # return render(request, spider.show_csv())
    return render(request,spider.show_csv(data_option))

def run_stock(requset):
    spider_gupiao.spider_gupiao()
    data_category = requset.GET.get('data_category')

    return render(requset,spider_gupiao.visualize_category(data_category))

# def visualize_stock_data(request):
#     if request.method == 'POST':
#         stock_name = request.POST.get('stockName')
#         spider_gupiao.visualize_stock_data(stock_name)
#         return render(request, 'stock_visualization.html')