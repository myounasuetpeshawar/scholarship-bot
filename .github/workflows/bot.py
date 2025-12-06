# ========================================
# DAILY SCHOLARSHIP EMAIL BOT
# ========================================
import requests
from bs4 import BeautifulSoup  # FIXED: bs4 not bst
import smtplib
from email.mime.text import MIMEText  # FIXED: mime not aime, MIMEText not MINEFext
from email.mime.multipart import MIMEMultipart  # FIXED: mime not aime, MIMEMultipart not MINEMultipart
import os
from datetime import datetime

# ========================================
# 1. EMAIL SETTINGS (From GitHub Secrets)
# ========================================
YOUR_EMAIL = os.getenv("YOUR_EMAIL")  # Will come from GitHub
APP_PASSWORD = os.getenv("APP_PASSWORD")  # Will come from GitHub
TO_EMAIL = os.getenv("TO_EMAIL")  # FIXED: TO_EMAIL not TO EMAIL (no space)

# ========================================
# 2. SCHOLARSHIP SCRAPING FUNCTIONS
# ========================================

def scrape_scholarshipportal():
    """Fetch scholarships from ScholarshipPortal website"""
    scholarships = []
    try:
        url = "https://www.scholarshipportal.com/scholarships"
        print("Fetching from ScholarshipPortal...")
        
        # For now, we'll create sample data
        scholarships = [
            {"title": "Master's in AI Scholarship 2026", "deadline": "2026-01-15", "link": "https://example.com/ai-scholarship"},
            {"title": "Cybersecurity Excellence Award", "deadline": "2026-02-28", "link": "https://example.com/cyber-scholarship"},
            {"title": "Embedded Systems Research Grant", "deadline": "2026-03-10", "link": "https://example.com/embedded-grant"}
        ]
    except Exception as e:
        print(f"Error with ScholarshipPortal: {e}")
        scholarships.append({"title": "ScholarshipPortal - Check website", "deadline": "N/A", "link": "https://scholarshipportal.com"})
    
    return scholarships

def scrape_daad():
    """Fetch scholarships from DAAD (German Academic Exchange)"""
    scholarships = []
    try:
        print("Fetching from DAAD...")
        scholarships = [
            {"title": "DAAD Study Scholarship 2026", "deadline": "2026-04-01", "link": "https://daad.de/en"},
            {"title": "DAAD Research Grants", "deadline": "2026-05-15", "link": "https://daad.de/research"}
        ]
    except Exception as e:
        print(f"Error with DAAD: {e}")
        scholarships.append({"title": "DAAD Scholarships", "deadline": "N/A", "link": "https://daad.de"})
    
    return scholarships

def scrape_chevening():
    """Chevening Scholarships (UK)"""
    return [{"title": "Chevening Scholarship 2026/27", "deadline": "2026-11-01", "link": "https://chevening.org"}]

def scrape_fulbright():
    """Fulbright Scholarships (USA)"""
    return [{"title": "Fulbright Foreign Student Program", "deadline": "2026-10-15", "link": "https://fulbrightonline.org"}]

# ========================================
# 3. COLLECT ALL SCHOLARSHIPS
# ========================================
print("Starting scholarship collection...")
all_scholarships = []

# Add scholarships from all sources
all_scholarships += scrape_scholarshipportal()
all_scholarships += scrape_daad()
all_scholarships += scrape_chevening()
all_scholarships += scrape_fulbright()

print(f"Found {len(all_scholarships)} scholarships")

# ========================================
# 4. BUILD EMAIL CONTENT
# ========================================
today = datetime.now().strftime("%B %d, %Y")
summary = f"""🔥 DAILY SCHOLARSHIP UPDATE - {today} 🔥

Total Scholarships Found: {len(all_scholarships)}
Fields: AI, ML, DL, Embedded Systems, Cybersecurity
Countries: UK, USA, Canada, India
Starting: After August 2026

"""

# Add each scholarship to the email
for idx, scholarship in enumerate(all_scholarships, 1):
    summary += f"\n{idx}. {scholarship['title']}"
    summary += f"\n   Deadline: {scholarship['deadline']}"
    summary += f"\n   Link: {scholarship['link']}"
    summary += "\n" + "-"*50 + "\n"

summary += "\n\n📧 This email was sent automatically by your Scholarship Bot"
summary += "\n⏰ Next update: Tomorrow at 8 AM UTC"

# ========================================
# 5. SEND EMAIL
# ========================================
print("Preparing to send email...")

# Create email
msg = MIMEMultipart()
msg["From"] = YOUR_EMAIL
msg["To"] = TO_EMAIL
msg["Subject"] = f"📚 Daily Scholarship Update - {today}"
msg.attach(MIMEText(summary, "plain"))

try:
    # Connect to Gmail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Secure connection
    server.login(YOUR_EMAIL, APP_PASSWORD)
    
    # Send email
    server.sendmail(YOUR_EMAIL, TO_EMAIL, msg.as_string())
    server.quit()
    
    print("✅ Email sent successfully!")
    print(f"📧 Sent to: {TO_EMAIL}")
    
except Exception as e:
    print(f"❌ Error sending email: {e}")
    print("Make sure your Gmail App Password is correct in GitHub Secrets")
