# coding:utf-8
import hashlib

def getMd5(ac):
    salt='/hferjberg'
    value=str(ac)+salt
    m5=hashlib.md5()
    m5.update(value)
    return m5.hexdigest()