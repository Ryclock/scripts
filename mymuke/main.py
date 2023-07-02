from scraper import WebScraper

if __name__ == "__main__":
    url = "https://www.mymuke.com/xxxxx.html"
    mobile = "YouPhoneNumber"
    scraper = WebScraper(url, mobile)
    scraper.scrape()
