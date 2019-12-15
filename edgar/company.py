import requests
from lxml import html, etree

BASE_URL = "https://www.sec.gov"

class Company():

    def __init__(self, name, cik):
        self.name = name
        self.cik = cik
        self.url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}"
        self._get_company_info()

    def _get_company_info(self):
        page = html.fromstring(requests.get(self.url).content)
        companyInfo = page.xpath("//div[@class='companyInfo']")[0]
        indentInfo = companyInfo.getchildren()[1]
        self.sic = indentInfo.getchildren()[1].text if len(indentInfo.getchildren()) > 2 else ""
        self.us_state = indentInfo.getchildren()[3].text if len(indentInfo.getchildren()) > 4 else ""

    def _get_filings_url(self, filing_type="", prior_to="", ownership="include", no_of_entries=100):
        url = self.url + "&type=" + filing_type + "&dateb=" + prior_to + "&owner=" +  ownership + "&count=" + str(no_of_entries)
        return url

    def get_all_filings(self, filing_type="", prior_to="", ownership="include", no_of_entries=100):
      url = self._get_filings_url(filing_type, prior_to, ownership, no_of_entries)
      page = requests.get(url)
      return html.fromstring(page.content)

    def _group_document_type(self, tree, document_type):
      result = []
      grouped = []
      for i, elem in enumerate(tree.xpath('//*[@id="seriesDiv"]/table/tr')):
        if i == 0:
          continue
        url = elem.xpath("td")[1].getchildren()[0].attrib["href"]
        grouped.append(url)
        if elem.xpath("td")[0].text == document_type:
          result.append(grouped)
          grouped = []
      return result

    def get_document_type_from_10K(self, document_type, no_of_documents=1):
      tree = self.get_all_filings(filing_type="10-K")
      url_groups = self._group_document_type(tree, "10-K")[:no_of_documents]
      result = []
      for url_group in url_groups:
        for url in url_group:
          url = BASE_URL + url
          content_page = get_request(url)
          table = content_page.find_class("tableFile")[0]
          for row in table.getchildren():
            if document_type in row.getchildren()[3].text:
              href = row.getchildren()[2].getchildren()[0].attrib["href"]
              href = BASE_URL + href
              doc = get_request(href)
              result.append(doc)
      return result

    def get_data_files_from_10K(self, document_type, no_of_documents=1, isxml=False):
      tree = self.get_all_filings(filing_type="10-K")
      url_groups = self._group_document_type(tree, "10-K")[:no_of_documents]
      result = []
      for url_group in url_groups:
        for url in url_group:
          url = BASE_URL + url
          content_page = get_request(url)
          tableFile = content_page.find_class("tableFile")
          if len(tableFile) < 2:
            continue
          table = tableFile[1]
          for row in table.getchildren():
            if document_type in row.getchildren()[3].text:
              href = row.getchildren()[2].getchildren()[0].attrib["href"]
              href = BASE_URL + href
              doc = get_request(href, isxml=isxml)
              result.append(doc)
      return result

    def get_10Ks(self, no_of_documents=1):
      tree = self.get_all_filings(filing_type="10-K")
      elems = tree.xpath('//*[@id="documentsbutton"]')[:no_of_documents]
      result = []
      for elem in elems:
          url = BASE_URL + elem.attrib["href"]
          content_page = get_request(url)
          table = content_page.find_class("tableFile")[0]
          last_row = table.getchildren()[-1]
          href = last_row.getchildren()[2].getchildren()[0].attrib["href"]
          href = BASE_URL + href
          doc = get_request(href)
          result.append(doc)
      return result

    def get_10K(self):
      return self.get_10Ks(no_of_documents=1)[0]


def get_request(href, isxml=False):
    page = requests.get(href)
    if isxml:
      return etree.fromstring(page.content)
    else:
      return html.fromstring(page.content)

def get_documents(tree, no_of_documents=1):
    BASE_URL = "https://www.sec.gov"
    elems = tree.xpath('//*[@id="documentsbutton"]')[:no_of_documents]
    result = []
    for elem in elems:
        url = BASE_URL + elem.attrib["href"]
        content_page = get_request(url)
        url = BASE_URL + content_page.xpath('//*[@id="formDiv"]/div/table/tr[2]/td[3]/a')[0].attrib["href"]
        filing = get_request(url)
        result.append(filing)

    if len(result) == 1:
        return result[0]
    return result

def get_CIK_from_company(company_name):
    tree = get_request("https://www.sec.gov/cgi-bin/browse-edgar?company=" + company_name)
    CIKList = tree.xpath('//*[@id="seriesDiv"]/table/tr[*]/td[1]/a/text()')
    names_list = []
    for elem in tree.xpath('//*[@id="seriesDiv"]/table/tr[*]/td[2]'):
        names_list.append(elem.text_content())
    return list(zip(CIKList, namesList))
