from lxml import html
import requests

BASE_URL = "https://www.sec.gov"

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
        

class Filing:
    main_xpath = '//*[@id="formDiv"]/div/table/tr[2]/td[3]/a'

    def __init__(self, elem):
        self.url = BASE_URL + elem.attrib["href"]
        self.elem = getRequest(self.url)

    @property
    def text_content(self):
        return self._get_text_content_by_link_xpath(self.main_xpath)

    @property
    def content(self):
        return self._get_html_by_link_xpath(self.main_xpath)

    @property
    def filing_date(self):
        return self._get_filing_info('Filing Date')

    @property
    def accepted(self):
        return self._get_filing_info('Accepted')

    @property
    def period_of_report(self):
        return self._get_filing_info('Period of Report')

    def sub_filing(self, sub_document, as_html = False):
        xpath = '//*[@id="formDiv"]/div/table/tr[td[4]/text()="{sub_document}"]/td[3]/a'.format(
            sub_document=sub_document
        )
        if as_html:
            return self._get_html_by_link_xpath(xpath)
        return self._get_text_content_by_link_xpath(xpath)

    def _get_content_by_link_xpath(self, xpath):
        url = BASE_URL + self.elem.xpath(xpath)[0].attrib["href"]
        content = getRequest(url)
        return content

    def _get_text_content_by_link_xpath(self, xpath):
        content = self._get_content_by_link_xpath(xpath)
        return content.body.text_content()

    def _get_html_by_link_xpath(self, xpath):
        content = self._get_content_by_link_xpath(xpath)
        return html.tostring(content).decode('utf8')

    def _get_filing_info(self, info_str):
        info_xpath = '//*[@id="formDiv"]//div[@class="formGrouping"]/div[preceding-sibling::div[1]/' \
                     'text()="{info_str}"]/text()'.format(info_str=info_str)
        return self.elem.xpath(info_xpath)[0]


def getRequest(href):
    page = requests.get(href)
    return html.fromstring(page.content)


def getDocuments(tree, sub_document=None, noOfDocuments=1, as_html=False):
    filings = getFilings(tree, noOfDocuments=noOfDocuments)
    if sub_document is None:
        if as_html:
            attr = 'content'
        else:
            attr = 'text_content'
        result = [getattr(filing, attr) for filing in filings]
    else:
        result = [filing.sub_filing(sub_document, as_html=as_html) for filing in filings]

    if len(result) == 1:
        return result[0]
    return result


def getFilings(tree, noOfDocuments=1):
    elems = tree.xpath('//*[@id="documentsbutton"]')[:noOfDocuments]
    return [Filing(elem) for elem in elems]


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
