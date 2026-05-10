import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="سكرتيري الذكي", page_icon="💼")
st.title("💼 سكرتيري الذكي")

# محاولة الاتصال
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("المفتاح السري غير موجود في إعدادات Secrets!")
    else:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # غيرنا الاسم هنا للإصدار المستقر والمضمون
        model = genai.GenerativeModel('gemini-pro')
        st.success("تم الاتصال بنجاح! السكرتير جاهز لخدمتك.") 
except Exception as e:
    st.error(f"خطأ تقني: {e}")

# واجهة رفع الملفات
uploaded_file = st.sidebar.file_uploader("ارفع ملفك (Excel أو CSV)", type=['csv', 'xlsx'])
prompt = st.chat_input("اكتب تعليماتك للسكرتير هنا...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            # إضافة سياق الملف إذا تم رفعه
            full_prompt = prompt
            if uploaded_file is not None:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                full_prompt = f"بناءً على البيانات التالية:\n{df.head(10).to_string()}\n\nالسؤال: {prompt}"
            
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"حدثت مشكلة في الرد: {e}")
