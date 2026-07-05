from bs4 import BeautifulSoup, Tag


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
