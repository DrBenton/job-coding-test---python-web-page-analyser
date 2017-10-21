
import re
import sys
from pprint import pprint
from scraper.doc_fetcher import fetch_url_content
from scraper.doc_analyser import DocAnalyser, DocSummary

if len(sys.argv) < 2:
    print('Usage: python main.py [URL]')
    print('(or "make run URL=[URL]" from the Makefile)')
    sys.exit(1)

target_url: str = sys.argv[1]

if not re.compile('^https?:\/\/').match(target_url):
    print(f'"{target_url}" is not a valid URL (should start with "http(s)://")')
    sys.exit(1)

print('Fetching page content...')

doc_analyser = DocAnalyser(fetch_url_content)
doc_summary: DocSummary = doc_analyser.analyse(target_url)

print('Page content fetched.')

print('')

print(f'Page title: {doc_summary.page_title}')
print(f'Page size: {doc_summary.doc_size} ({doc_summary.doc_size_human_friendly})')
print(f'Word count: {doc_summary.word_count}')
print(f'Unique word count: {doc_summary.unique_word_count}')

print('Most common words:')
for common_word in doc_summary.most_common_5_words:
    print(f' * {common_word[0]} ({common_word[1]} times)')

print('Meta keywords which do not appear in the content:')
for missing_meta_keyword in doc_summary.missing_meta_keywords:
    print(f' * {missing_meta_keyword}')

print('Meta tags:')
for meta_tag in doc_summary.meta_tags:
    print(f' * {meta_tag.name} (value: {meta_tag.content})')

print('Links:')
for link in doc_summary.links:
    print(f' * {link.text} (href: {link.href})')

