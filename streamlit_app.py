import streamlit as st
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from core.password_checker import PasswordStrengthChecker
from core.breach_checker import BreachChecker

# Page configuration
st.set_page_config(
    page_title="Password Security Suite",
    page_icon="🔐",
    layout="centered"
)

# Initialize classes
checker = PasswordStrengthChecker()
breach_checker = BreachChecker()

# Title
st.title("🔐 Password Security Suite")
st.markdown("### Analyze password strength & check for breaches")

# Password input
password = st.text_input("Enter your password:", type="password")

# Analyze button
if st.button("🔍 Analyze", type="primary"):
    if password:
        with st.spinner("Analyzing..."):
            # Strength analysis
            strength = checker.check_strength(password)
            
            # Breach check
            breach = breach_checker.check_password(password)
            
            # Display results
            st.markdown("---")
            st.markdown("## 📊 Results")
            
            # Strength display
            if "Weak" in strength['strength']:
                st.error(f"**Strength:** {strength['strength']}")
            elif "Medium" in strength['strength']:
                st.warning(f"**Strength:** {strength['strength']}")
            elif "Strong" in strength['strength']:
                st.success(f"**Strength:** {strength['strength']}")
            else:
                st.info(f"**Strength:** {strength['strength']}")
            
            # Score and Entropy
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Score", f"{strength['score']}/{strength['max_score']}")
            with col2:
                st.metric("Entropy", f"{strength['entropy']} bits")
            
            # Criteria
            st.markdown("### 📋 Criteria")
            cols = st.columns(2)
            items = list(strength['criteria'].items())
            for i, (key, value) in enumerate(items):
                label = key.replace('_', ' ').title()
                icon = "✅" if value else "❌"
                with cols[i % 2]:
                    st.write(f"{icon} {label}")
            
            # Recommendations
            if strength['feedback']:
                st.markdown("### 💡 Recommendations")
                for f in strength['feedback']:
                    st.write(f)
            
            # Breach check
            st.markdown("### 🔍 Breach Check")
            if breach:
                if breach[0] is None:
                    st.warning(f"⚠️ {breach[1]}")
                elif breach[0]:
                    st.error(f"🚨 **Password BREACHED!** Found {breach[1]} times")
                else:
                    st.success("✅ **No breaches found**")
            
            # Footer
            st.markdown("---")
            st.caption("🔒 Your password is never stored or sent anywhere")
    else:
        st.warning("Please enter a password first")
