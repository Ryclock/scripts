import argparse
import requests
from bs4 import BeautifulSoup
import time
import os


def create_temp_directory():
    timestamp = int(time.time())
    temp_dir = f"temp_dir_{timestamp}"
    os.makedirs(temp_dir)
    return temp_dir


def extract_toc_and_title(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(
            f"Error: Failed to fetch URL {url}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.find('h1', class_='Post-Title')
    catalog_elements = soup.find_all(
        ['h2', 'h3'], attrs={"data-into-catalog-status": True})

    title = title_element.get_text() if title_element else "No Title"
    toc_content = ""

    for catalog_element in catalog_elements:
        text_content = catalog_element.get_text()
        toc_content += text_content + "\n"

    return title, toc_content


def save_to_file(output_dir, url, title, toc_content):
    filename = "".join(c if c.isalnum() else "_" for c in url)
    file_path = os.path.join(output_dir, f"{filename}.txt")
    with open(file_path, "w", encoding="utf-8") as output_file:
        output_file.write(title + "\n\n" + toc_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Zhihu Table of Contents Extractor")
    parser.add_argument(
        "--file", help="Specify a file containing a list of URLs.")
    parser.add_argument("--url", nargs='+',
                        help="Specify one or more URLs separated by spaces")

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as file:
            urls = file.read().splitlines()
    elif args.url:
        urls = args.url
    else:
        parser.print_help()
        exit(1)

    output_dir = create_temp_directory()
    print(f"Output directory: {output_dir}")

    for url in urls:
        title, toc_content = extract_toc_and_title(url)
        if title or toc_content:
            save_to_file(output_dir, url, title, toc_content)
