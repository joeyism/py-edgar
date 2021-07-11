# EDGAR
A small library to access files from SEC's edgar.

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

To avoid pull of all company data from sec.gov on Edgar initialization, pass in a local path to the data

``` python
from edgar import Edgar
edgar = Edgar("/path/to/cik-lookup-data.txt")
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
```python
Company(name, cik, timeout=10)
```
* name (company name)
* cik (company CIK number)
* timeout (optional) (default: 10)

#### Methods

`get_filings_url(self, filing_type="", prior_to="", ownership="include", no_of_entries=100) -> str`

Returns a url to fetch filings data
* filing_type: The type of document you want. i.e. 10-K, S-8, 8-K. If not specified, it'll return all documents
* prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
* ownership: defaults to include. Options are include, exclude, only.
* no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.


`get_all_filings(self, filing_type="", prior_to="", ownership="include", no_of_entries=100) -> lxml.html.HtmlElement`

Returns the HTML in the form of [lxml.html](http://lxml.de/lxmlhtml.html)
* filing_type: The type of document you want. i.e. 10-K, S-8, 8-K. If not specified, it'll return all documents
* prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
* ownership: defaults to include. Options are include, exclude, only.
* no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.


`get_10Ks(self, no_of_documents=1, as_documents=False) -> List[lxml.html.HtmlElement]`

Returns the HTML in the form of [lxml.html](http://lxml.de/lxmlhtml.html) of concatenation of all the documents in the 10-K
* no_of_documents (default: 1): numer of documents to be retrieved
* When `as_documents` is set to `True`, it returns `-> List[edgar.document.Documents]` a list of [Documents](#documents)


`get_document_type_from_10K(self, document_type, no_of_documents=1) -> List[lxml.html.HtmlElement]`

Returns the HTML in the form of [lxml.html](http://lxml.de/lxmlhtml.html) of the document within 10-K
* document_type: Tye type of document you want, i.e. 10-K, EX-3.2
* no_of_documents (default: 1): numer of documents to be retrieved


`get_data_files_from_10K(self, document_type, no_of_documents=1, isxml=False) -> List[lxml.html.HtmlElement]`

Returns the HTML in the form of [lxml.html](http://lxml.de/lxmlhtml.html) of the data file within 10-K
* document_type: Tye type of document you want, i.e. EX-101.INS
* no_of_documents (default: 1): numer of documents to be retrieved
* isxml (default: False): by default, things aren't case sensitive and is parsed with `html` in `lxml. If this is True, then it is parsed with `etree` which is case sensitive

#### Class Method

`get_documents(self, tree: lxml.html.Htmlelement, no_of_documents=1, debug=False, as_documents=False) -> List[lxml.html.HtmlElement]` Returns a list of strings, each string contains the body of the specified document from input

* tree: lxml.html form that is returned from Company.getAllFilings
* no_of_documents: number of document returned. If it is 1, the returned result is just one string, instead of a list of strings. Defaults to 1.
* debug (default: **False**): if **True**, displays the URL and form
* When `as_documents` is set to `True`, it returns `-> List[edgar.document.Documents]` a list of [Documents](#documents)



### Edgar
Gets all companies from EDGAR

`get_cik_by_company_name(company_name: str) -> str`: Returns the CIK if given the exact name or the company

`get_company_name_by_cik(cik: str) -> str`: Returns the company name if given the CIK (with the `000`s) 

`find_company_name(words: str) -> List[str]`: Returns a list of company names by exact word matching

`match_company_by_company_name(self, name, top=5) -> List[Dict[str, Any]]`: Returns a list of dictionarys, with company names, CIK, and their fuzzy match score
* `top (default: 5)` returns the top number of fuzzy matches. If set to `None`, it'll return the whole list (which is a lot)

### XBRL
Parses data from XBRL
#### Properties
`relevant_children`
* get children that are not `context`
`relevant_children_parsed`
* get children that are not `context`, `unit`, `schemaRef`
* cleans tags

### Documents
Filing and Documents Details for the SEC EDGAR Form (such as 10-K)

```python
Documents(url, timeout=10)
```
#### Properties
`url: str`: URL of the document

`content: dict`: Dictionary of meta data of the document

`content['Filing Date']: str`: Document filing date

`content['Accepted']: str`: Document accepted datetime

`content['Period of Report']: str`: The date period that the document is for

`element: lxml.html.HtmlElement`: The HTML element for the Document (from the url) so it can be further parsed


## Contribution
<a href="https://www.buymeacoffee.com/joeyism" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
