#coding:utf-8
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render(request,'ajax/index.html')

def add(request):
    #判断是否是ajax请求
    if request.is_ajax():
        ajax_str='Tajax'
    else:
        ajax_str='Fajax'
    a=request.GET['a']
    b=request.GET['b']
    print(a,b)
    a=int(a)
    b=int(b)
    return  HttpResponse(str(a+b)+ajax_str)

def ajax_list(request):
    #list
    a = range(100)
    return JsonResponse(a, safe=False)

def ajax_dict(request):
    name_dict = {'x': 'xx', '名': '五兵'}
    return JsonResponse(name_dict)

def edit_favorites(request):
    if request.is_ajax():
        message = "Yes, AJAX!"
    else:
        message = "Not Ajax"
    return HttpResponse(message)