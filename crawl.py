import asyncio
from asyncio.tasks import create_task
from random import normalvariate
from sys import base_exec_prefix
from types import TracebackType
from typing import TypedDict
from urllib.parse import urljoin

import aiohttp
import requests
from bs4 import BeautifulSoup, Tag
from requests.compat import urlparse


class AsyncCrawler:
    def __init__(
        self,
        base_url,
    ) -> None:
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 3
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "AsyncCrawler":
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        assert self.session is not None
        await self.session.close()

    async def add_page_visit(self, normalized_url) -> bool:
        async with self.lock:
            if normalized_url not in self.page_data:
                return True
            else:
                return False

    async def get_html(self, url):
        try:
            assert self.session is not None
            async with self.session.get(
                url, headers={"User-agent": "BootCrawler/1.0"}
            ) as response:
                if response.status >= 400:
                    raise Exception(response.status)

                html = await response.text()
                if isinstance(html, str):
                    return html
                else:
                    print("erro")
                    raise Exception("headers,content-type not a string")
        except Exception as e:
            print(f"error fetching {url}: {e}")

    async def crawl_page(self, current_url=""):
        url_obj = urlparse(current_url)
        if url_obj.netloc != self.base_domain:
            return

        normalized_current_url = normalize_url(current_url)

        add_page_task = asyncio.create_task(self.add_page_visit(normalized_current_url))
        if not await add_page_task:
            return

        if self.page_data.get(normalized_current_url, -1) != -1:
            return

        async with self.semaphore:
            print(
                f"Crawling {current_url} active:{(self.max_concurrency - self.semaphore._value)} "
            )
            html = await self.get_html(current_url)
            if html is None:
                return
            corrent_page_data = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_current_url] = corrent_page_data

            next_urls = get_urls_from_html(html, self.base_url)

        tasks: list[asyncio.Task[None]] = []
        for next_url in next_urls:
            tasks.append(asyncio.create_task(self.crawl_page(next_url)))

        if tasks:
            await asyncio.gather(*tasks)

    async def crawl(self) -> dict[str, PageData]:
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(base_url):
    async with AsyncCrawler(base_url) as crawler:
        return crawler.crawl()


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def extract_page_data(html: str, page_url: str) -> PageData:
    dict: PageData = {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }

    return dict


def _in_base_url(base_url, current_url) -> bool:
    l = len(base_url)
    if list(base_url) == list(current_url)[:l] or current_url[0] == "/":
        return True
    else:
        return False


# %%
def normalize_url(full_link: str) -> str:
    http_ignore = ["https://", "http://"]
    last_bar = "/"
    end = len(full_link)
    start = 0
    for pattern in http_ignore:
        if pattern in full_link:
            start = len(pattern)
            break
    if last_bar == full_link[-1]:
        end -= 1
    return "".join(list(full_link)[start:end])


def get_heading_from_html(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "xml")
    h_txt = soup.find("h1")
    if not h_txt:
        h_txt = soup.find("h2")
    return h_txt.get_text(strip=True) if isinstance(h_txt, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    # trying to find by first loking at main
    main_body = soup.find("main")
    if main_body:
        paragraph = main_body.find("p")
        if isinstance(paragraph, Tag):
            return paragraph.get_text(strip=True)
    paragraph = soup.find("p")
    return paragraph.get_text(strip=True) if isinstance(paragraph, Tag) else ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links = soup.findAll("a")
    url_vector = []
    for tag_a in links:
        url = tag_a.get("href")
        if list(url)[0] == "/":  # relative
            url_vector.append(urljoin(base_url, url))
        else:  # absolute
            url_vector.append(url)

    return url_vector


def get_images_from_html(html: str, base_url) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    imgs = soup.findAll("img")
    img_src_list = []
    for img in imgs:
        img_src = img.get("src")
        if list(img_src)[0] == "/":  # relative
            img_src_list.append(urljoin(base_url, img_src))
        else:  # absolute
            img_src_list.append(img_src)
    return img_src_list
