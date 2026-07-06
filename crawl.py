from typing import TypedDict
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


def get_html(url):
    request = requests.get(url, headers={"User-agent": "BootCrawler/1.0"})
    if request.status_code >= 400:
        raise Exception(request.status_code)
    html = request.text
    if isinstance(html, str):
        return html
    else:
        print("erro")
        raise Exception("headers,content-type not a string")


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
    # print(soup)
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


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def extract_page_data(html: str, page_url: str) -> PageData:
    dict = {}
    dict["url"] = page_url
    dict["heading"] = get_heading_from_html(html)
    dict["first_paragraph"] = get_first_paragraph_from_html(html)
    dict["outgoing_links"] = get_urls_from_html(html, page_url)
    dict["image_urls"] = get_images_from_html(html, page_url)
    return dict
