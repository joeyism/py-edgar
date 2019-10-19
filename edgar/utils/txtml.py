
class TXTML:

  @classmethod
  def _clean_text_(cls, text):
    return text.replace('\n', '')

  @classmethod
  def getDocumentType(cls, document):
    return document.getchildren()[0].text

  @classmethod
  def getHTMLFromDocument(cls, document):
    properties = {}

    while document.tag != 'text':
      properties[document.tag] = cls._clean_text_(document.text)
      document = document.getchildren()[0]

    return document, properties

  @classmethod
  def parseFull10K(cls, doc):
    text = ""
    for child in doc.getchildren():
      if child.tag == 'sec-header':
          continue
      html, properties = TXTML.getHTMLFromDocument(child)
      if properties['type'] == '10-K':
        text = text + html.text_content()
    return text
