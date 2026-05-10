import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="سكرتيري الذكي", page_icon="💼")
st.title("💼 سكرتيري الذكي")

# محاولة الاتصال - الطريقة المختصرة والمستقرة
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("المفتاح السري غير موجود في إعدادات Secrets!")
    else:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # استخدام الاسم المجرد للموديل وهو الأكثر استقراراً
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # تجربة اتصال سريعة للتأكد
        st.success("تم الاتصال بنجاح!") 
except Exception as e:
    st.error(f"خطأ في الإعدادات: {e}")

# واجهة رفع الملفات
uploaded_file = st.sidebar.file_uploader("ارفع ملفك (Excel أو CSV)", type=['csv', 'xlsx'])
prompt = st.chat_input("اسألني أي شيء عن ملفك...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            full_prompt = prompt
            if uploaded_file is not None:
                if uploaded_file.name.endswith('xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)
                
                # إرسال البيانات كتحليل نصي
                data_summary = df.head(15).to_string()
                full_prompt = f"أنت مساعد إداري خبير. هذه بيانات من ملف:\n{data_summary}\n\nأجب على هذا السؤال بناءً عليها: {prompt}"
            
            # محاولة توليد الرد
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
        except Exception as e:
            # عرض الخطأ بشكل مبسط
            st.error(f"عذراً، واجهت مشكلة في معالجة الرد. تأكد من صلاحية المفتاح.")
            st.info(f"تفاصيل الخطأ التقني: {e}")
