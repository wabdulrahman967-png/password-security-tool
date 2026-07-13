import streamlit as st
from core.password_checker import PasswordStrengthChecker
from core.breach_checker import BreachChecker

# إعداد الصفحة
st.set_page_config(
    page_title="Password Security Suite",
    page_icon="🔐",
    layout="centered"
)

# تهيئة الكلاسات
checker = PasswordStrengthChecker()
breach_checker = BreachChecker()

# العنوان
st.title("🔐 Password Security Suite")
st.markdown("### تحليل قوة كلمة المرور والتحقق من التسريبات")

# حقل إدخال كلمة المرور
password = st.text_input("أدخل كلمة المرور:", type="password")

# زر التحليل
if st.button("🔍 تحليل", type="primary"):
    if password:
        with st.spinner("جاري التحليل..."):
            # تحليل القوة
            strength = checker.check_strength(password)
            
            # التحقق من التسريب
            breach = breach_checker.check_password(password)
            
            # عرض النتائج
            st.markdown("---")
            st.markdown("## 📊 النتائج")
            
            # عرض القوة
            if "Weak" in strength['strength']:
                st.error(f"**القوة:** {strength['strength']}")
            elif "Medium" in strength['strength']:
                st.warning(f"**القوة:** {strength['strength']}")
            elif "Strong" in strength['strength']:
                st.success(f"**القوة:** {strength['strength']}")
            else:
                st.info(f"**القوة:** {strength['strength']}")
            
            # النقاط والإنتروبيا
            col1, col2 = st.columns(2)
            with col1:
                st.metric("الدرجة", f"{strength['score']}/{strength['max_score']}")
            with col2:
                st.metric("الإنتروبيا", f"{strength['entropy']} bits")
            
            # المعايير
            st.markdown("### 📋 المعايير")
            cols = st.columns(2)
            for i, (key, value) in enumerate(strength['criteria'].items()):
                label = key.replace('_', ' ').title()
                icon = "✅" if value else "❌"
                with cols[i % 2]:
                    st.write(f"{icon} {label}")
            
            # التوصيات
            if strength['feedback']:
                st.markdown("### 💡 التوصيات")
                for f in strength['feedback']:
                    st.write(f)
            
            # التحقق من التسريب
            st.markdown("### 🔍 فحص التسريبات")
            if breach:
                if breach[0] is None:
                    st.warning(f"⚠️ {breach[1]}")
                elif breach[0]:
                    st.error(f"🚨 **تم تسريب كلمة المرور!** عدد المرات: {breach[1]}")
                else:
                    st.success("✅ **لم يتم تسريب كلمة المرور**")
            
            # نصيحة
            st.markdown("---")
            st.caption("🔒 كلمة المرور مش بتتخزن ولا بتتبعت لأي حد")
    else:
        st.warning("من فضلك أدخل كلمة المرور أولاً")
