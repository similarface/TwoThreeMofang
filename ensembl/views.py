#coding:utf-8
from django.shortcuts import render,render_to_response,redirect,HttpResponseRedirect,HttpResponse
from TwoThreeMofang.form import UploadFileForm
# Create your views here.
from TwoThreeMofang.common.tools.Paging import Paging
from TwoThreeMofang.common.tools.DataConver import StringToInt
import models
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.template import RequestContext

def index(request):
    return  render_to_response('ensembl/index2.html')

def Population(request,*args,**kwargs):
    #总记录数
    if request.method=='POST':
        lrsid=request.POST.get('keyword')
        print lrsid
        lrsid=str(lrsid).strip()
        if lrsid!="" and lrsid!=None:
            lrsid=lrsid.replace("，",",").replace(" ",'').replace("\t","")
            rsids=lrsid.split(',')
            request.session['rsidlist']=rsids
            request.session['rsidstr']=lrsid
        else:
            request.session['rsidlist']=None
            request.session['rsidstr']=None
    page=kwargs.get('page')
    page=StringToInt(page)
    rsids=request.session.get('rsidlist')
    #如果输入框有关键字请求进入
    if rsids!=None and rsids!='' and 'rsids' in request.path:
        #获取记录数目
        count=models.PopulationGenetics.objects.filter(rsid__in=rsids).count()
        #创建分页对象
        paging=Paging(count,page,10,8)
        #关键字筛选
        result=models.PopulationGenetics.objects.filter(rsid__in=rsids)[paging.start:paging.end]
        #连接地址介入
        urlline='/ensembl/Population/rsids/'
        #分页链接代码
        page_html=paging.PageContent(urlline)
    else:
        #输入框没有关键字请求进入
        #获取记录数目
        request.session['rsidlist']=None
        request.session['rsidstr']=None
        count=models.PopulationGenetics.objects.all().count()
        paging=Paging(count,page,10,8)
        result=models.PopulationGenetics.objects.all()[paging.start:paging.end]
        #分页链接代码
        page_html=paging.PageContent("/ensembl/Population/")
    #分页的连接转码
    page=mark_safe(' '.join(page_html))
    #获取请求的关键字
    lrsid=request.session.get('rsidstr')
    checkboxContext=models.ModelInfo.objects.filter(TABLE_NAME='ensembl_populationgenetics')
    ret={'data':result,'checkselect':checkboxContext,'count':count,'page':page,'rsidstr':lrsid}
    return render_to_response('ensembl/populationdata.html',ret)


def SelfPopulation(request,*args,**kwargs):
    print('------')
    #总记录数
    if request.method=='POST':
        lrsid=request.POST.get('keyword').encode('utf-8')
        lrsid=str(lrsid).strip()
        print(lrsid)
        if lrsid!="" and lrsid!=None:
            lrsid=lrsid.replace("，",",").replace(" ",'').replace("\t","")
            rsids=lrsid.split(',')
            request.session['rsidlist']=rsids
            request.session['rsidstr']=lrsid
        else:
            request.session['rsidlist']=None
            request.session['rsidstr']=None
    page=kwargs.get('page')
    page=StringToInt(page)
    rsids=request.session.get('rsidlist')
    #如果输入框有关键字请求进入
    if rsids!=None and rsids!='' and 'rsids' in request.path:
        #获取记录数目
        count=models.SelfPopulationGenetics.objects.filter(Q(rsid__in=rsids) | Q(pos__in=rsids)).count()
        #创建分页对象
        paging=Paging(count,page,10,8)
        #关键字筛选
        result=models.SelfPopulationGenetics.objects.filter(Q(rsid__in=rsids) | Q(pos__in=rsids))[paging.start:paging.end]
        #连接地址介入
        urlline='/ensembl/Population/rsids/'
        #分页链接代码
        page_html=paging.PageContent(urlline)
    else:
        #输入框没有关键字请求进入
        #获取记录数目
        request.session['rsidlist']=None
        request.session['rsidstr']=None
        count=models.SelfPopulationGenetics.objects.all().count()
        paging=Paging(count,page,10,8)
        result=models.SelfPopulationGenetics.objects.all()[paging.start:paging.end]
        #分页链接代码
        page_html=paging.PageContent("/ensembl/Population/")
    #分页的连接转码
    page=mark_safe(' '.join(page_html))
    #获取请求的关键字
    lrsid=request.session.get('rsidstr')
    checkboxContext=models.ModelInfo.objects.filter(TABLE_NAME='mofang_populationgenetics')
    ret={'data':result,'checkselect':checkboxContext,'count':count,'page':page,'rsidstr':lrsid}
    return render_to_response('ensembl/populationdata.html',ret)










'''
上传文件查询
# '''
# def PopulationRsids(request,*args,**kwargs):
#     pass
#
# def getInConditionFromFile(f):
#     incondition=''
#     for chunk in f.chunks():
#         incondition=incondition+chunk
#     temp=incondition.split('\n')
#     inconditions="'"
#     rsidlist=[]
#     for item in temp:
#         print(item)
#         rsidlist.append(item.strip())
#         inconditions=inconditions+item.strip()+"','"
#     return rsidlist,inconditions[0:-2]
#
#
# def PopulationRsids(request,*args,**kwargs):
#     print('-----------PopulationRsids-------------')
#     global rsidslist
#     global rsidsStr
#     #获取页面
#     page=kwargs.get('page')
#     page=StringToInt(page)
#     if request.method=='POST':
#         form = UploadFileForm(request.POST,request.FILES)
#         #表单是否有效
#         if form.is_valid():
#             #根据上传的文件生成rsid的list和strs
#             rsidslist,rsidsStr=getInConditionFromFile(request.FILES['file'])
#         print('rsidsStr:'+rsidsStr)
#     print('rsidsStr:'+rsidsStr)
#     if rsidsStr!=None and rsidsStr!='':
#         count=models.PopulationGenetics.objects.filter(rsid__in=rsidslist).count()
#         print(count)
#         paging=Paging(count,page,10,8)
#         #SQL='SELECT * FROM ensembl_populationgenetics WHERE rsid in (%s) LIMIT '+str(paging.start)+","+str(paging.end)
#         SQL="SELECT * FROM ensembl_populationgenetics WHERE rsid in ('rs3815865','rs229527') LIMIT "+str(paging.start)+","+str(paging.end)
#
#         #result = models.PopulationGenetics.objects.raw(SQL,[rsidsStr])
#
#         #SQL='SELECT * FROM ensembl_populationgenetics LIMIT '+str(paging.start)+","+str(paging.end)
#         result = models.PopulationGenetics.objects.raw(SQL)
#
#         urlline='/ensembl/Population/rsids/'
#         page_html=paging.PageContent(urlline)
#     else:
#         print('执行了')
#         count=models.PopulationGenetics.objects.all().count()
#         paging=Paging(count,page,10,8)
#         SQL='SELECT * FROM ensembl_populationgenetics LIMIT '+str(paging.start)+","+str(paging.end)
#         result = models.PopulationGenetics.objects.raw(SQL)
#         page_html=paging.PageContent("/ensembl/Population/")
#     page=mark_safe(' '.join(page_html))
#     ret={'data':result,'count':count,'page':page}
#     return render_to_response('ensembl/populationdata.html',ret)
#
#
#
#
#
#
#
#
#



# def Population(request,page):
#     #总记录数
#     count=models.PopulationGenetics.objects.all().count()
#     page=StringToInt(page)
#     paging=Paging(count,page,15,8)
#     SQL='SELECT * FROM ensembl_populationgenetics LIMIT '+str(paging.start)+","+str(paging.end)
#     print(SQL,'norsid')
#     result = models.PopulationGenetics.objects.raw(SQL)
#     #result= models.PopulationGenetics.objects.all()[paging.start:paging.end]
#     page_html=paging.PageContent("/ensembl/Population/")
#     page=mark_safe(' '.join(page_html))
#     ret={'data':result,'count':count,'page':page}
#     return render_to_response('ensembl/populationdata.html',ret)
#


# def Population(request,page):
#     #总记录数
#     count=models.PopulationGenetics.objects.all().count()
#     page=StringToInt(page)
#     paging=Paging(count,page,15,8)
#     SQL='SELECT * FROM ensembl_populationgenetics LIMIT '+str(paging.start)+","+str(paging.end)
#     print(SQL,'norsid')
#     result = models.PopulationGenetics.objects.raw(SQL)
#     #result= models.PopulationGenetics.objects.all()[paging.start:paging.end]
#     page_html=paging.PageContent("/ensembl/Population/")
#     page=mark_safe(' '.join(page_html))
#     ret={'data':result,'count':count,'page':page}
#     return render_to_response('ensembl/populationdata.html',ret)
#
# def PopulationRsid(request,lrsid,page=1):
#     print("lrsid:"+lrsid,page)
#     #总记录数
#     count=models.PopulationGenetics.objects.filter(rsid=lrsid).count()
#     page=StringToInt(page)
#     paging=Paging(count,page,15,8)
#     SQL='select * from ensembl_populationgenetics where rsid=%s LIMIT '+str(paging.start)+","+str(paging.end)
#     print(SQL)
#     result = models.PopulationGenetics.objects.raw(SQL,[lrsid])
#     urlline='/ensembl/Population/'+lrsid.encode('utf-8')+'/'
#     page_html=paging.PageContent(urlline)
#     #page_html=paging.PageContent("/ensembl/Population/"+lrsid+"/")
#     page=mark_safe(' '.join(page_html))
#     ret={'data':result,'count':count,'page':page}
#     return render_to_response('ensembl/populationdata.html',ret,context_instance=RequestContext(request))
#
# def PopulationPost(request,page=1):
#     if request.method=='POST':
#         lrsid=request.POST.get('rsid')
#         if lrsid==None or lrsid=='':
#             return redirect('/ensembl/Population/')
#     print("lrsid1:"+lrsid,page)
#     #总记录数
#     count=models.PopulationGenetics.objects.filter(rsid=lrsid).count()
#     page=StringToInt(page)
#     paging=Paging(count,page,15,8)
#     SQL='select * from ensembl_populationgenetics where rsid=%s LIMIT '+str(paging.start)+","+str(paging.end)
#     print(SQL)
#     result = models.PopulationGenetics.objects.raw(SQL,[lrsid])
#     urlline='/ensembl/Population/'+lrsid.encode('utf-8')+'/'
#     page_html=paging.PageContent(urlline)
#     #page_html=paging.PageContent("/ensembl/Population/"+lrsid+"/")
#     page=mark_safe(' '.join(page_html))
#     ret={'data':result,'count':count,'page':page}
#     return render_to_response('ensembl/populationdata.html',ret,context_instance=RequestContext(request))


        #param= ("%s," * rsids.__len__())[0:-1]
        # SQL="select * from ensembl_populationgenetics where rsid in ("+param+") LIMIT "+str(paging.start)+","+str(10)
        # result = models.PopulationGenetics.objects.raw(SQL,rsids)
    #SQL="select * from ensembl_populationgenetics where rsid=%s LIMIT "+str(paging.start)+","+str(10)

        # SQL='SELECT * FROM ensembl_populationgenetics LIMIT '+str(paging.start)+","+str(10)
        # result = models.PopulationGenetics.objects.raw(SQL)