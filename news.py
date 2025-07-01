import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# --------- SCRAPER 1: The Hacker News ---------
def get_hacker_news_selenium():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0")

    driver_path = r"C:\Users\ThomasRutt\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Your chromedriver path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://thehackernews.com")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = ["🛡️ TOP 5 CYBERSECURITY STORIES - TheHackerNews:\n"]

    articles = soup.find_all("div", class_="body-post")[:5]
    for article in articles:
        title_tag = article.find("h2", class_="home-title")
        title = title_tag.text.strip() if title_tag else "No title"
        link_tag = article.find("a")
        link = link_tag["href"] if link_tag else "No link"
        results.append(f"🔹 {title}\n🔗 {link}\n")

    return "\n".join(results)

# --------- SCRAPER 2: Reddit Cybersecurity (hot posts) ---------
def get_reddit_cyber_posts():
    url = "https://www.reddit.com/r/cybersecurity/hot.json?limit=5"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    posts = response.json()["data"]["children"]

    results = ["🧠 REDDIT - r/cybersecurity (Top Posts):\n"]
    for post in posts:
        title = post["data"]["title"]
        permalink = "https://reddit.com" + post["data"]["permalink"]
        results.append(f"🔸 {title}\n🔗 {permalink}\n")

    return "\n".join(results)


# --------- SEND EMAIL ---------
def send_email_digest(content):
    EMAIL_ADDRESS = "email@gmail.com" # Replace with email
    EMAIL_PASSWORD = "APP_PASSWORD"  # Replace with your actual Gmail app password

    msg = EmailMessage()
    msg["Subject"] = "🧠 Your Cybersecurity & Cloud Digest"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "email@gmail.com"  # Change if you want to send to a different email
    msg.set_content(content)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# --------- MAIN ---------
if __name__ == "__main__":
    print("🔍 Gathering content...")

    news = get_hacker_news_selenium()
    reddit = get_reddit_cyber_posts()


    full_digest = f"{news}\n\n{reddit}"
    send_email_digest(full_digest)

    print("✅ Email sent to email@gmail.com!")
