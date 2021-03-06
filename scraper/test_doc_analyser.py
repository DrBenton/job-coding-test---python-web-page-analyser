
from typing import Callable
from scraper.doc_analyser import DocAnalyser


def test_parsing_title():
    html_doc = '<html><head><title>Hello Plum!</title></head><body>Once upon a time there were three little sisters</body></html>'

    sut = DocAnalyser(_doc_fetcher_mock(html_doc))
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

    sut = DocAnalyser(_doc_fetcher_mock(html_doc))
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


def test_doc_size():
    sut = DocAnalyser(_doc_fetcher_mock(_test_real_doc_content))
    doc_summary = sut.analyse('https://docs.djangoproject.com/en/1.11/misc/design-philosophies/')

    assert doc_summary.doc_size == 38623
    assert doc_summary.doc_size_human_friendly == '38.62 KB'


def test_parsing_body_content():
    html_doc_with_title = '<html><head><title>Hello Plum!</title></head><body>Once upon a <b>time</b> there were <span class="highlight"><i>three</i> little sisters</span></body></html>'

    sut = DocAnalyser(_doc_fetcher_mock(html_doc_with_title))
    doc_summary = sut.analyse('http://dummy.com')

    assert doc_summary.body_content == 'Once upon a time there were three little sisters'

    html_doc_without_title = '<html><head></head><body>Once upon a <b>time</b> there were <span class="highlight"><i>three</i> little sisters</span></body></html>'

    sut = DocAnalyser(_doc_fetcher_mock(html_doc_without_title))
    doc_summary = sut.analyse('http://dummy.com')

    assert doc_summary.body_content == 'Once upon a time there were three little sisters'


def test_parsing_word_count():
    html_doc = '<html><head><title>Hello Plum!</title></head><body>Once upon a time there were three little sisters</body></html>'

    sut = DocAnalyser(_doc_fetcher_mock(html_doc))
    doc_summary = sut.analyse('http://dummy.com')

    assert doc_summary.word_count == 9


def test_parsing_unique_word_count():
    html_doc = '<html><head><title>Hello Plum!</title></head><body>Once upon a time upon there were little three little sisters</body></html>'

    sut = DocAnalyser(_doc_fetcher_mock(html_doc))
    doc_summary = sut.analyse('http://dummy.com')

    assert doc_summary.word_count == 11
    assert doc_summary.unique_word_count == 9


def test_parsing_most_common_words():
    html_doc = '<html><head><title>Hello Plum!</title></head><body>Once a upon little upon upon a time upon there a were a little three little a sisters fairy tale tale</body></html>'

    sut = DocAnalyser(_doc_fetcher_mock(html_doc))
    doc_summary = sut.analyse('http://dummy.com')

    assert doc_summary.most_common_5_words == [('a', 5), ('upon', 4), ('little', 3), ('tale', 2), ('Once', 1)]


def test_parsing_missing_keywords():
    html_doc = """
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="keywords" content="Python programming language object oriented web free open source software license documentation download community">
        </head>
        <body>
            Once upon a web time there were three little Python sisters downloading free open source 
            <span>documentation</span> for their community
        </body>
    </html>
    """

    sut = DocAnalyser(_doc_fetcher_mock(html_doc))
    doc_summary = sut.analyse('http://dummy.com')

    assert doc_summary.missing_meta_keywords == ['programming', 'language', 'object', 'oriented', 'software', 'license', 'download']


def test_parsing_links():
    html_doc = """
    <html>
        <body>
            Once upon a web time there were three little <A hRef="/">Python</a> sisters downloading free open source 
            <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">documentation</span> for their
            <a href="https://www.python.org/community/" target="_blank">community</a>
        </body>
    </html>
    """

    sut = DocAnalyser(_doc_fetcher_mock(html_doc))
    doc_summary = sut.analyse('http://dummy.com')

    expected_results = (
        ('Python', '/'),
        ('documentation', 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'),
        ('community', 'https://www.python.org/community/'),
    )

    assert len(doc_summary.links) == len(expected_results)
    for link_index, expected in enumerate(expected_results):
        assert doc_summary.links[link_index].text == expected[0] and doc_summary.links[link_index].href == expected[1]


def _doc_fetcher_mock(expected_fetched_doc: str) ->Callable:
    def mock(url: str) ->str:
        return expected_fetched_doc

    return mock


_test_real_doc_content = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="ROBOTS" content="ALL" />
    <meta http-equiv="imagetoolbar" content="no" />
    <meta name="MSSmartTagsPreventParsing" content="true" />
    <meta name="Copyright" content="Django Software Foundation" />
    <meta name="keywords" content="Python, Django, framework, open-source" />
    <meta name="description" content="" />

    <!-- Favicons -->
    <link rel="apple-touch-icon" href="/s/img/icon-touch.e4872c4da341.png">
    <link rel="icon" sizes="192x192" href="/s/img/icon-touch.e4872c4da341.png">
    <link rel="shortcut icon" href="/s/img/favicon.6dbf28c0650e.ico">
    <meta name="msapplication-TileColor" content="#113228">
    <meta name="msapplication-TileImage" content="/s/img/icon-tile.b01ac0ef9f67.png">

    <title>Design philosophies | Django documentation | Django</title>

    <link rel="stylesheet" href="/s/css/output.5f8483691d8b.css" >
    <script src="/s/js/lib/webfontloader/webfontloader.e75218f5f090.js"></script>
    <script>
    WebFont.load({
      custom: {
        families: ['FontAwesome', 'Fira+Mono'],
      },
      google: {
        families: ['Roboto:400italic,700italic,300,700,400:latin'
        ]
      },
      classes: false,
      events: false,
      timeout: 1000
    });
    </script>
    <script src="/s/js/lib/modernizr.3b36762e418a.js"></script>
    
  
    
      
    
  
  <link rel="canonical" href="https://docs.djangoproject.com/en/1.11/misc/design-philosophies/">
  
    
        
          
        
        
        <link rel="alternate"
           hreflang="el"
           href="https://docs.djangoproject.com/el/1.11/misc/design-philosophies/">
    
        
          
        
        
        <link rel="alternate"
           hreflang="x-default"
           href="https://docs.djangoproject.com/en/1.11/misc/design-philosophies/">
        
        <link rel="alternate"
           hreflang="en"
           href="https://docs.djangoproject.com/en/1.11/misc/design-philosophies/">
    
        
          
        
        
        <link rel="alternate"
           hreflang="es"
           href="https://docs.djangoproject.com/es/1.11/misc/design-philosophies/">
    
        
          
        
        
        <link rel="alternate"
           hreflang="fr"
           href="https://docs.djangoproject.com/fr/1.11/misc/design-philosophies/">
    
        
          
        
        
        <link rel="alternate"
           hreflang="id"
           href="https://docs.djangoproject.com/id/1.11/misc/design-philosophies/">
    
        
          
        
        
        <link rel="alternate"
           hreflang="ja"
           href="https://docs.djangoproject.com/ja/1.11/misc/design-philosophies/">
    
        
          
        
        
        <link rel="alternate"
           hreflang="ko"
           href="https://docs.djangoproject.com/ko/1.11/misc/design-philosophies/">
    
        
          
        
        
        <link rel="alternate"
           hreflang="pl"
           href="https://docs.djangoproject.com/pl/1.11/misc/design-philosophies/">
    
        
          
        
        
        <link rel="alternate"
           hreflang="pt-br"
           href="https://docs.djangoproject.com/pt-br/1.11/misc/design-philosophies/">
    
  

  <link rel="search"
        type="application/opensearchdescription+xml"
        href="https://docs.djangoproject.com/en/1.11/search/description/"
        title="Django documentation">

  </head>

  <body id="generic" class="">

    <div role="banner" id="top">
  <div class="container">
    <a class="logo" href="https://www.djangoproject.com/">Django</a>
    <p class="meta">The web framework for perfectionists with deadlines.</p>
    <div role="navigation">
      <ul>
        <li>
          <a href="https://www.djangoproject.com/start/overview/">Overview</a>
        </li>
        <li>
          <a href="https://www.djangoproject.com/download/">Download</a>
        </li>
        <li class="active">
          <a href="https://docs.djangoproject.com/">Documentation</a>
        </li>
        <li>
          <a href="https://www.djangoproject.com/weblog/">News</a>
        </li>
        <li>
          <a href="https://www.djangoproject.com/community/">Community</a>
        </li>
        <li>
          <a href="https://code.djangoproject.com/">Code</a>
        </li>
        <li>
          <a href="https://www.djangoproject.com/foundation/">About</a>
        </li>
        <li>
          <a href="https://www.djangoproject.com/fundraising/">&#9829; Donate</a>
        </li>
      </ul>
    </div>
  </div>
</div>


    <div class="copy-banner">
      <div class="container">
        
  <h1><a href="https://docs.djangoproject.com/en/1.11/">Documentation</a></h1>

      </div>
    </div>
    <div id="billboard"></div>

    <div class="container sidebar-right">
      <div role="main">

        
          
        

        
<div id="version-switcher">
  <ul id="doc-languages" class="language-switcher">
  
  
  <li class="other">
    
      
    
    <a href="https://docs.djangoproject.com/el/1.11/misc/design-philosophies/">el</a>
  </li>
  
  
  
  
  
  <li class="other">
    
      
    
    <a href="https://docs.djangoproject.com/es/1.11/misc/design-philosophies/">es</a>
  </li>
  
  
  
  <li class="other">
    
      
    
    <a href="https://docs.djangoproject.com/fr/1.11/misc/design-philosophies/">fr</a>
  </li>
  
  
  
  <li class="other">
    
      
    
    <a href="https://docs.djangoproject.com/id/1.11/misc/design-philosophies/">id</a>
  </li>
  
  
  
  <li class="other">
    
      
    
    <a href="https://docs.djangoproject.com/ja/1.11/misc/design-philosophies/">ja</a>
  </li>
  
  
  
  <li class="other">
    
      
    
    <a href="https://docs.djangoproject.com/ko/1.11/misc/design-philosophies/">ko</a>
  </li>
  
  
  
  <li class="other">
    
      
    
    <a href="https://docs.djangoproject.com/pl/1.11/misc/design-philosophies/">pl</a>
  </li>
  
  
  
  <li class="other">
    
      
    
    <a href="https://docs.djangoproject.com/pt-br/1.11/misc/design-philosophies/">pt-br</a>
  </li>
  
  
    <li class="current"
        title="Click on the links on the left to switch to another language.">
      <span>Language: <strong>en</strong></span>
    </li>
  </ul>

  
  <ul id="doc-versions" class="version-switcher">
    
    
    <li class="other">
      
        
      
      <a href="https://docs.djangoproject.com/en/1.7/misc/design-philosophies/">1.7</a>
    </li>
    
    
    
    <li class="other">
      
        
      
      <a href="https://docs.djangoproject.com/en/1.8/misc/design-philosophies/">1.8</a>
    </li>
    
    
    
    <li class="other">
      
        
      
      <a href="https://docs.djangoproject.com/en/1.9/misc/design-philosophies/">1.9</a>
    </li>
    
    
    
    <li class="other">
      
        
      
      <a href="https://docs.djangoproject.com/en/1.10/misc/design-philosophies/">1.10</a>
    </li>
    
    
    
    
    
    <li class="other">
      
        
      
      <a href="https://docs.djangoproject.com/en/2.0/misc/design-philosophies/">2.0</a>
    </li>
    
    
    
    <li class="other">
      
        
      
      <a href="https://docs.djangoproject.com/en/dev/misc/design-philosophies/">dev</a>
    </li>
    
    
    <li class="current"
        title="This document describes Django 1.11. Click on the links on the left to see other versions.">
       <span>Documentation version:
         <strong>1.11</strong>
       </span>
    </li>
  </ul>
</div>


<div id="docs-content">
<div class="section" id="s-design-philosophies">
<span id="design-philosophies"></span><h1>Design philosophies<a class="headerlink" href="#design-philosophies" title="Permalink to this headline">¶</a></h1>
<p>This document explains some of the fundamental philosophies Django’s developers
have used in creating the framework. Its goal is to explain the past and guide
the future.</p>
<div class="section" id="s-overall">
<span id="overall"></span><h2>Overall<a class="headerlink" href="#overall" title="Permalink to this headline">¶</a></h2>
<div class="section" id="s-loose-coupling">
<span id="s-id1"></span><span id="loose-coupling"></span><span id="id1"></span><h3>Loose coupling<a class="headerlink" href="#loose-coupling" title="Permalink to this headline">¶</a></h3>
<p id="index-0">A fundamental goal of Django’s stack is <a class="reference external" href="http://wiki.c2.com/?CouplingAndCohesion">loose coupling and tight cohesion</a>.
The various layers of the framework shouldn’t “know” about each other unless
absolutely necessary.</p>
<p>For example, the template system knows nothing about Web requests, the database
layer knows nothing about data display and the view system doesn’t care which
template system a programmer uses.</p>
<p>Although Django comes with a full stack for convenience, the pieces of the
stack are independent of another wherever possible.</p>
</div>
<div class="section" id="s-less-code">
<span id="s-id2"></span><span id="less-code"></span><span id="id2"></span><h3>Less code<a class="headerlink" href="#less-code" title="Permalink to this headline">¶</a></h3>
<p>Django apps should use as little code as possible; they should lack boilerplate.
Django should take full advantage of Python’s dynamic capabilities, such as
introspection.</p>
</div>
<div class="section" id="s-quick-development">
<span id="s-id3"></span><span id="quick-development"></span><span id="id3"></span><h3>Quick development<a class="headerlink" href="#quick-development" title="Permalink to this headline">¶</a></h3>
<p>The point of a Web framework in the 21st century is to make the tedious aspects
of Web development fast. Django should allow for incredibly quick Web
development.</p>
</div>
<div class="section" id="s-don-t-repeat-yourself-dry">
<span id="s-dry"></span><span id="don-t-repeat-yourself-dry"></span><span id="dry"></span><h3>Don’t repeat yourself (DRY)<a class="headerlink" href="#don-t-repeat-yourself-dry" title="Permalink to this headline">¶</a></h3>
<p id="index-1">Every distinct concept and/or piece of data should live in one, and only one,
place. Redundancy is bad. Normalization is good.</p>
<p>The framework, within reason, should deduce as much as possible from as little
as possible.</p>
<div class="admonition seealso">
<p class="first admonition-title">See also</p>
<p class="last">The <a class="reference external" href="http://wiki.c2.com/?DontRepeatYourself">discussion of DRY on the Portland Pattern Repository</a></p>
</div>
</div>
<div class="section" id="s-explicit-is-better-than-implicit">
<span id="s-id5"></span><span id="explicit-is-better-than-implicit"></span><span id="id5"></span><h3>Explicit is better than implicit<a class="headerlink" href="#explicit-is-better-than-implicit" title="Permalink to this headline">¶</a></h3>
<p>This is a core Python principle listed in <span class="target" id="index-2"></span><a class="pep reference external" href="https://www.python.org/dev/peps/pep-0020"><strong>PEP 20</strong></a>, and it means Django
shouldn’t do too much “magic.” Magic shouldn’t happen unless there’s a really
good reason for it. Magic is worth using only if it creates a huge convenience
unattainable in other ways, and it isn’t implemented in a way that confuses
developers who are trying to learn how to use the feature.</p>
</div>
<div class="section" id="s-consistency">
<span id="s-id6"></span><span id="consistency"></span><span id="id6"></span><h3>Consistency<a class="headerlink" href="#consistency" title="Permalink to this headline">¶</a></h3>
<p>The framework should be consistent at all levels. Consistency applies to
everything from low-level (the Python coding style used) to high-level (the
“experience” of using Django).</p>
</div>
</div>
<div class="section" id="s-models">
<span id="models"></span><h2>Models<a class="headerlink" href="#models" title="Permalink to this headline">¶</a></h2>
<div class="section" id="s-id7">
<span id="id7"></span><h3>Explicit is better than implicit<a class="headerlink" href="#id7" title="Permalink to this headline">¶</a></h3>
<p>Fields shouldn’t assume certain behaviors based solely on the name of the
field. This requires too much knowledge of the system and is prone to errors.
Instead, behaviors should be based on keyword arguments and, in some cases, on
the type of the field.</p>
</div>
<div class="section" id="s-include-all-relevant-domain-logic">
<span id="include-all-relevant-domain-logic"></span><h3>Include all relevant domain logic<a class="headerlink" href="#include-all-relevant-domain-logic" title="Permalink to this headline">¶</a></h3>
<p>Models should encapsulate every aspect of an “object,” following Martin
Fowler’s <a class="reference external" href="https://www.martinfowler.com/eaaCatalog/activeRecord.html">Active Record</a> design pattern.</p>
<p>This is why both the data represented by a model and information about
it (its human-readable name, options like default ordering, etc.) are
defined in the model class; all the information needed to understand a
given model should be stored <em>in</em> the model.</p>
</div>
</div>
<div class="section" id="s-database-api">
<span id="database-api"></span><h2>Database API<a class="headerlink" href="#database-api" title="Permalink to this headline">¶</a></h2>
<p>The core goals of the database API are:</p>
<div class="section" id="s-sql-efficiency">
<span id="sql-efficiency"></span><h3>SQL efficiency<a class="headerlink" href="#sql-efficiency" title="Permalink to this headline">¶</a></h3>
<p>It should execute SQL statements as few times as possible, and it should
optimize statements internally.</p>
<p>This is why developers need to call <code class="docutils literal"><span class="pre">save()</span></code> explicitly, rather than the
framework saving things behind the scenes silently.</p>
<p>This is also why the <code class="docutils literal"><span class="pre">select_related()</span></code> <code class="docutils literal"><span class="pre">QuerySet</span></code> method exists. It’s an
optional performance booster for the common case of selecting “every related
object.”</p>
</div>
<div class="section" id="s-terse-powerful-syntax">
<span id="terse-powerful-syntax"></span><h3>Terse, powerful syntax<a class="headerlink" href="#terse-powerful-syntax" title="Permalink to this headline">¶</a></h3>
<p>The database API should allow rich, expressive statements in as little syntax
as possible. It should not rely on importing other modules or helper objects.</p>
<p>Joins should be performed automatically, behind the scenes, when necessary.</p>
<p>Every object should be able to access every related object, systemwide. This
access should work both ways.</p>
</div>
<div class="section" id="s-option-to-drop-into-raw-sql-easily-when-needed">
<span id="option-to-drop-into-raw-sql-easily-when-needed"></span><h3>Option to drop into raw SQL easily, when needed<a class="headerlink" href="#option-to-drop-into-raw-sql-easily-when-needed" title="Permalink to this headline">¶</a></h3>
<p>The database API should realize it’s a shortcut but not necessarily an
end-all-be-all. The framework should make it easy to write custom SQL – entire
statements, or just custom <code class="docutils literal"><span class="pre">WHERE</span></code> clauses as custom parameters to API calls.</p>
</div>
</div>
<div class="section" id="s-url-design">
<span id="url-design"></span><h2>URL design<a class="headerlink" href="#url-design" title="Permalink to this headline">¶</a></h2>
<div class="section" id="s-id8">
<span id="id8"></span><h3>Loose coupling<a class="headerlink" href="#id8" title="Permalink to this headline">¶</a></h3>
<p>URLs in a Django app should not be coupled to the underlying Python code. Tying
URLs to Python function names is a Bad And Ugly Thing.</p>
<p>Along these lines, the Django URL system should allow URLs for the same app to
be different in different contexts. For example, one site may put stories at
<code class="docutils literal"><span class="pre">/stories/</span></code>, while another may use <code class="docutils literal"><span class="pre">/news/</span></code>.</p>
</div>
<div class="section" id="s-infinite-flexibility">
<span id="infinite-flexibility"></span><h3>Infinite flexibility<a class="headerlink" href="#infinite-flexibility" title="Permalink to this headline">¶</a></h3>
<p>URLs should be as flexible as possible. Any conceivable URL design should be
allowed.</p>
</div>
<div class="section" id="s-encourage-best-practices">
<span id="encourage-best-practices"></span><h3>Encourage best practices<a class="headerlink" href="#encourage-best-practices" title="Permalink to this headline">¶</a></h3>
<p>The framework should make it just as easy (or even easier) for a developer to
design pretty URLs than ugly ones.</p>
<p>File extensions in Web-page URLs should be avoided.</p>
<p>Vignette-style commas in URLs deserve severe punishment.</p>
</div>
<div class="section" id="s-definitive-urls">
<span id="s-id9"></span><span id="definitive-urls"></span><span id="id9"></span><h3>Definitive URLs<a class="headerlink" href="#definitive-urls" title="Permalink to this headline">¶</a></h3>
<p id="index-3">Technically, <code class="docutils literal"><span class="pre">foo.com/bar</span></code> and <code class="docutils literal"><span class="pre">foo.com/bar/</span></code> are two different URLs, and
search-engine robots (and some Web traffic-analyzing tools) would treat them as
separate pages. Django should make an effort to “normalize” URLs so that
search-engine robots don’t get confused.</p>
<p>This is the reasoning behind the <a class="reference internal" href="../../ref/settings/#std:setting-APPEND_SLASH"><code class="xref std std-setting docutils literal"><span class="pre">APPEND_SLASH</span></code></a> setting.</p>
</div>
</div>
<div class="section" id="s-template-system">
<span id="template-system"></span><h2>Template system<a class="headerlink" href="#template-system" title="Permalink to this headline">¶</a></h2>
<div class="section" id="s-separate-logic-from-presentation">
<span id="s-separation-of-logic-and-presentation"></span><span id="separate-logic-from-presentation"></span><span id="separation-of-logic-and-presentation"></span><h3>Separate logic from presentation<a class="headerlink" href="#separate-logic-from-presentation" title="Permalink to this headline">¶</a></h3>
<p>We see a template system as a tool that controls presentation and
presentation-related logic – and that’s it. The template system shouldn’t
support functionality that goes beyond this basic goal.</p>
</div>
<div class="section" id="s-discourage-redundancy">
<span id="discourage-redundancy"></span><h3>Discourage redundancy<a class="headerlink" href="#discourage-redundancy" title="Permalink to this headline">¶</a></h3>
<p>The majority of dynamic websites use some sort of common sitewide design –
a common header, footer, navigation bar, etc. The Django template system should
make it easy to store those elements in a single place, eliminating duplicate
code.</p>
<p>This is the philosophy behind <a class="reference internal" href="../../ref/templates/language/#template-inheritance"><span class="std std-ref">template inheritance</span></a>.</p>
</div>
<div class="section" id="s-be-decoupled-from-html">
<span id="be-decoupled-from-html"></span><h3>Be decoupled from HTML<a class="headerlink" href="#be-decoupled-from-html" title="Permalink to this headline">¶</a></h3>
<p>The template system shouldn’t be designed so that it only outputs HTML. It
should be equally good at generating other text-based formats, or just plain
text.</p>
</div>
<div class="section" id="s-xml-should-not-be-used-for-template-languages">
<span id="xml-should-not-be-used-for-template-languages"></span><h3>XML should not be used for template languages<a class="headerlink" href="#xml-should-not-be-used-for-template-languages" title="Permalink to this headline">¶</a></h3>
<p id="index-4">Using an XML engine to parse templates introduces a whole new world of human
error in editing templates – and incurs an unacceptable level of overhead in
template processing.</p>
</div>
<div class="section" id="s-assume-designer-competence">
<span id="assume-designer-competence"></span><h3>Assume designer competence<a class="headerlink" href="#assume-designer-competence" title="Permalink to this headline">¶</a></h3>
<p>The template system shouldn’t be designed so that templates necessarily are
displayed nicely in WYSIWYG editors such as Dreamweaver. That is too severe of
a limitation and wouldn’t allow the syntax to be as nice as it is. Django
expects template authors are comfortable editing HTML directly.</p>
</div>
<div class="section" id="s-treat-whitespace-obviously">
<span id="treat-whitespace-obviously"></span><h3>Treat whitespace obviously<a class="headerlink" href="#treat-whitespace-obviously" title="Permalink to this headline">¶</a></h3>
<p>The template system shouldn’t do magic things with whitespace. If a template
includes whitespace, the system should treat the whitespace as it treats text
– just display it. Any whitespace that’s not in a template tag should be
displayed.</p>
</div>
<div class="section" id="s-don-t-invent-a-programming-language">
<span id="don-t-invent-a-programming-language"></span><h3>Don’t invent a programming language<a class="headerlink" href="#don-t-invent-a-programming-language" title="Permalink to this headline">¶</a></h3>
<p>The goal is not to invent a programming language. The goal is to offer just
enough programming-esque functionality, such as branching and looping, that is
essential for making presentation-related decisions. The <a class="reference internal" href="../../topics/templates/#template-language-intro"><span class="std std-ref">Django Template
Language (DTL)</span></a> aims to avoid advanced logic.</p>
<p>The Django template system recognizes that templates are most often written by
<em>designers</em>, not <em>programmers</em>, and therefore should not assume Python
knowledge.</p>
</div>
<div class="section" id="s-safety-and-security">
<span id="safety-and-security"></span><h3>Safety and security<a class="headerlink" href="#safety-and-security" title="Permalink to this headline">¶</a></h3>
<p>The template system, out of the box, should forbid the inclusion of malicious
code – such as commands that delete database records.</p>
<p>This is another reason the template system doesn’t allow arbitrary Python code.</p>
</div>
<div class="section" id="s-extensibility">
<span id="extensibility"></span><h3>Extensibility<a class="headerlink" href="#extensibility" title="Permalink to this headline">¶</a></h3>
<p>The template system should recognize that advanced template authors may want
to extend its technology.</p>
<p>This is the philosophy behind custom template tags and filters.</p>
</div>
</div>
<div class="section" id="s-views">
<span id="views"></span><h2>Views<a class="headerlink" href="#views" title="Permalink to this headline">¶</a></h2>
<div class="section" id="s-simplicity">
<span id="simplicity"></span><h3>Simplicity<a class="headerlink" href="#simplicity" title="Permalink to this headline">¶</a></h3>
<p>Writing a view should be as simple as writing a Python function. Developers
shouldn’t have to instantiate a class when a function will do.</p>
</div>
<div class="section" id="s-use-request-objects">
<span id="use-request-objects"></span><h3>Use request objects<a class="headerlink" href="#use-request-objects" title="Permalink to this headline">¶</a></h3>
<p>Views should have access to a request object – an object that stores metadata
about the current request. The object should be passed directly to a view
function, rather than the view function having to access the request data from
a global variable. This makes it light, clean and easy to test views by passing
in “fake” request objects.</p>
</div>
<div class="section" id="s-id10">
<span id="id10"></span><h3>Loose coupling<a class="headerlink" href="#id10" title="Permalink to this headline">¶</a></h3>
<p>A view shouldn’t care about which template system the developer uses – or even
whether a template system is used at all.</p>
</div>
<div class="section" id="s-differentiate-between-get-and-post">
<span id="differentiate-between-get-and-post"></span><h3>Differentiate between GET and POST<a class="headerlink" href="#differentiate-between-get-and-post" title="Permalink to this headline">¶</a></h3>
<p>GET and POST are distinct; developers should explicitly use one or the other.
The framework should make it easy to distinguish between GET and POST data.</p>
</div>
</div>
<div class="section" id="s-cache-framework">
<span id="s-cache-design-philosophy"></span><span id="cache-framework"></span><span id="cache-design-philosophy"></span><h2>Cache Framework<a class="headerlink" href="#cache-framework" title="Permalink to this headline">¶</a></h2>
<p>The core goals of Django’s <a class="reference internal" href="../../topics/cache/"><span class="doc">cache framework</span></a> are:</p>
<div class="section" id="s-id11">
<span id="id11"></span><h3>Less code<a class="headerlink" href="#id11" title="Permalink to this headline">¶</a></h3>
<p>A cache should be as fast as possible.  Hence, all framework code surrounding
the cache backend should be kept to the absolute minimum, especially for
<code class="docutils literal"><span class="pre">get()</span></code> operations.</p>
</div>
<div class="section" id="s-id12">
<span id="id12"></span><h3>Consistency<a class="headerlink" href="#id12" title="Permalink to this headline">¶</a></h3>
<p>The cache API should provide a consistent interface across the different
cache backends.</p>
</div>
<div class="section" id="s-id13">
<span id="id13"></span><h3>Extensibility<a class="headerlink" href="#id13" title="Permalink to this headline">¶</a></h3>
<p>The cache API should be extensible at the application level based on the
developer’s needs (for example, see <a class="reference internal" href="../../topics/cache/#cache-key-transformation"><span class="std std-ref">Cache key transformation</span></a>).</p>
</div>
</div>
</div>

</div>



<div class="browse-horizontal">
  
  <div class="left"><a href="../api-stability/"><i class="icon icon-chevron-left"></i> API stability</a></div>
  
  
  <div class="right"><a href="../distributions/">Third-party distributions of Django <i class="icon icon-chevron-right"></i></a></div>
  
</div>



        <a href="#top" class="backtotop"><i class="icon icon-chevron-up"></i> Back to Top</a>
      </div>

      
<h1 class="visuallyhidden">Additional Information</h1>
<div role="complementary">
  
  

<form action="https://docs.djangoproject.com/en/1.11/search/" class="search form-input" role="search">
  <label class="visuallyhidden" for="news-search">Search:</label>
    <input type="search" name="q" placeholder="Search 1.11 documentation" id="id_q" />

    <button type="submit">
      <i class="icon icon-search"></i>
      <span class="visuallyhidden">Search</span>
    </button>
</form>

  

  


  <div class="fundraising-sidebar">
    <h2>Support Django!</h2>

    <div class="small-heart">
      <img src="/s/img/small-fundraising-heart.d255f6e934e5.png" alt="Support Django!" />
    </div>

    <div class="small-cta">
      <ul class="list-links-small">
        <li><a href="https://www.djangoproject.com/fundraising/">
          Puneet Kaura donated to the Django Software Foundation to
          support Django development. Donate today!
        </a></li>
      </ul>
    </div>
  </div>



  
    <h2>Contents</h2>
    
    <ul>
<li><a class="reference internal" href="#">Design philosophies</a><ul>
<li><a class="reference internal" href="#overall">Overall</a><ul>
<li><a class="reference internal" href="#loose-coupling">Loose coupling</a></li>
<li><a class="reference internal" href="#less-code">Less code</a></li>
<li><a class="reference internal" href="#quick-development">Quick development</a></li>
<li><a class="reference internal" href="#don-t-repeat-yourself-dry">Don’t repeat yourself (DRY)</a></li>
<li><a class="reference internal" href="#explicit-is-better-than-implicit">Explicit is better than implicit</a></li>
<li><a class="reference internal" href="#consistency">Consistency</a></li>
</ul>
</li>
<li><a class="reference internal" href="#models">Models</a><ul>
<li><a class="reference internal" href="#id7">Explicit is better than implicit</a></li>
<li><a class="reference internal" href="#include-all-relevant-domain-logic">Include all relevant domain logic</a></li>
</ul>
</li>
<li><a class="reference internal" href="#database-api">Database API</a><ul>
<li><a class="reference internal" href="#sql-efficiency">SQL efficiency</a></li>
<li><a class="reference internal" href="#terse-powerful-syntax">Terse, powerful syntax</a></li>
<li><a class="reference internal" href="#option-to-drop-into-raw-sql-easily-when-needed">Option to drop into raw SQL easily, when needed</a></li>
</ul>
</li>
<li><a class="reference internal" href="#url-design">URL design</a><ul>
<li><a class="reference internal" href="#id8">Loose coupling</a></li>
<li><a class="reference internal" href="#infinite-flexibility">Infinite flexibility</a></li>
<li><a class="reference internal" href="#encourage-best-practices">Encourage best practices</a></li>
<li><a class="reference internal" href="#definitive-urls">Definitive URLs</a></li>
</ul>
</li>
<li><a class="reference internal" href="#template-system">Template system</a><ul>
<li><a class="reference internal" href="#separate-logic-from-presentation">Separate logic from presentation</a></li>
<li><a class="reference internal" href="#discourage-redundancy">Discourage redundancy</a></li>
<li><a class="reference internal" href="#be-decoupled-from-html">Be decoupled from HTML</a></li>
<li><a class="reference internal" href="#xml-should-not-be-used-for-template-languages">XML should not be used for template languages</a></li>
<li><a class="reference internal" href="#assume-designer-competence">Assume designer competence</a></li>
<li><a class="reference internal" href="#treat-whitespace-obviously">Treat whitespace obviously</a></li>
<li><a class="reference internal" href="#don-t-invent-a-programming-language">Don’t invent a programming language</a></li>
<li><a class="reference internal" href="#safety-and-security">Safety and security</a></li>
<li><a class="reference internal" href="#extensibility">Extensibility</a></li>
</ul>
</li>
<li><a class="reference internal" href="#views">Views</a><ul>
<li><a class="reference internal" href="#simplicity">Simplicity</a></li>
<li><a class="reference internal" href="#use-request-objects">Use request objects</a></li>
<li><a class="reference internal" href="#id10">Loose coupling</a></li>
<li><a class="reference internal" href="#differentiate-between-get-and-post">Differentiate between GET and POST</a></li>
</ul>
</li>
<li><a class="reference internal" href="#cache-framework">Cache Framework</a><ul>
<li><a class="reference internal" href="#id11">Less code</a></li>
<li><a class="reference internal" href="#id12">Consistency</a></li>
<li><a class="reference internal" href="#id13">Extensibility</a></li>
</ul>
</li>
</ul>
</li>
</ul>

    
  

  
  <h2>Browse</h2>
  <ul>
    
    
    <li>Prev: <a href="../api-stability/">API stability</a></li>
    
    
    <li>Next: <a href="../distributions/">Third-party distributions of Django</a></li>
    
    <li><a href="https://docs.djangoproject.com/en/1.11/contents/">Table of contents</a></li>
    
    <li><a href="https://docs.djangoproject.com/en/1.11/genindex/">General Index</a></li>
    
    <li><a href="https://docs.djangoproject.com/en/1.11/py-modindex/">Python Module Index</a></li>
    
    
  </ul>
  

  
  <h2>You are here:</h2>
  <ul>
    <li>
      <a href="https://docs.djangoproject.com/en/1.11/">Django 1.11 documentation</a>
      
      <ul><li><a href="../">Meta-documentation and miscellany</a>
      
      <ul><li>Design philosophies</li></ul>
      </li></ul>
    </li>
  </ul>
  

  
  <h2 id="getting-help-sidebar">Getting help</h2>
  <dl class="list-links">
    <dt><a href="https://docs.djangoproject.com/en/1.11/faq/">FAQ</a></dt>
    <dd>Try the FAQ — it's got answers to many common questions.</dd>

    <dt><a href="/en/stable/genindex/">Index</a>, <a href="/en/stable/py-modindex/">Module Index</a>, or <a href="/en/stable/contents/">Table of Contents</a></dt>
    <dd>Handy when looking for specific information.</dd>

    <dt><a href="https://groups.google.com/group/django-users/">django-users mailing list</a></dt>
    <dd>Search for information in the archives of the django-users mailing list, or post a question.</dd>

    <dt><a href="irc://irc.freenode.net/django">#django IRC channel</a></dt>
    <dd>Ask a question in the #django IRC channel, or search the IRC logs to see if it’s been asked before.</dd>

    <dt><a href="https://code.djangoproject.com/">Ticket tracker</a></dt>
    <dd>Report bugs with Django or Django documentation in our ticket tracker.</dd>
  </dl>
  

  
  <h2>Download:</h2>
  <p>
    Offline (Django 1.11):
    <a href="/m/docs/django-docs-1.11-en.zip">HTML</a> |
    <a href="https://media.readthedocs.org/pdf/django/1.11.x/django.pdf">PDF</a> |
    <a href="https://media.readthedocs.org/epub/django/1.11.x/django.epub">ePub</a>
    <br>
    <span class="quiet">
      Provided by <a href="https://readthedocs.org/">Read the Docs</a>.
    </span>
  </p>
  
</div>

      

    </div>

     
     

    
    
    

    
      
<div role="contentinfo">
  <div class="subfooter">
    <div class="container">
      <h1 class="visuallyhidden">Django Links</h1>

      <div class="col learn">
        <h2>Learn More</h2>
        <ul>
          <li><a href="https://www.djangoproject.com/start/overview/">About Django</a></li>
          
          <li><a href="https://www.djangoproject.com/start/">Getting Started with Django</a></li>
          <li><a href="https://docs.djangoproject.com/en/dev/internals/organization/">Team Organization</a></li>
          <li><a href="https://www.djangoproject.com/foundation/">Django Software Foundation</a></li>
          <li><a href="https://www.djangoproject.com/conduct/">Code of Conduct</a></li>
          <li><a href="https://www.djangoproject.com/diversity/">Diversity Statement</a></li>
        </ul>
      </div>

      <div class="col involved">
        <h2>Get Involved</h2>
        <ul>
          <li><a href="https://www.djangoproject.com/community/">Join a Group</a></li>
          <li><a href="https://docs.djangoproject.com/en/dev/internals/contributing/">Contribute to Django</a></li>
          <li><a href="https://docs.djangoproject.com/en/dev/internals/contributing/bugs-and-features/">Submit a Bug</a></li>
          <li><a href="https://docs.djangoproject.com/en/dev/internals/security/#reporting-security-issues">Report a Security Issue</a></li>
        </ul>
      </div>

      <div class="col follow last-child">
        <h2>Follow Us</h2>
        <ul>
          <li><a href="https://github.com/django">GitHub</a></li>
          <li><a href="https://twitter.com/djangoproject">Twitter</a></li>
          <li><a href="https://www.djangoproject.com/rss/weblog/">News RSS</a></li>
          <li><a href="https://groups.google.com/forum/#!forum/django-users">Django Users Mailing List</a></li>
        </ul>
      </div>

    </div>
  </div>

  <div class="footer">
    <div class="container">
      <div class="footer-logo">
        <a class="logo" href="https://www.djangoproject.com/">Django</a>
      </div>
      <ul class="thanks">
        <li>
          <span>Hosting by</span> <a class="rackspace" href="https://www.rackspace.com">Rackspace</a>
          <span>Search by</span> <a class="elastic" href="https://www.elastic.co">Elastic Search</a>
        </li>
        <li class="design"><span>Design by</span> <a class="threespot" href="https://www.threespot.com">Threespot</a> <span class="ampersand">&amp;</span> <a class="andrevv" href="http://andrevv.com/"></a></li>
      </ul>
      <p class="copyright">&copy; 2005-2017
        <a href="https://www.djangoproject.com/foundation/"> Django Software
        Foundation</a> and individual contributors. Django is a
        <a href="https://www.djangoproject.com/trademarks/">registered
        trademark</a> of the Django Software Foundation.
      </p>
    </div>
  </div>

</div>

    

    
    <script>
    function extless(input) {
        return input.replace(/(.*)\.[^.]+$/, '$1');
    }
    var require = {
        shim: {
            'jquery': [],
            'jquery.inview': ["jquery"],
            'jquery.payment': ["jquery"],
            'jquery.flot': ["jquery"],
            'jquery.unveil': ["jquery"],
            'stripe': {
              exports: 'Stripe'
            }
        },
        paths: {
            "jquery": extless("/s/js/lib/jquery/dist/jquery.min.87e69028f78d.js"),
            "jquery.inview": extless("/s/js/lib/jquery.inview/jquery.inview.min.4edba1c65592.js"),
            "jquery.payment": extless("/s/js/lib/jquery.payment/lib/jquery.payment.e99c05ca79ae.js"),
            "jquery.unveil": extless("/s/js/lib/unveil/jquery.unveil.min.ac79eb277093.js"),
            "jquery.flot": extless("/s/js/lib/jquery-flot/jquery.flot.min.9964206e9d7f.js"),
            "clipboard": extless("/s/js/lib/clipboard/dist/clipboard.min.bd70fd596a23.js"),
            "mod/floating-warning": extless("/s/js/mod/floating-warning.a21b2abd2884.js"),
            "mod/list-collapsing": extless("/s/js/mod/list-collapsing.c1a08d3ef9e9.js"),
            "mod/list-feature": extless("/s/js/mod/list-feature.73529480f25b.js"),
            "mod/mobile-menu": extless("/s/js/mod/mobile-menu.841726ee903a.js"),
            "mod/version-switcher": extless("/s/js/mod/version-switcher.c28bb83972bb.js"),
            "mod/search-key": extless("/s/js/mod/search-key.f3c0a6fcfedd.js"),
            "mod/stripe-custom-checkout": extless("/s/js/mod/stripe-custom-checkout.aac1352045b7.js"),
            "mod/stripe-change-card": extless("/s/js/mod/stripe-change-card.682c710317a8.js"),
            "stripe-checkout": "https://checkout.stripe.com/checkout",
            "stripe": "https://js.stripe.com/v2/?"  // ? needed due to require.js
        }
    };
    </script>
    <script data-main="/s/js/main.3a2ae4b1529c.js" src="/s/js/lib/require.177879fbe7dd.js"></script>
    



  </body>
</html>
"""
