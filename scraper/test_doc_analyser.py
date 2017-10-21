
from typing import Callable
from scraper.doc_analyser import DocAnalyser


def test_parsing_title():
    html_doc = '<html><head><title>Hello Plum!</title></head><body>Once upon a time there were three little sisters</body></html>'

    sut = DocAnalyser(doc_fetcher_mock(html_doc))
    doc_summary = sut.analyse('http://dummy.com')
    assert doc_summary.page_title == 'Hello Plum!'


def doc_fetcher_mock(expected_fetched_doc: str) ->Callable:
    def mock(url: str) ->str:
        return expected_fetched_doc

    return mock
