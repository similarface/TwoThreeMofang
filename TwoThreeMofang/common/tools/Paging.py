#coding:utf-8
__author__ = 'similarface'
class Paging:
    def __init__(self,count,page,per_item=5,viewpagenum=13):
        #总记录数
        self.Count=count
        #点击的页码
        self.Page=page
        #一页的记录个数
        self.PerItem=per_item
        #可见页的个数
        self.ViewPageNum=viewpagenum
    @property
    def start(self):
        '''
        开始地址
        :return:
        '''
        return (self.Page-1) * self.PerItem
    @property
    def end(self):
        '''
        结束地址
        :return:
        '''
        return self.Page*self.PerItem
    @property
    def all_page_count(self):
        '''
        获取总的页数
        :return:
        '''
        temp=divmod(self.Count,self.PerItem)
        #计算总页数
        if temp[1]==0:
            #能整除
            all_page_count=temp[0]
        else:
            #不能整除
            all_page_count=temp[0]+1
        return all_page_count

    def PageBeginEnd(self):
        '''
        分页显示页码开始位置和结束位置
        :return:
        '''
        mesoposition=divmod(self.ViewPageNum,2)[0]
        begin=self.Page-mesoposition-1
        end=self.Page+mesoposition
        #页面总数小于可显示的页面 应该全显示
        if self.all_page_count<self.ViewPageNum:
            begin=0
            end=self.all_page_count
        else:
            #页面总数大于可显示页面
            #点击页面在中位数左边
            if self.Page<=mesoposition:
                begin=0
                end=self.ViewPageNum
            else:
                #点击页面在中位数超过总页数
                if self.Page+mesoposition>self.all_page_count:
                    begin=self.Page-mesoposition
                    end=self.all_page_count
                else:
                    begin=self.Page-mesoposition-1
                    end = self.Page+mesoposition
        return begin,end

    def PageContent(self,hrefflag):
        '''
        返回分页的内容
        hrefflag like "/app01/index/"
        :return:
        '''
        #返回的html标签
        page_html=[]
        #分页首页
        first_html="<a href='"+hrefflag+"%d'>首页</a>" %(1,)
        page_html.append(first_html)
        if self.Page<=1:
            prv_html="<a href='#'>上一页</a>"
        else:
            prv_html="<a href='"+hrefflag+"%d'>上一页</a>" %(self.Page-1,)
        page_html.append(prv_html)
        #获取开始结束页面
        begin,end=self.PageBeginEnd()
        for i in range(begin,end):
            #当前页面
            if self.Page ==i+1:
                a_html="<a style='color:red' href='"+hrefflag+"%d'>%d</a>"%(i+1,i+1)
            else:
                #其余页
                a_html="<a href='"+hrefflag+"%d'>%d</a>"%(i+1,i+1)
            page_html.append(a_html)
        #下一页不能超过最大页数
        if self.Page==self.all_page_count:
            next_html="<a href='#'>下一页</a>"
        else:
            next_html="<a href='"+hrefflag+"%d'>下一页</a>" %(self.Page+1,)
        page_html.append(next_html)
        end_html="<a href='"+hrefflag+"%d'>尾页</a>" % (self.all_page_count,)
        page_html.append(end_html)
        #html标签不转义
        return page_html

if __name__ =="__main__":
    count=97
    page=1
    paging=Paging(count,page,5,3)
    x,y=paging.PageBeginEnd()
    print(x,y)