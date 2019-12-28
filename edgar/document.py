import requests
from lxml import html

class Document:

  def __init__(self, url, timeout=10):
    self.url = url
    self.text = requests.get(self.url, timeout=timeout).content

class Documents:

  def __get_text_from_list__(self, arr):
    return [val.text_content() for val in arr]

  def __init__(self, url, timeout=10):
    self.url = url
    page = requests.get(self.url, timeout=timeout)
    tree = html.fromstring(page.content)
    content = tree.find_class("formContent")[0]
    info_head = self.__get_text_from_list__(content.find_class("infoHead"))
    info = self.__get_text_from_list__(content.find_class("info"))
    self.content = dict(zip(info_head, info))
