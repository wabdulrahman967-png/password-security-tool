import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.password_checker import PasswordStrengthChecker
from core.breach_checker import BreachChecker
from core.encryption import CaesarCipher
from core.generator import PasswordGenerator
from core.report_generator import ReportGenerator

st.set_page_config(
    page_title="Password Security Suite",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1a1c2c 0%, #0d0e17 60%);
    }
    .hero {
        text-align: center;
        padding: 1.2rem 0 0.4rem 0;
    }
    .hero h1 {
        font-size: 2.4rem;
        background: linear-gradient(90deg, #89b4fa, #a6e3a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero p {
        color: #9399b2;
        font-size: 1rem;
    }
    div[data-testid="stMetric"] {
        background: #181926;
        border: 1px solid #292c3c;
        border-radius: 12px;
        padding: 0.6rem;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
    footer, #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

checker = PasswordStrengthChecker()
breach_checker = BreachChecker()
report_gen = ReportGenerator()

st.markdown(
    """
    <div class="hero">
        <h1>🔐 Password Security Suite</h1>
        <p>Strength analysis · breach lookup · secure generator · classic cipher lab</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_check, tab_generate, tab_cipher, tab_about = st.tabs(
    ["🔍 Strength & Breach Check", "🎲 Password Generator", "🔁 Caesar Cipher", "ℹ️ About"]
)

# ---------------------------------------------------------------------------
# TAB 1: Strength + breach check
# ---------------------------------------------------------------------------
with tab_check:
    password = st.text_input("Enter a password to analyze:", type="password", key="pw_input")
    check_breach = st.checkbox("Also check Have I Been Pwned (needs internet)", value=True)
    go = st.button("🔍 Analyze", type="primary", use_container_width=True)

    if go:
        if not password:
            st.warning("Please enter a password first")
        else:
            strength = checker.check_strength(password)

            st.markdown("---")
            level = strength["strength"]
            if "Weak" in level:
                st.error(f"**Strength:** {level}")
            elif "Medium" in level:
                st.warning(f"**Strength:** {level}")
            elif "Very Strong" in level:
                st.success(f"**Strength:** {level}")
            else:
                st.info(f"**Strength:** {level}")

            st.progress(min(strength["score"] / strength["max_score"], 1.0))

            c1, c2, c3 = st.columns(3)
            c1.metric("Score", f"{strength['score']}/{strength['max_score']}")
            c2.metric("Entropy", f"{strength['entropy']} bits")
            c3.metric("Est. crack time", strength["crack_time"])

            st.markdown("#### 📋 Criteria")
            cols = st.columns(2)
            for i, (key, value) in enumerate(strength["criteria"].items()):
                label = key.replace("_", " ").title()
                icon = "✅" if value else "❌"
                cols[i % 2].write(f"{icon} {label}")

            if strength["feedback"]:
                st.markdown("#### 💡 Recommendations")
                for f in strength["feedback"]:
                    st.write(f)

            breach_info = {"is_breached": False, "count": 0}
            if check_breach:
                st.markdown("#### 🌐 Breach Check")
                with st.spinner("Checking Have I Been Pwned..."):
                    breach = breach_checker.check_password(password)
                if breach[0] is None:
                    st.warning(f"⚠️ {breach[1]}")
                elif breach[0]:
                    st.error(f"🚨 **Password BREACHED!** Found {breach[1]:,} times in known leaks")
                    breach_info = {"is_breached": True, "count": breach[1]}
                else:
                    st.success("✅ No breaches found")

            report_data = {**strength, "breach_info": breach_info}
            report_text = report_gen.generate_report(report_data)
            st.download_button(
                "📄 Download report (.txt)",
                data=report_text,
                file_name="password_security_report.txt",
                use_container_width=True,
            )

            st.caption("🔒 Your password is never stored or sent anywhere except the anonymized breach check.")

# ---------------------------------------------------------------------------
# TAB 2: Password generator
# ---------------------------------------------------------------------------
with tab_generate:
    st.markdown("#### 🎲 Generate a strong password")
    length = st.slider("Length", min_value=8, max_value=64, value=16)
    col_a, col_b = st.columns(2)
    with col_a:
        use_upper = st.checkbox("Uppercase (A-Z)", value=True)
        use_digits = st.checkbox("Digits (0-9)", value=True)
    with col_b:
        use_lower = st.checkbox("Lowercase (a-z)", value=True)
        use_special = st.checkbox("Special (!@#$...)", value=True)
    avoid_ambiguous = st.checkbox("Avoid ambiguous characters (l, 1, O, 0...)", value=False)

    if st.button("Generate password", type="primary", use_container_width=True):
        try:
            generated = PasswordGenerator.generate(
                length=length,
                use_upper=use_upper,
                use_lower=use_lower,
                use_digits=use_digits,
                use_special=use_special,
                avoid_ambiguous=avoid_ambiguous,
            )
            st.code(generated, language=None)
            gen_strength = checker.check_strength(generated)
            st.caption(
                f"Strength: {gen_strength['strength']} · Entropy: {gen_strength['entropy']} bits"
            )
        except ValueError as e:
            st.error(str(e))

# ---------------------------------------------------------------------------
# TAB 3: Caesar cipher lab
# ---------------------------------------------------------------------------
with tab_cipher:
    st.markdown("#### 🔁 Caesar Cipher (educational)")
    mode = st.radio("Mode", ["Encrypt", "Decrypt", "Brute-force all shifts"], horizontal=True)
    text = st.text_area("Text", height=100)

    if mode in ("Encrypt", "Decrypt"):
        shift = st.slider("Shift", 1, 25, 3)
        if st.button("Run", type="primary", use_container_width=True):
            if text:
                result = (
                    CaesarCipher.encrypt(text, shift)
                    if mode == "Encrypt"
                    else CaesarCipher.decrypt(text, shift)
                )
                st.code(result, language=None)
            else:
                st.warning("Enter some text first")
    else:
        if st.button("Try all 25 shifts", type="primary", use_container_width=True):
            if text:
                for r in CaesarCipher.brute_force(text):
                    st.write(f"**Shift {r['shift']:>2}:** {r['text']}")
            else:
                st.warning("Enter some text first")

# ---------------------------------------------------------------------------
# TAB 4: About
# ---------------------------------------------------------------------------
with tab_about:
    st.markdown(
        """
        ### About this tool

        **Password Security Suite** is an open-source toolkit for evaluating and
        generating strong passwords.

        - **Strength analysis** — 7-point criteria check + true Shannon entropy
        - **Breach check** — k-anonymity lookup against Have I Been Pwned,
          your password is never transmitted in full
        - **Generator** — cryptographically secure passwords via Python's `secrets` module
        - **Caesar cipher lab** — classic cipher for learning encryption basics

        Built with Python & Streamlit.
        """
    )
