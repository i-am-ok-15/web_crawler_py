import unittest
from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html, get_url_links_from_html, get_image_links_from_html, extract_page_data

class TestURLMethods(unittest.TestCase):

    def test_normalize_url_https_trailing(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_https_no_trailing(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http_trailing(self):
        input_url = "http://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http_no_trailing(self):
        input_url = "http://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)
    
    def test_get_h1_from_html(self):
        input_html = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""

        actual = get_h1_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_happy_path(self):
        input_html = """<html>
    <body>
        <h1>Main Heading</h1>
        <p>This is the first paragraph.</p>
        <p>This is a second paragraph.</p>
    </body>
</html>"""

        actual = get_h1_from_html(input_html)
        expected = "Main Heading"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_nested_and_siblings(self):
        input_html = """<html>
    <body>
        <div>
            <span>Welcome Guest</span>
            <h1>Article Title</h1>
        </div>
        <section>
            <p>The actual content starts here.</p>
        </section>
    </body>
</html>"""

        actual = get_h1_from_html(input_html)
        expected = "Article Title"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_empty_tags(self):
        input_html = """<html>
    <body>
        <h1 class="title-main" id="top">Title with Attributes</h1>
        <p></p>
        <p>Text in the second paragraph.</p>
    </body>
</html>"""

        actual = get_h1_from_html(input_html)
        expected = "Title with Attributes"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_inner_tags(self):
        input_html = """<html>
    <body>
        <h1>Breaking <i>News</i> Today</h1>
        <p>Visit our <a href="/home">website</a> for <b>more</b> info.</p>
    </body>
</html>"""

        actual = get_h1_from_html(input_html)
        expected = "Breaking News Today"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html(self):

        input_html = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""

        actual = get_first_paragraph_from_html(input_html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_happy_path(self):

        input_html = """<html>
    <body>
        <h1>Main Heading</h1>
        <p>This is the first paragraph.</p>
        <p>This is a second paragraph.</p>
    </body>
</html>"""

        actual = get_first_paragraph_from_html(input_html)
        expected = "This is the first paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_nested_and_siblings(self):

        input_html = """<html>
    <body>
        <div>
            <span>Welcome Guest</span>
            <h1>Article Title</h1>
        </div>
        <section>
            <p>The actual content starts here.</p>
        </section>
    </body>
</html>"""

        actual = get_first_paragraph_from_html(input_html)
        expected = "The actual content starts here."
        self.assertEqual(actual, expected)

    def test_get_p_from_html_empty_tags(self):
        input_html = """<html>
    <body>
        <h1 class="title-main" id="top">Title with Attributes</h1>
        <p></p>
        <p>Text in the second paragraph.</p>
    </body>
</html>"""

        actual = get_first_paragraph_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_p_from_html_inner_tags(self):
        input_html = """<html>
    <body>
        <h1>Breaking <i>News</i> Today</h1>
        <p>Visit our <a href="/home">website</a> for <b>more</b> info.</p>
    </body>
</html>"""

        actual = get_first_paragraph_from_html(input_html)
        expected = "Visit our website for more info."
        self.assertEqual(actual, expected)

    def test_get_url_links_happy_path(self):
        input_html = """<html>
    <body>
        <h1>Welcome to Boot.dev</h1>
        <p>Learn backend development <a href="https://boot.dev">here</a>.</p>
        <img src="https://boot.dev/images/hero.png" alt="Hero Image">
    </body>
</html>"""
        base_url = "https://boot.dev"
        actual = get_url_links_from_html(input_html, base_url)
        expected = ['https://boot.dev']
        self.assertEqual(actual, expected)

    def test_get_url_links_empty_case(self):
        input_html = """<html>
    <body>
        <p>This is a plain text paragraph.</p>
        <div>There are no links or images in this section.</div>
    </body>
</html>"""
        base_url = "https://boot.dev"
        actual = get_url_links_from_html(input_html, base_url)
        expected = []       
        self.assertEqual(actual, expected)

    def test_get_url_links_relative_path(self):
        input_html = """<ul>
    <li><a href="/courses/python">Python Course</a></li>
    <li><a href="/courses/golang">Go Course</a></li>
    <li><img src="/assets/badges/python-badge.png" alt="Python Badge"></li>
    <li><img src="/assets/badges/go-badge.png" alt="Go Badge"></li>
</ul>"""
        base_url = "https://boot.dev"
        actual = get_url_links_from_html(input_html, base_url)
        expected = ['https://boot.dev/courses/python', 'https://boot.dev/courses/golang']     
        self.assertEqual(actual, expected)
    
    def test_get_url_links_nested_elements(self):
        input_html = """<div class="footer">
    <a href="https://twitter.com/bootdotdev">
        <img src="https://boot.dev/icons/twitter.svg" alt="Twitter">
    </a>
    <a href="https://github.com/bootdotdev">
        <img src="https://boot.dev/icons/github.svg" alt="GitHub">
    </a>
</div>"""
        base_url = "https://boot.dev"
        actual = get_url_links_from_html(input_html, base_url)
        expected = ['https://twitter.com/bootdotdev', 'https://github.com/bootdotdev']      
        self.assertEqual(actual, expected)
    
    def test_get_url_links_mixed_quotes_attributes(self):
        input_html = """<div>
    <a class="btn" href='https://blog.boot.dev/news'>News</a>
    <img class='avatar' src="/images/user_123.jpg" width="500">
    <a href="mailto:contact@boot.dev">Contact Us</a>
</div>"""
        base_url = "https://boot.dev"
        actual = get_url_links_from_html(input_html, base_url)
        expected = ['https://blog.boot.dev/news', 'mailto:contact@boot.dev']     
        self.assertEqual(actual, expected)

    def test_get_image_links_happy_path(self):
        input_html = """<html>
    <body>
        <h1>Welcome to Boot.dev</h1>
        <p>Learn backend development <a href="https://boot.dev">here</a>.</p>
        <img src="https://boot.dev/images/hero.png" alt="Hero Image">
    </body>
</html>"""
        base_url = "https://boot.dev"
        actual = get_image_links_from_html(input_html, base_url)
        expected = ['https://boot.dev/images/hero.png']       
        self.assertEqual(actual, expected)

    def test_get_image_links_empty_case(self):
        input_html = """<html>
    <body>
        <p>This is a plain text paragraph.</p>
        <div>There are no links or images in this section.</div>
    </body>
</html>"""
        base_url = "https://boot.dev"
        actual = get_image_links_from_html(input_html, base_url)
        expected = []       
        self.assertEqual(actual, expected)
    
    def test_get_image_links_relative_path(self):
        input_html = """<ul>
    <li><a href="/courses/python">Python Course</a></li>
    <li><a href="/courses/golang">Go Course</a></li>
    <li><img src="/assets/badges/python-badge.png" alt="Python Badge"></li>
    <li><img src="/assets/badges/go-badge.png" alt="Go Badge"></li>
</ul>"""
        base_url = "https://boot.dev"
        actual = get_image_links_from_html(input_html, base_url)
        expected = ['https://boot.dev/assets/badges/python-badge.png', 'https://boot.dev/assets/badges/go-badge.png']    
        self.assertEqual(actual, expected)
    
    def test_get_image_links_nested_elements(self):
        input_html = """<div class="footer">
    <a href="https://twitter.com/bootdotdev">
        <img src="https://boot.dev/icons/twitter.svg" alt="Twitter">
    </a>
    <a href="https://github.com/bootdotdev">
        <img src="https://boot.dev/icons/github.svg" alt="GitHub">
    </a>
</div>"""
        base_url = "https://boot.dev"
        actual = get_image_links_from_html(input_html, base_url)
        expected = ['https://boot.dev/icons/twitter.svg', 'https://boot.dev/icons/github.svg']       
        self.assertEqual(actual, expected)
    
    def test_get_image_links_mixed_quotes_attributes(self):
        input_html = """<div>
    <a class="btn" href='https://blog.boot.dev/news'>News</a>
    <img class='avatar' src="/images/user_123.jpg" width="500">
    <a href="mailto:contact@boot.dev">Contact Us</a>
</div>"""
        base_url = "https://boot.dev"
        actual = get_image_links_from_html(input_html, base_url)
        expected = ['https://boot.dev/images/user_123.jpg']
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_happy_path(self):
        input_url = "https://blog.boot.dev"
        input_body = """<html>
        <body>
            <h1>The Future of Backend</h1>
            <p>Backend development is evolving rapidly with new tools.</p>
            <a href="https://boot.dev/blog">Read Blog</a>
            <img src="https://boot.dev/hero.jpg" alt="Hero">
        </body>
    </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
        "url": "https://blog.boot.dev",
        "h1": "The Future of Backend",
        "first_paragraph": "Backend development is evolving rapidly with new tools.",
        "outgoing_links": ["https://boot.dev/blog"],
        "image_urls": ["https://boot.dev/hero.jpg"]
    }
        self.assertEqual(actual, expected)

    def test_extract_page_data_relative_paths_and_multiple_items(self):
        input_url = "https://blog.boot.dev"
        input_body = """<html>
        <body>
            <h1>Course Catalog</h1>
            <div>
                <p>Browse our full list of courses below.</p>
                <ul>
                    <li><a href="/courses/python">Python</a></li>
                    <li><a href="/courses/go">Go</a></li>
                </ul>
                <img src="/icons/python.png">
                <img src="/icons/go.png">
            </div>
        </body>
    </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
        "url": "https://blog.boot.dev",
        "h1": "Course Catalog",
        "first_paragraph": "Browse our full list of courses below.",
        "outgoing_links": [
            "https://blog.boot.dev/courses/python",
            "https://blog.boot.dev/courses/go"
        ],
        "image_urls": [
            "https://blog.boot.dev/icons/python.png",
            "https://blog.boot.dev/icons/go.png"
        ]
    }
        self.assertEqual(actual, expected)

    def test_extract_page_data_nested_tags(self):
        input_url = "https://blog.boot.dev"
        input_body = """<html>
        <body>
            <div>
                <h1>Welcome to <i>Boot.dev</i></h1>
                <section>
                    <p>Start your <b>coding adventure</b> today.</p>
                    <a href="https://twitter.com/bootdotdev"><img src="https://boot.dev/twitter.svg"></a>
                </section>
            </div>
        </body>
    </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
        "url": "https://blog.boot.dev",
        "h1": "Welcome to Boot.dev",
        "first_paragraph": "Start your coding adventure today.",
        "outgoing_links": ["https://twitter.com/bootdotdev"],
        "image_urls": ["https://boot.dev/twitter.svg"]
    }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_links_or_images(self):
        input_url = "https://blog.boot.dev"
        input_body = """<html>
        <body>
            <h1>Privacy Policy</h1>
            <p>We do not store your data. This is a static page.</p>
            <p>If you have questions, mail us.</p>
        </body>
    </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
        "url": "https://blog.boot.dev",
        "h1": "Privacy Policy",
        "first_paragraph": "We do not store your data. This is a static page.",
        "outgoing_links": [],
        "image_urls": []
    }
        self.assertEqual(actual, expected)

    def test_extract_page_data_messy_attributes(self):
        input_url = "https://blog.boot.dev"
        input_body = """<html>
        <body>
            <h1 class='main-title'>Community Guidelines</h1>
            <p class="intro">Please be respectful to everyone.</p>
            <a href= 'https://discord.gg/bootdotdev' >Join Discord</a>
            <img src='/assets/logo_small.png' class="logo" />
        </body>
    </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
        "url": "https://blog.boot.dev",
        "h1": "Community Guidelines",
        "first_paragraph": "Please be respectful to everyone.",
        "outgoing_links": ["https://discord.gg/bootdotdev"],
        "image_urls": ["https://blog.boot.dev/assets/logo_small.png"]
    }
        self.assertEqual(actual, expected)
                            
if __name__ == '__main__':
    unittest.main()