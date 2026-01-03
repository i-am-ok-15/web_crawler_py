from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.netloc}{parsed_url.path}"
    if normalized_url[-1] == "/":
        return normalized_url[:-1]
    else:
        return normalized_url

def get_h1_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    if soup.h1 == None:
        return ""
    return soup.h1.get_text()

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    
    main_section = soup.find("main")
    if main_section:
        first_p = main_section.find("p")
    else:
        first_p = soup.find("p")

    return first_p.get_text(strip=True) if first_p else ""

def get_url_links_from_html(html, base_url):
    url_links = []
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        link = urljoin(base_url, link.get("href"))
        url_links.append(link)
    return url_links

def get_image_links_from_html(html, base_url):
    image_links = []
    soup = BeautifulSoup(html, "html.parser")
    if not soup:
        return ""
    for image in soup.find_all("img"):
        image = urljoin(base_url, image.get("src"))
        image_links.append(image)
    return image_links

def extract_page_data(input_body, input_url):
    extracted_page_data = {
        "url": str(input_url),
        "h1": get_h1_from_html(input_body),
        "first_paragraph": get_first_paragraph_from_html(input_body),
        "outgoing_links": get_url_links_from_html(input_body, input_url),
        "image_urls": get_image_links_from_html(input_body, input_url)
    }
    return extracted_page_data