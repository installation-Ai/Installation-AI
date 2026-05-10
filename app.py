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
        # استخدمنا هنا الاسم الكامل والأحدث للموديل
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        st.success("تم الاتصال بنجاح! السكرتير جاهز لخدمتك.") 
except Exception as e:
    st.error(f"خطأ تقني في الاتصال: {e}")

# واجهة رفع الملفات
uploaded_file = st.sidebar.file_uploader("ارفع ملفك (Excel أو CSV)", type=['csv', 'xlsx'])
prompt = st.chat_input("اكتب تعليماتك للسكرتير هنا...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            full_prompt = prompt
            if uploaded_file is not None:
                # محاولة قراءة الملف المرفوع
                if uploaded_file.name.endswith('xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)
                # إرسال عينة من البيانات للذكاء الاصطناعي لفهم الملف
                data_summary = df.head(10).to_string()
                full_prompt = f"أنت سكرتير ذكي. إليك بيانات من ملف إكسل:\n{data_summary}\n\nبناءً على هذه البيانات، أجب على التالي: {prompt}"
            
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"حدثت مشكلة أثناء محاولة الرد: {e}")
