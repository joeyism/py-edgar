from lxml import html
import requests

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
        
def test():
    com = Company("Oracle Corp", "0001341439")
    tree = com.getAllFilings(filingType = "10-K")
    return getDocuments(tree)
