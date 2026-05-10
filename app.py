import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="سكرتيري الذكي", page_icon="💼")
st.title("💼 سكرتيري الذكي")

# محاولة الاتصال وعرض الخطأ الحقيقي
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("المفتاح السري غير موجود في إعدادات Secrets!")
    else:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("تم الاتصال بنجاح!") # رسالة تأكيد للاتصال
except Exception as e:
    st.error(f"خطأ تقني حقيقي: {e}")

# واجهة رفع الملفات والمحادثة البسيطة للتجربة
uploaded_file = st.sidebar.file_uploader("ارفع ملفك", type=['csv', 'xlsx'])
prompt = st.chat_input("اسألني أي شيء...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"فشل الرد بسبب: {e}")
