import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import pandas as pd

# .env faylından istifadəçi məlumatlarını yükləyin
load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# KOICA platformasına daxil olun
login_url = "https://sso.aztu.edu.az"
attendance_url = "https://sap.aztu.edu.az/studies/lecture_attend.php?lec_open_idx=60456&lecture_code=4138&sem_code=20242"

session = requests.Session()
login_payload = {
   "username":load_dotenv.username,
    "password": load_dotenv.password,
}

session.post(login_url, data=login_payload)

# Davamiyyət məlumatlarını əldə edin
response = session.get(attendance_url)
soup = BeautifulSoup(response.content, "html.parser")

# Müvafiq tarixə uyğun davamiyyət məlumatlarını toplayın
attendance_data = []
rows = soup.find_all("tr")

for row in rows:
    cols = row.find_all("td")
    cols = [ele.text.strip() for ele in cols]
    attendance_data.append(cols)

# Cədvəl faylında saxlayın
attendance_df = pd.DataFrame(attendance_data, columns=["Tarix", "Davamiyyət"])
attendance_df.to_excel("attendance.xlsx", index=False)

print("Davamiyyət məlumatlari uğurla cədvəl faylinda saxlanildi.")
