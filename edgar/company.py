import requests
from lxml import html

BASE_URL = "https://www.sec.gov"

class Company():

    def __init__(self, name, cik):
        self.name = name
        self.cik = cik

    def _getFilingsUrl(self, filingType="", priorTo="", ownership="include", noOfEntries=100):
        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + self.cik + "&type=" + filingType + "&dateb=" + priorTo + "&owner=" +  ownership + "&count=" + str(noOfEntries)
        return url

    def getAllFilings(self, filingType="", priorTo="", ownership="include", noOfEntries=100):
        url = self._getFilingsUrl(filingType, priorTo, ownership, noOfEntries)
        page = requests.get(url)
        return html.fromstring(page.content)

    def get10Ks(self, noOfDocuments=1):
      tree = self.getAllFilings(filingType="10-K")
      elems = tree.xpath('//*[@id="documentsbutton"]')[:noOfDocuments]
      result = []
      for elem in elems:
          url = BASE_URL + elem.attrib["href"]
          contentPage = getRequest(url)
          table = contentPage.find_class("tableFile")[0]
          lastRow = table.getchildren()[-1]
          href = lastRow.getchildren()[2].getchildren()[0].attrib["href"]
          href = BASE_URL + href
          doc = getRequest(href)
          result.append(doc)
      return result

    def get10K(self):
      return self.get10Ks(noOfDocuments=1)[0]


def getRequest(href):
    page = requests.get(href)
    return html.fromstring(page.content)

def getDocuments(tree, noOfDocuments=1):
    BASE_URL = "https://www.sec.gov"
    elems = tree.xpath('//*[@id="documentsbutton"]')[:noOfDocuments]
    result = []
    for elem in elems:
        url = BASE_URL + elem.attrib["href"]
        contentPage = getRequest(url)
        url = BASE_URL + contentPage.xpath('//*[@id="formDiv"]/div/table/tr[2]/td[3]/a')[0].attrib["href"]
        filing = getRequest(url)
        result.append(filing.body.text_content())

    if len(result) == 1:
        return result[0]
    return result

def getCIKFromCompany(companyName):
    tree = getRequest("https://www.sec.gov/cgi-bin/browse-edgar?company=" + companyName)
    CIKList = tree.xpath('//*[@id="seriesDiv"]/table/tr[*]/td[1]/a/text()')
    namesList = []
    for elem in tree.xpath('//*[@id="seriesDiv"]/table/tr[*]/td[2]'):
        namesList.append(elem.text_content())
    return list(zip(CIKList, namesList))


