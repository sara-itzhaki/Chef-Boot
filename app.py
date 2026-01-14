import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="שף Gemini - עוזר הבישול שלך", page_icon="👨‍🍳")

# עיצוב RTL (מימין לשמאל)
st.markdown("""
    <style>
    .stApp { direction: RTL; text-align: right; }
    [data-testid="stChatMessage"] { direction: RTL; text-align: right; flex-direction: row-reverse; }
    [data-testid="stChatInput"] { direction: RTL; }
    textarea { text-align: right !important; direction: RTL !important; }
    section[data-testid="stSidebar"] { direction: RTL; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# סרגל צד (Sidebar)
with st.sidebar:
    st.header("⚙️ הגדרות המטבח")
    cuisine = st.selectbox("סוג מטבח", ["הכל", "איטלקי", "צרפתי", "ים-תיכוני", "קינוחים"])
    difficulty = st.select_slider("רמת קושי", options=["קל מאוד", "בינוני", "למתקדמים"])
    
    if st.button("נקה היסטוריית צ'אט"):
        st.session_state.messages = []
        st.rerun()

st.title("👨‍🍳 שף Gemini האישי")

# אתחול הלקוח והצ'אט
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)
    # הוראות מערכת קבועות
    sys_instruct = "אתה שף מומחה. ענה רק על שאלות הקשורות למטבח ובישול. ענה תמיד בעברית."
    st.session_state.chat = st.session_state.client.chats.create(
         model="models/gemini-flash-latest",  
        config={"system_instruction": sys_instruct}
    )
    st.session_state.messages = []

# הצגת היסטוריית ההודעות
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# קלט מהמשתמש
if prompt := st.chat_input("מה נבשל היום?"):
    # הצגת הודעת המשתמש
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # יצירת תשובת השף
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("השף רושם את המתכון... 🍳")
        
        # בניית הפרומפט המלא עם ההעדפות (כאן הגדרנו את המשתנה!)
        full_context = f"בקשת המשתמש: {prompt}. העדפות: מטבח {cuisine}, רמת קושי {difficulty}."
        
        try:
            response = st.session_state.chat.send_message(full_context)
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # כפתור הורדה למתכון
            st.download_button(
                label="📥 הורד מתכון כקובץ טקסט",
                data=full_response,
                file_name="recipe.txt",
                mime="text/plain"
            )
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"אופס, קרתה שגיאה: {e}")