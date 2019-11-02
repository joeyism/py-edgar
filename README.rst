
EDGAR
=====

A small library to access files from SEC's edgar.

Installation
------------

..

     pip install edgar


Example
-------

To get a company's latest 5 10-Ks, run

.. code-block:: python

   from edgar import Company
   company = Company("Oracle Corp", "0001341439")
   tree = company.get_all_filings(filing_type = "10-K")
   docs = edgar.get_documents(tree, no_of_documents=5)

or

.. code-block:: python

   from edgar import Company, TXTML

   company = Company("INTERNATIONAL BUSINESS MACHINES CORP", "0000051143")
   doc = company.get_10K()
   text = TXTML.parse_full_10K(doc)

To get all companies and find a specific one, run

.. code-block:: python

   from edgar import Edgar
   edgar = Edgar()
   possible_companies = edgar.find_company_name("Cisco System")

API
---

Company
^^^^^^^

The **Company** class has two fields:


* name (company name)
* cik (company CIK number)

get_filings_url
"""""""""""""""

Returns a url to fetch filings data


* **Input**

  * filing_type: The type of document you want. i.e. 10-K, S-8, 8-K. If not specified, it'll return all documents
  * prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
  * ownership: defaults to include. Options are include, exclude, only.
  * no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.

get_all_filings
"""""""""""""""

Returns the HTML in the form of `lxml.html <http://lxml.de/lxmlhtml.html>`_


* **Input**

  * filing_type: The type of document you want. i.e. 10-K, S-8, 8-K. If not specified, it'll return all documents
  * prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
  * ownership: defaults to include. Options are include, exclude, only.
  * no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.

Edgar
^^^^^

Gets all companies from EDGAR

get_cik_by_company_name
"""""""""""""""""""""""


* **Input**

  * name: name of the company

get_company_name_by_cik
"""""""""""""""""""""""


* **Input**

  * cik: cik of the company

find_company_name
"""""""""""""""""


* **Input**

  * words: input words to search the company

get_documents
^^^^^^^^^^^^^

Returns a list of strings, each string contains the body of the specified document from input


* **Input**

  * tree: lxml.html form that is returned from Company.getAllFilings
  * no_of_documents: number of document returned. If it is 1, the returned result is just one string, instead of a list of strings. Defaults to 1.
