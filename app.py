import streamlit as st
import google.generativeai as genai

st.title("🔎 كشاف الموديلات المتاحة")

if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        st.write("جاري البحث عن الموديلات التي يدعمها حسابك...")
        
        # كود لجلب القائمة كاملة من جوجل
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if available_models:
            st.success(f"وجدنا {len(available_models)} موديلات متاحة!")
            st.write("انسخ أحد الأسماء التالية وضعه في الرد القادم:")
            for model_name in available_models:
                st.code(model_name)
        else:
            st.warning("لم نجد موديلات تدعم توليد المحتوى. قد تكون هناك مشكلة في صلاحيات المفتاح.")
            
    except Exception as e:
        st.error(f"خطأ أثناء جلب القائمة: {e}")
else:
    st.error("المفتاح غير موجود في Secrets")
