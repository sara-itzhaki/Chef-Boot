import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

print("בודק מודלים זמינים...")
try:
    for m in client.models.list():
        print(f"מודל זמין: {m.name}")
except Exception as e:
    print(f"שגיאה בבדיקה: {e}")