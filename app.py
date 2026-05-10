import streamlit as st
import pandas as pd
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="سكرتيري الذكي", page_icon="💼")
st.title("💼 سكرتيري الذكي")

# الربط باستخدام الموديل اللي شفناه في القائمة عندك
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # استخدمنا الاسم اللي طلع في شاشتك بالضبط
        model = genai.GenerativeModel('gemini-2.5-flash')
        st.success("✅ تم الاتصال بنجاح! سكرتيرك المطور جاهز.")
    except Exception as e:
        st.error(f"مشكلة في الربط: {e}")
else:
    st.error("المفتاح غير موجود في Secrets")

# رفع الملفات
uploaded_file = st.sidebar.file_uploader("ارفع ملفك (Excel أو CSV)", type=['csv', 'xlsx'])
prompt = st.chat_input("اسأل سكرتيرك أي شيء...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            full_prompt = prompt
            if uploaded_file:
                # قراءة الملف المرفوع
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                # نأخذ عينة من البيانات عشان يفهمها
                context = df.head(20).to_string()
                full_prompt = f"أنت سكرتير ذكي ومحلل بيانات خبير. إليك بيانات من الملف المرفوع:\n{context}\n\nبناءً على هذه البيانات، أجب على التالي: {prompt}"
            
            # إرسال الطلب للموديل الجديد
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"حدث خطأ أثناء معالجة الرد: {e}")
