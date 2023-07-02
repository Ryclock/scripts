import requests
from bs4 import BeautifulSoup
import html


class WebScraper:
    def __init__(self, url, mobile):
        self.url = url
        self.mobile = mobile
        self.post_id = self.extract_post_id()

    def extract_post_id(self):
        return self.url.split("/")[-1].split(".")[0]

    def get_page_content(self):
        return requests.get(self.url).text

    def extract_text_content(self, page_content):
        soup = BeautifulSoup(page_content, "html.parser")
        div_element = soup.find("div", class_="content22")
        if not div_element:
            return ""

        paragraphs = div_element.find_all("p")
        text_content = ""
        for paragraph in paragraphs:
            paragraph_text = paragraph.get_text(separator="\n", strip=True)
            images = paragraph.find_all("img")
            for img in images:
                src = img.get("src")
                if src:
                    paragraph_text += f"---picture URL---\n{src}\n----------"
            paragraph_text = html.unescape(paragraph_text)
            paragraph_text = paragraph_text.replace(
                "\u200e", "").replace("\u200f", "")
            text_content += "\n"+paragraph_text + "\n"

        return text_content

    def save_to_file(self, content, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

    def check_and_submit_form(self):
        soup = BeautifulSoup(self.get_page_content(), "html.parser")
        link = soup.find("a", class_="zhi12-popup zhi12-widget")
        if link:
            link_url = link["href"]
            response = requests.get(link_url)
            response_soup = BeautifulSoup(response.text, "html.parser")
            codecheck_key_input = response_soup.find(
                "input", {"name": "codecheck_key"})
            form_data = {
                "mobile": self.mobile,
                "post_id": self.post_id,
                "op": "提交",
                "codecheck_key": codecheck_key_input["value"],
            }
            return requests.post(link_url, data=form_data).text

        return self.get_page_content()

    def scrape(self):
        submitted_content = self.check_and_submit_form()
        extracted_content = self.extract_text_content(submitted_content)
        self.save_to_file(extracted_content, "question_bank.txt")
