from lxml import html
import requests

class Company():

    def __init__(self, name, cik):
        self.name = name
        self.cik = cik

    def getFilingsUrl(self, filingType="", priorTo="", ownership="include", noOfEntries=100):
        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + self.cik + "&type=" + filingType + "&dateb=" + priorTo + "&owner=" +  ownership + "&count=" + str(noOfEntries)
        return url

    def getAllFilings(self, filingType="", priorTo="", ownership="include", noOfEntries=100):
        page = requests.get(self.getFilingsUrl(filingType, priorTo, ownership, noOfEntries))
        return html.fromstring(page.content)


def getRequest(href):
    page = requests.get(href)
    return html.fromstring(page.content)

def getDocuments(tree, noOfDocuments=1):
    baseurl = "https://www.sec.gov"
    elems = tree.xpath('//*[@id="documentsbutton"]')[:noOfDocuments]
    result = []
    for elem in elems:
        url = baseurl + elem.attrib["href"]
        contentPage = getRequest(url)
        url = baseurl + contentPage.xpath('//*[@id="formDiv"]/div/table/tr[2]/td[3]/a')[0].attrib["href"]
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


def test():
    com = Company("Oracle Corp", "0001341439")
    tree = com.getAllFilings(filingType = "10-K")
    return getDocuments(tree)
