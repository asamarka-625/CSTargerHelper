from typing import Tuple
import requests
from bs4 import BeautifulSoup


def get_response(url: str) -> bytes:
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        return response.content
        
    except requests.exceptions.RequestException as err:
        print(f"Error fetching the URL: {err}")
    
    except Exception as err:
        prnit(f"Unexpected error: {err}")
 

def get_name_and_link(content: bytes) -> Tuple[str, str]:
    soup = BeautifulSoup(content, "html.parser")
    blocks = soup.find_all("div", class_="blog-post-content")
    
    result = []
    for block in blocks:
        block_a = block.find("a")
        name = block_a.text.strip()
        link = block_a.get("href")
        result.append((name, link))
    
    return result
    

def get_image_and_step(content: bytes) -> Tuple[str, str]:
    soup = BeautifulSoup(content, "html.parser")
    slides = soup.find_all("div", class_="multiphoto-box")
    
    result = []
    for slide in slides:
        step = slide.find("span").text.strip()
        image_link = slide.find("img").get("src")
        result.append((step, image_link))
    
    return result
    
    
if __name__ == "__main__":
    url_base = "https://раскидки-гранат.рф/"
    url = "https://раскидки-гранат.рф/raskidki-granat-counter-strike-2/dust-2/"
    
    print(f"Parse {url}")
    content1 = get_response(url=url)
    data1 = get_name_and_link(content1)
    
    print(f"Parse {data1[0][0]}: {data1[0][1]}")
    content2 = get_response(url=f"{url_base}{data1[0][1]}")
    data2 = get_name_and_link(content2)
    
    for name, link in data2:
        print(f"Parse {name}: {link}")
        content3 = get_response(url=f"{url_base}{link}")
        data3 = get_image_and_step(content3)
        
        for d3 in data3:
            print(d3)