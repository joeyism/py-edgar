from lxml import html


def get_text_content(elem: html.HtmlElement) -> str:
    text_nodes = elem.xpath('.//text()')
    return ' '.join(node.strip() for node in text_nodes if node.strip())


def extract_text_with_spacing(element: html.HtmlElement) -> str:
    """
    Extracts text from an lxml.html.HtmlElement such that:
    - Text within <span> elements is concatenated together.
    - Text outside of <span> elements is separated by spaces.

    Parameters:
        element (lxml.html.HtmlElement): The HTML element to extract text from.

    Returns:
        str: The extracted text with appropriate spacing.
    """
    text_parts = []
    current_span_text = []

    for child in element.iter():
        if child.tag == 'span':
            # If it's a span, accumulate its text
            current_span_text.append(child.text or '')
        else:
            # If we encounter a non-span tag, flush current span text
            if current_span_text:
                text_parts.append(''.join(current_span_text).strip())
                current_span_text = []  # Reset for the next span

            # Add the text of non-span elements
            if child.text:
                text_parts.append(child.text.strip())

    # If there's any text left in the span, add it to the result
    if current_span_text:
        text_parts.append(''.join(current_span_text).strip())

    return ' '.join(text_parts).strip()
