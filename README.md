# EDGAR
A small library to access files from SEC's edgar.

## Contribution
<a href="https://www.buymeacoffee.com/joeyism" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## Installation

>   pip install edgar

## Example
To get a company's latest 5 10-Ks, run

``` python
from edgar import Company
company = Company("Oracle Corp", "0001341439")
tree = company.get_all_filings(filing_type = "10-K")
docs = Company.get_documents(tree, no_of_documents=5)
```
or
```python
from edgar import Company, TXTML

company = Company("INTERNATIONAL BUSINESS MACHINES CORP", "0000051143")
doc = company.get_10K()
text = TXTML.parse_full_10K(doc)
```

To get all companies and find a specific one, run

``` python
from edgar import Edgar
edgar = Edgar()
possible_companies = edgar.find_company_name("Cisco System")
```

To get XBRL data, run
```python
from edgar import Company, XBRL, XBRLElement

company = Company("Oracle Corp", "0001341439")
results = company.get_data_files_from_10K("EX-101.INS", isxml=True)
xbrl = XBRL(results[0])
XBRLElement(xbrl.relevant_children_parsed[15]).to_dict() // returns a dictionary of name, value, and schemaRef
```

## API

### Company
The **Company** class has two fields:

* name (company name)
* cik (company CIK number)
* timeout (optional) (default: 10)

##### get_filings_url
Returns a url to fetch filings data
* **Input**
    * filing_type: The type of document you want. i.e. 10-K, S-8, 8-K. If not specified, it'll return all documents
    * prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
    * ownership: defaults to include. Options are include, exclude, only.
    * no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.

##### get_all_filings
Returns the HTML in the form of [lxml.html](http://lxml.de/lxmlhtml.html)
* **Input**
    * filing_type: The type of document you want. i.e. 10-K, S-8, 8-K. If not specified, it'll return all documents
    * prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
    * ownership: defaults to include. Options are include, exclude, only.
    * no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.

##### get_10Ks
Returns the HTML in the form of [lxml.html](http://lxml.de/lxmlhtml.html) of concatenation of all the documents in the 10-K
* **Input**
    * no_of_documents (default: 1): numer of documents to be retrieved

##### get_document_type_from_10K
Returns the HTML in the form of [lxml.html](http://lxml.de/lxmlhtml.html) of the document within 10-K
* **Input**
    * document_type: Tye type of document you want, i.e. 10-K, EX-3.2
    * no_of_documents (default: 1): numer of documents to be retrieved

##### get_data_files_from_10K
Returns the HTML in the form of [lxml.html](http://lxml.de/lxmlhtml.html) of the data file within 10-K
* **Input**
    * document_type: Tye type of document you want, i.e. EX-101.INS
    * no_of_documents (default: 1): numer of documents to be retrieved
    * isxml (default: False): by default, things aren't case sensitive and is parsed with `html` in `lxml. If this is True, then it is parsed with `etree` which is case sensitive

##### get_documents (class method)
Returns a list of strings, each string contains the body of the specified document from input
* **Input**
    * tree: lxml.html form that is returned from Company.getAllFilings
    * no_of_documents: number of document returned. If it is 1, the returned result is just one string, instead of a list of strings. Defaults to 1.
    * debug (default: **False**): if **True**, displays the URL and form


### Edgar
Gets all companies from EDGAR
##### get_cik_by_company_name
* **Input**
    * name: name of the company

##### get_company_name_by_cik
* **Input**
    * cik: cik of the company

##### find_company_name
* **Input**
    * words: input words to search the company

### XBRL
Parses data from XBRL
* `relevant_children`
    * get children that are not `context`
* `relevant_children_parsed`
    * get children that are not `context`, `unit`, `schemaRef`
    * cleans tags

