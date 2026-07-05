import unittest

from crawl import get_first_paragraph_from_html, get_heading_from_html, normalize_url


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


if __name__ == "__main__":
    unittest.main()
