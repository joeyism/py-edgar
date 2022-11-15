# -*- coding: UTF-8 -*-
import requests
from lxml import html

# The required SEC EDGAR request header
SEC_HEADERS = {
    'user-agent': 'Edgar oit@sec.gov',
    'accept-encoding':  'gzip, deflate',
    'host':  'www.sec.gov',
    'referer': 'https://www.sec.gov/', 
    'cache-control': 'no-cache', 
    #'connection': 'close'
    #'connection': 'keep-alive'
}
# Set new default requests header
headers = SEC_HEADERS

class Document:

  def __init__(self, url, timeout=10):
    self.url = url
    self.text = requests.get(self.url, timeout=timeout, headers=SEC_HEADERS).content

class Documents(str):

  def __get_text_from_list__(self, arr):
    return [val.text_content() for val in arr]

  def __init__(self, url, timeout=10):
    self.url = url
    page = requests.get(self.url, timeout=timeout, headers=SEC_HEADERS)
    tree = html.fromstring(page.content)
    content = tree.find_class("formContent")[0]
    info_head = self.__get_text_from_list__(content.find_class("infoHead"))
    info = self.__get_text_from_list__(content.find_class("info"))
    self.content = dict(zip(info_head, info))
    self.element = html.fromstring(requests.get(self.url, timeout=timeout, headers=SEC_HEADERS).content)

  def __repr__(self):
    return str(self.__dict__)

  def __str__(self):
    return str(self.__dict__)
