import os
import time
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables
load_dotenv()
USERNAME = os.getenv('1337_USERNAME')
PASSWORD = os.getenv('1337_PASSWORD')

EMAIL_FROM = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

POLL_INTERVAL = 20  # seconds
SITE_URL = "https://admission.1337.ma/users/sign_in"
POOL_URL = "https://admission.1337.ma/candidature/piscine"
last_notification_hash = None

# ---- Email Notification Function ----
def send_email_notification(subject, body):
    message = MIMEMultipart()
    message["From"] = EMAIL_FROM
    message["To"] = EMAIL_TO
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, message.as_string())
            print("📧 Email notification sent.")
            return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

# ---- Hash Pool Section for Change Detection ----
def get_pool_section_hash(page):
    section = page.query_selector('div.flex.flex-col.justify-center.items-center.bg-gray-100')
    if section:
        content = section.inner_html()
        return hashlib.md5(content.encode()).hexdigest()
    return None

# ---- Pool Page Monitor ----
def monitor_pool_page():
    print(f"Logging in with username: {USERNAME}")
    global last_notification_hash
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # set to False if you want to see the browser UI
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe"
        )
        context = browser.new_context(user_agent="Mozilla/5.0")

        # Clear cookies if any (should be empty on new_context, but just in case)
        context.clear_cookies()

        # Create a page to clear localStorage and sessionStorage
        page = context.new_page()

        # Now navigate to the login page
        page.goto(SITE_URL, wait_until="domcontentloaded")

        # Wait for input fields
        page.wait_for_selector('input[name="email"]', timeout=10000)
        page.fill('input[name="email"]', USERNAME)

        page.wait_for_selector('input[name="password"]', timeout=10000)
        page.fill('input[name="password"]', PASSWORD)

        page.click('button[type="submit"]')

        # Or wait a bit and check URL manually
        time.sleep(20)
        if page.is_visible('text="Invalid email or password"'):
            print("❌ Login failed: invalid credentials.")
            return

        current_url = page.url
        print(f"Current URL after login: {current_url}")
        if "/users/sign_in" in current_url:
            print("Login failed or URL pattern changed.")
            return  # Stop or handle login failure
        else:
            print("Login successful, proceeding...")

        while True:
            try:
                page.goto(POOL_URL, wait_until="domcontentloaded", timeout=15000)

                if page.title() == "Access Denied" or "403" in page.content():
                    print("🚫 Blocked (403) - stopping")
                    send_email_notification("🚫 1337 Monitor Blocked", "Firewall or access restriction detected.")
                    break

                current_hash = get_pool_section_hash(page)
                placeholder_present = page.is_visible('text="Any available Pool will appear here"')

                if not placeholder_present and current_hash and current_hash != last_notification_hash:
                    subject = "🚨 POOL AVAILABLE at 1337!"
                    body = f"A new pool has been posted!\n\nCheck it here: {POOL_URL}"
                    if send_email_notification(subject, body):
                        last_notification_hash = current_hash

                print(f"[{time.strftime('%H:%M:%S')}] Pool status: {'Available' if not placeholder_present else 'Not available'}")
                time.sleep(POLL_INTERVAL)

            except Exception as e:
                print(f"⚠️ Error: {str(e)} - retrying in 60 seconds...")
                time.sleep(60)

# ---- Run Bot ----
if __name__ == "__main__":
    monitor_pool_page()
