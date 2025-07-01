import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup browser options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0")

# Path to your chromedriver.exe — update if needed
driver_path = r"C:\Users\ThomasRutt\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=options)

# Job search parameters
job_title = "azure"
location = "Brisbane"
url = f"https://www.seek.com.au/{job_title}-jobs/in-{location.lower()}"

driver.get(url)

# Wait until job cards are loaded on page
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="job-card"]'))
)

# Find all job cards
job_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="job-card"]')

print(f"\n✅ Found {len(job_cards)} job listings:\n")

# Open CSV file for writing
with open("seek_jobscloudazure.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["Job Title", "Company", "Location", "Job Link", "Description"])

    for card in job_cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, 'a[data-automation="jobTitle"]').text
            link = card.find_element(By.CSS_SELECTOR, 'a[data-automation="jobTitle"]').get_attribute("href")
            company = card.find_element(By.CSS_SELECTOR, '[data-automation="jobCompany"]').text
            location = card.find_element(By.CSS_SELECTOR, '[data-automation="jobLocation"]').text
            try:
                desc = card.find_element(By.CSS_SELECTOR, '[data-automation="jobShortDescription"]').text
            except:
                desc = "No description available"

            print(f"🔹 {title}")
            print(f"🏢 {company}")
            print(f"📍 {location}")
            print(f"🔗 {link}")
            print(f"📝 {desc}")
            print("-" * 80)

            writer.writerow([title, company, location, link, desc])
        except Exception as e:
            print("❌ Error scraping job card:", e)

driver.quit()
