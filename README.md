# EDGAR

A small library to access files from SEC's edgar.

## Installation

>   pip install edgar

## Example
To get a company's latest 5 10-Ks, run

```
    from edgar import *
    com = edgar.Company("Oracle Corp", "0001341439")
    tree = com.getAllFilings(filingType = "10-K")
    docs = edgar.getDocuments(tree, noOfDocuments=5)

```

## API

### Company
The **Company** class has two fields:

* name (company name)
* cik (company CIK number)

#### getFilingsUrl
Returns a url to fetch filings data

**Input**
* filingType: The type of document you want. i.e. 10-K, S-8, 8-K. If not specified, it'll return all documents
* priorTo: Time prior which documents are to be retrieved. If not specified, it'll return all documents
* ownership: defaults to include. Options are include, exclude, only.
* noOfEntries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.

#### getAllFilings
Returns the HTML in the form of [lxml.html](http://lxml.de/lxmlhtml.html)

**Input**
* filingType: The type of document you want. i.e. 10-K, S-8, 8-K. If not specified, it'll return all documents
* priorTo: Time prior which documents are to be retrieved. If not specified, it'll return all documents
* ownership: defaults to include. Options are include, exclude, only.
* noOfEntries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.

### getDocuments
Returns a list of strings, each string contains the body of the specified document from input

**Input**
* tree: lxml.html form that is returned from Company.getAllFilings
* noOfDocuments: number of document returned. If it is 1, the returned result is just one string, instead of a list of strings. Defaults to 1.


## Release Notes
**0.1**
* First release
