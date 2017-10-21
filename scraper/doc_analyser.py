
from collections import Counter
from typing import Callable, NamedTuple, Optional, List, Set, Tuple
from bs4 import BeautifulSoup
import humanfriendly


class DocMetaTag(NamedTuple):
    name: str
    content: str


class DocLink(NamedTuple):
    text: str
    href: str


class DocSummary(NamedTuple):
    page_title: str
    meta_tags: List[DocMetaTag]
    doc_size: int
    body_content: str
    links: List[DocLink]

    @property
    def doc_size_human_friendly(self) -> str:
        return humanfriendly.format_size(self.doc_size)

    @property
    def words(self) -> Tuple[str]:
        return tuple([word.strip() for word in self.body_content.split(' ') if word])

    @property
    def unique_words(self) -> Set[str]:
        return set(self.words)

    @property
    def word_count(self) -> int:
        return len(self.words)

    @property
    def unique_word_count(self) -> int:
        return len(self.unique_words)

    @property
    def most_common_5_words(self) -> List[str]:
        counter = Counter(self.words)
        return counter.most_common(5)

    @property
    def missing_meta_keywords(self) -> List[str]:
        keywords = self.get_meta_by_name('keywords')
        if keywords is None:
            return []

        missing_keywords = []
        unique_words = self.unique_words
        for keyword in keywords.content.split(' '):
            if keyword not in unique_words:
                missing_keywords.append(keyword)

        return missing_keywords

    def get_meta_by_name(self, name: str) -> Optional[DocMetaTag]:
        for meta in self.meta_tags:
            if meta.name == name:
                return meta
        return None


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
            'links': self._get_links(soup),
        }
        # BeautifulSoup's `get_text()` method is quite convenient, but it prefixes the `<body>` text content
        # with the page title, which is not what we want.
        # --> let's strip the title prefix from the `get_text()` result:
        doc_summary_dict['body_content'] = soup.get_text()[
            (len(doc_summary_dict['page_title']) if doc_summary_dict['page_title'] is not None else 0):
        ]

        return DocSummary(**doc_summary_dict)

    @staticmethod
    def _get_meta_tags(soup: BeautifulSoup) -> List[DocMetaTag]:
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

    @staticmethod
    def _get_links(soup: BeautifulSoup) -> List[DocLink]:
        return [DocLink(a.string, a.get('href')) for a in soup.find_all('a')]
