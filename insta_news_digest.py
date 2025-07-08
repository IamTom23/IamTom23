import os
import time
import smtplib
import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_instagram_ready_news():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://thehackernews.com")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    article = soup.find("div", class_="body-post")
    title_tag = article.find("h2", class_="home-title")
    link_tag = article.find("a")
    title = title_tag.text.strip() if title_tag else "No title"
    link = link_tag["href"] if link_tag else "No link"

    # Get summary from the article
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(link)
    time.sleep(3)
    article_soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    paragraphs = article_soup.select("div.articlebody > p")
    summary = ""
    for p in paragraphs:
        text = p.get_text(strip=True)
        if text and len(summary) < 500:
            summary += text + " "
    summary = summary.strip()

    return {
        "title": title,
        "link": link,
        "script": f"🎙️ Cyber Alert!\n\n{title}\n\nIn under 60 seconds, here’s what you need to know:\n\n{summary}\n\nWant the full story? Check the link in bio! 🔗\n#CyberSecurity #News #TheHackerNews"
    }


def send_email(script_data):
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = f"📢 Instagram Cyber News Script: {script_data['title'][:50]}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content(script_data["script"])

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


if __name__ == "__main__":
    print("🔍 Fetching latest cybersecurity news...")
    news = get_instagram_ready_news()
    print("✉️ Sending Instagram script to your email...")
    send_email(news)
    print("✅ Done.")
