
from typing import Callable, List, NamedTuple
from bs4 import BeautifulSoup
import humanfriendly


class DocMetaTag(NamedTuple):
    name: str
    content: str


class DocSummary(NamedTuple):
    page_title: str
    meta_tags: List[DocMetaTag]
    doc_size: int
    body_content: str

    @property
    def doc_size_human_friendly(self) -> str:
        return humanfriendly.format_size(self.doc_size)

    @property
    def word_count(self) -> int:
        return len(self.body_content.split(' '))

    @property
    def unique_word_count(self) -> int:
        return len(set(self.body_content.split(' ')))


class DocAnalyser:

    def __init__(self, doc_fetcher: Callable):
        self.doc_fetcher = doc_fetcher

    def analyse(self, url: str) -> DocSummary:
        html_doc: str = self.doc_fetcher(url)
        soup = BeautifulSoup(html_doc, 'html.parser')

        doc_summary_dict = {
            'page_title': soup.title.string if soup.title else None,
            'meta_tags': self._get_meta_tags(soup),
            'doc_size': len(html_doc),
        }
        doc_summary_dict['body_content'] = soup.get_text()[
            (len(doc_summary_dict['page_title']) if doc_summary_dict['page_title'] is not None else 0):
        ]

        return DocSummary(**doc_summary_dict)

    def _get_meta_tags(self, soup: BeautifulSoup) -> List[DocMetaTag]:
        meta_tags = []
        for meta in soup.find_all('meta'):
            content: str = meta.get('content')

            # Try various <meta> tags types
            name: str = meta.get('name')
            if name is None:
                name = meta.get('http-equiv')
            if name is None:
                name = meta.get('property')
            if name is None and 'charset' in meta.attrs:
                name = 'charset'
                content = meta.get('charset')

            meta_tags.append(DocMetaTag(name=name, content=content))

        return meta_tags
