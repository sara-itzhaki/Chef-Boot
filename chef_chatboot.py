import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("שגיאה: מפתח לא נמצא")
else:
    client = genai.Client(api_key=api_key)
    
    # שינוי קטן כאן - הגדרת המודל בצורה מפורשת
    model_id = "models/gemini-2.5-flash"
    
    sys_instruct = "אתה שף מומחה. ענה רק על שאלות הקשורות למטבח ובישול."

    print("--- בוט השף מוכן! ---")

    # יצירת הצ'אט
    chat = client.chats.create(model=model_id, config={"system_instruction": sys_instruct})

    while True:
        user_input = input("את: ")
        if user_input.lower() in ['צא', 'exit']:
            break
        
        try:
            # הוספת "Response" בצורה מפורשת
            response = chat.send_message(user_input)
            print(f"שף: {response.text}")
        except Exception as e:
            print(f"קרתה שגיאה: {e}")
        print("-" * 20)