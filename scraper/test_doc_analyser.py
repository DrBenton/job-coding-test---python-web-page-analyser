
from typing import Callable
from scraper.doc_analyser import DocAnalyser


def test_parsing_title():
    html_doc = '<html><head><title>Hello Plum!</title></head><body>Once upon a time there were three little sisters</body></html>'

    sut = DocAnalyser(doc_fetcher_mock(html_doc))
    doc_summary = sut.analyse('http://dummy.com')
    assert doc_summary.page_title == 'Hello Plum!'


def test_parsing_meta():
    html_doc = """
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
        
            <link rel="prefetch" href="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js">
            
            <meta http-equiv="imagetoolbar" content="false">
        
            <meta property="og:type" content="website">
            <meta property="og:site_name" content="Python.org">
            <meta property="og:title" content="PEP 274 -- Dict Comprehensions">
            <meta property="og:description" content="The official home of the Python Programming Language">
            
            <meta name="keywords" content="Python programming language object oriented web free open source software license documentation download community">
        </head>
        <body>
            PEP 274 -- Dict Comprehensions | Python.org
        </body>
    </html>
    """

    sut = DocAnalyser(doc_fetcher_mock(html_doc))
    doc_summary = sut.analyse('https://www.python.org/dev/peps/pep-0274/')

    expected_results = (
        ('charset', 'utf-8'),
        ('X-UA-Compatible', 'IE=edge'),
        ('imagetoolbar', 'false'),
        ('og:type', 'website'),
        ('og:site_name', 'Python.org'),
        ('og:title', 'PEP 274 -- Dict Comprehensions'),
        ('og:description', 'The official home of the Python Programming Language'),
        ('keywords', 'Python programming language object oriented web free open source software license documentation download community'),
    )

    assert len(doc_summary.meta_tags) == len(expected_results)
    for tag_index, expected in enumerate(expected_results):
        assert doc_summary.meta_tags[tag_index].name == expected[0] and doc_summary.meta_tags[tag_index].content == expected[1]


def doc_fetcher_mock(expected_fetched_doc: str) ->Callable:
    def mock(url: str) ->str:
        return expected_fetched_doc

    return mock
