import unittest

from crawl import (
    extract_page_data,
    get_first_paragraph_from_html,
    get_heading_from_html,
    get_images_from_html,
    get_urls_from_html,
    normalize_url,
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        input_url2 = "http://www.boot.dev/blog/path"
        input_url3 = "https://www.boot.dev/blog/path/"

        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"

        self.assertEqual(actual, expected)
        actual = normalize_url(input_url2)

        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
        actual = normalize_url(input_url3)

        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_empty(self):
        input_body = "<html><body>Test Title</body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic_on_h2(self):
        input_body = "<html><body><h2>Test Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority_empty_main(self):
        html_full2 = """<html><body>
                    <h2>Outside paragraph.</h2>
                    <main>
                    </main>
                    <p>Main paragraph.outside main</p>
                </body></html>"""
        actual = get_first_paragraph_from_html(html_full2)
        expected = "Main paragraph.outside main"
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_on_paragraph(self):
        input_url = "https://crawler-test.com.br"
        input_body = """<html><body><p>
        <a href="https://crawler-test.com.br"></p>
        <span>Boot.dev</span></a></body></html>
        """
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com.br"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_on_header(self):
        input_url = "https://crawler-test.com.br"
        input_body = """<html><body><h1>
            <a href="https://crawler-test.com.br"></h1>
            <p> paragrafo normal</p>
            <span>Boot.dev</span></a></body></html>
            """
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com.br"]
        self.assertEqual(actual, expected)

    def test_get__relative_urls_from_html_on_header(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body><h1>
            <a href="/image_pa"></h1>
            <p> paragrafo normal</p>
            <span>Boot.dev</span></a></body></html>
            """
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/image_pa"]
        self.assertEqual(actual, expected)

    def test_get__image_from_html_header(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body><h1>
            <img src="/big_logo.png"></h1>
            <p> paragrafo normal</p>
            <span>Boot.dev</span></a></body></html>
            """
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/big_logo.png"]
        self.assertEqual(actual, expected)

    def test_get__image_from_html_main(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body><main>
            <img src="/big_logo.png"></main>
            <p> paragrafo normal</p>
            <span>Boot.dev</span></a></body></html>
            """
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/big_logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://www.big_logos/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://www.big_logos/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute_multiple_images_multiple_tags(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        <h1>  <img src="https://www.big_logos/logo.png" alt="Logo"></h1>
        <p> <img src="https://www.big_logos/big_logo.png" alt="BigLogo"></p>
        <img src="https://www.big_logos/very_big_logo.png" alt="VeryBigLogo">
        </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://www.big_logos/logo.png",
            "https://www.big_logos/big_logo.png",
            "https://www.big_logos/very_big_logo.png",
        ]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute_multiple_images(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        <img src="https://www.big_logos/logo.png" alt="Logo">
        <img src="https://www.big_logos/big_logo.png" alt="BigLogo">
        <img src="https://www.big_logos/very_big_logo.png" alt="VeryBigLogo">
        </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://www.big_logos/logo.png",
            "https://www.big_logos/big_logo.png",
            "https://www.big_logos/very_big_logo.png",
        ]
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_complex(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title + a link</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <a href="/link2">Link 2</a>
            <p>
            <img src="/complex.png" alt="Image 2">
            <img src="/image1.jpg" alt="Image 1"></p>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title + a link",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [
                "https://crawler-test.com/link1",
                "https://crawler-test.com/link2",
            ],
            "image_urls": [
                "https://crawler-test.com/complex.png",
                "https://crawler-test.com/image1.jpg",
            ],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_real_site(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title + a link</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <a href="/link2">Link 2</a>
            <p>
            <img src="/complex.png" alt="Image 2">
            <img src="/image1.jpg" alt="Image 1"></p>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title + a link",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [
                "https://crawler-test.com/link1",
                "https://crawler-test.com/link2",
            ],
            "image_urls": [
                "https://crawler-test.com/complex.png",
                "https://crawler-test.com/image1.jpg",
            ],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_paragraph_main(self):

        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title + a link</h1>
            <p>This is the first paragraph.</p>
            <main>
            <a href="/link1">Link 1</a>
            <a href="/link2">Link 2</a>
            <p> paragrafo verdadeiro</p></main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title + a link",
            "first_paragraph": "paragrafo verdadeiro",
            "outgoing_links": [
                "https://crawler-test.com/link1",
                "https://crawler-test.com/link2",
            ],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)


def test_extract_page_data_empty(self):

    input_url = "https://crawler-test.com"
    input_body = """<html><body>
            <p></p>
            <main>
            <p>pipi popop </p></main>
        </body></html>"""
    actual = extract_page_data(input_body, input_url)
    expected = {
        "url": "https://crawler-test.com",
        "heading": "",
        "first_paragraph": "",
        "outgoing_links": [],
        "image_urls": [],
    }
    self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
