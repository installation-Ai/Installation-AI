import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="سكرتيري الذكي", page_icon="💼")
st.title("💼 سكرتيري الذكي")

# محاولة الربط
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # استخدمنا هنا النسخة المستقرة والمجربة عالمياً
        model = genai.GenerativeModel('gemini-pro')
        st.success("✅ المتصل الآن: سكرتيرك الذكي جاهز!")
    except Exception as e:
        st.error(f"❌ مشكلة في الربط: {e}")
else:
    st.error("🔑 المفتاح السري غير مضاف في إعدادات Secrets")

# رفع الملفات
uploaded_file = st.sidebar.file_uploader("ارفع ملف الإكسل هنا", type=['csv', 'xlsx'])
prompt = st.chat_input("اكتب سؤالك للسكرتير...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            context = ""
            if uploaded_file:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                context = f"تحليل لبيانات الملف:\n{df.head(10).to_string()}\n\n"
            
            # إرسال السؤال مع سياق البيانات
            response = model.generate_content(context + prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"⚠️ حدث خطأ في معالجة الرد: {e}")
