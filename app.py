import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="سكرتيري الذكي", page_icon="💼")
st.title("💼 سكرتيري الذكي")

# جلب المفتاح والتأكد منه
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # محاولة تعريف الموديل بأكثر اسم مستقر
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("تم الاتصال بنجاح!")
    else:
        st.error("المفتاح السري (Secrets) غير موجود!")
except Exception as e:
    st.error(f"خطأ في الإعدادات: {e}")

# واجهة رفع الملفات
uploaded_file = st.sidebar.file_uploader("ارفع ملفك", type=['csv', 'xlsx'])
prompt = st.chat_input("اسألني عن بياناتك...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            full_prompt = prompt
            if uploaded_file is not None:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                data_info = df.head(10).to_string()
                full_prompt = f"هذه بيانات من ملف إكسل:\n{data_info}\n\nسؤالي هو: {prompt}"
            
            # تنفيذ الطلب
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"حدث خطأ أثناء الرد. التفاصيل: {e}")
