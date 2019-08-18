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


class Edgar():

    def __init__(self):
        all_companies_page = requests.get("https://www.sec.gov/Archives/edgar/cik-lookup-data.txt")
        all_companies_content = all_companies_page.content.decode("latin1")
        all_companies_array = all_companies_content.split("\n")
        del all_companies_array[-1]
        all_companies_array_rev = []
        for i, item in enumerate(all_companies_array):
            if item == "":
                continue
            item_arr = item.split(":")
            all_companies_array[i] = (item_arr[0], item_arr[1])
            all_companies_array_rev.append((item_arr[1], item_arr[0]))
        self.all_companies_dict = dict(all_companies_array)
        self.all_companies_dict_rev = dict(all_companies_array_rev)

    def getCikByCompanyName(self, name):
        return self.all_companies_dict[name]

    def getCompanyNameByCik(self, cik):
        return self.all_companies_dict_rev[cik]

    def findCompanyName(self, words):
        possibleCompanies = []
        words = words.lower()
        for company in self.all_companies_dict:
            if all(word in company.lower() for word in words.split(" ")):
                possibleCompanies.append(company)
        return possibleCompanies
        


def getRequest(href):
    page = requests.get(href)
    return html.fromstring(page.content)


def getDocuments(tree, sub_document=None, noOfDocuments=1):
    baseurl = "https://www.sec.gov"
    elems = tree.xpath('//*[@id="documentsbutton"]')[:noOfDocuments]
    result = []
    for elem in elems:
        url = baseurl + elem.attrib["href"]
        contentPage = getRequest(url)
        sub_doc_xpath = _get_sub_document_xpath(sub_document)
        url = baseurl + contentPage.xpath(sub_doc_xpath)[0].attrib["href"]
        filing = getRequest(url)
        result.append(filing.body.text_content())

    if len(result) == 1:
        return result[0]
    return result


def _get_sub_document_xpath(sub_document=None):
    if sub_document is None:
        return '//*[@id="formDiv"]/div/table/tr[2]/td[3]/a'

    return '//*[@id="formDiv"]/div/table/tr[td[4]/text()="{sub_document}"]/td[3]/a'.format(sub_document=sub_document)


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
