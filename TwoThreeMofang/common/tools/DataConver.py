#coding:utf-8
__author__ = 'similarface'
def StringToInt(str):
    try:
        return int(str)
    except Exception,e:
        return int(1)