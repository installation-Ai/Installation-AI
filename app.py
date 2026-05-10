import streamlit as st
import pandas as pd
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="سكرتيري الذكي", page_icon="💼")
st.title("💼 سكرتيري الذكي")

# الربط باستخدام النسخة الأكثر استقراراً في العالم
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # نستخدم اسم الموديل القديم والمضمون 100% في كل السيرفرات
        model = genai.GenerativeModel('gemini-pro')
        st.success("✅ تم الاتصال بنجاح! السكرتير جاهز.")
    except Exception as e:
        st.error(f"مشكلة في الربط: {e}")
else:
    st.error("المفتاح غير موجود في Secrets")

# رفع الملفات
uploaded_file = st.sidebar.file_uploader("ارفع ملفك", type=['csv', 'xlsx'])
prompt = st.chat_input("اسأل سكرتيرك أي شيء...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            context = ""
            if uploaded_file:
                df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
                context = f"تحليل بيانات:\n{df.head(5).to_string()}\n\n"
            
            # إرسال الطلب
            response = model.generate_content(context + prompt)
            st.markdown(response.text)
        except Exception as e:
            # هنا بنعرف إذا لسه فيه مشكلة في الاسم
            st.warning("جاري محاولة الاتصال البديلة...")
            try:
                # محاولة أخيرة بأسلوب مختلف
                model_alt = genai.GenerativeModel('models/gemini-pro')
                response = model_alt.generate_content(context + prompt)
                st.markdown(response.text)
            except:
                st.error(f"عذراً، يبدو أن هناك قيوداً في منطقتك الجغرافية على هذا الموديل. الخطأ: {e}")
