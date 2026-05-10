import streamlit as st
import pandas as pd
import google.generativeai as genai

# إعدادات واجهة الموقع
st.set_page_config(page_title="سكرتيري الذكي", page_icon="💼", layout="wide")
st.title("💼 سكرتيري الذكي - مساعدك الشخصي")

# جلب المفتاح السري بأمان
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("جاري إعداد المفتاح السري...")

# القائمة الجانبية لرفع الملفات
st.sidebar.header("📂 ارفع ملفات شغلك هنا")
uploaded_file = st.sidebar.file_uploader("اختر ملف Excel أو CSV", type=['csv', 'xlsx'])

data_context = ""
if uploaded_file is not None:
    try:
        # قراءة الملف
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.sidebar.success("تم رفع الملف بنجاح! ✅")
        st.sidebar.write("نظرة سريعة على البيانات:")
        st.sidebar.dataframe(df.head())
        
        # تحويل البيانات لنص يفهمه الذكاء الاصطناعي
        data_context = f"إليك بيانات ملف العمل المرفق:\n{df.to_string()}"
    except Exception as e:
        st.sidebar.error(f"حدث خطأ أثناء قراءة الملف: {e}")

# واجهة المحادثة (الشات)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب تعليماتك للسكرتير أو اطلب تقرير بناءً على الملف..."):
    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # دمج البيانات مع طلب المستخدم وإرسالها للذكاء الاصطناعي
    full_prompt = f"أنت سكرتير ذكي ومحترف. أجب على طلب المستخدم بدقة وبناءً على البيانات التالية إن وجدت.\n\n{data_context}\n\nطلب المستخدم: {prompt}"

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("تأكد من إعداد المفتاح السري بشكل صحيح في إعدادات Streamlit.")
