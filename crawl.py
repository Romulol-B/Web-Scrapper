import asyncio
from random import normalvariate
from sys import base_exec_prefix
from typing import TypedDict
from urllib.parse import urljoin

import aiohttp
import requests
from bs4 import BeautifulSoup, Tag


def extract_page_data(html: str, page_url: str) -> PageData:
    dict = {}
    dict["url"] = page_url
    dict["heading"] = get_heading_from_html(html)
    dict["first_paragraph"] = get_first_paragraph_from_html(html)
    dict["outgoing_links"] = get_urls_from_html(html, page_url)
    dict["image_urls"] = get_images_from_html(html, page_url)
    return dict


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


def _in_base_url(base_url, current_url) -> bool:
    l = len(base_url)
    if list(base_url) == list(current_url)[:l] or current_url[0] == "/":
        return True
    else:
        return False


def crawl_page(base_url, current_url=None, page_data=None):

    normalized_current_url = normalize_url(current_url)
    normalized_base_url = normalize_url(base_url)
    # if current_url[-1] == "/":
    #    current_url = base_url + current_url
    #    print("concatenacao:", current_url)
    if not _in_base_url(base_url, current_url):
        return
    if page_data is None:
        page_data = {}
    if page_data.get(normalized_current_url, -1) != -1:
        return
    html_pag = get_html(current_url)
    corrent_page_data = extract_page_data(html_pag, current_url)
    page_data[corrent_page_data["url"]] = corrent_page_data

    for url in corrent_page_data["outgoing_links"]:
        if url not in page_data.keys():
            crawl_page(base_url, url, page_data)
    return page_data


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
