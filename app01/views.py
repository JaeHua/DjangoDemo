from django.shortcuts import render,HttpResponse
from . import spider
# Create your views here.
def index(request):
    return render(request, 'index.html')

def run_spider(request):
    # print(['python', 'spider.py'])
    spider.my_spider()
    data_option = request.GET.get('data_option')
    # return render(request, spider.show_csv())
    return render(request,spider.show_csv(data_option))