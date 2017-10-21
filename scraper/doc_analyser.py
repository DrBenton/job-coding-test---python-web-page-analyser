
from typing import Callable, NamedTuple
from bs4 import BeautifulSoup


class DocSummary(NamedTuple):
    page_title: str


class DocAnalyser:

    def __init__(self, doc_fetcher: Callable):
        self.doc_fetcher = doc_fetcher

    def analyse(self, url: str) -> DocSummary:
        html_doc: str = self.doc_fetcher(url)
        self._soup = BeautifulSoup(html_doc, 'html.parser')

        doc_summary_dict = {
            'page_title': self._soup.title.string
        }

        return DocSummary(**doc_summary_dict)

