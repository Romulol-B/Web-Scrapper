import xml
from cmath import isinf
from pydoc import html

from bs4 import BeautifulSoup, Tag

from crawl import normalize_url


def main():
    html_full = """<html><body>
                <h2>Outside paragraph.</h2>
                <main>
                    <p>Main paragraph.</p>
                </main>
            </body></html>"""
    print(html_full)


if __name__ == "__main__":
    main()
