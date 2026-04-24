import streamlit as st
import time
from smart_link_opener import identify_official_website

# Page config
st.set_page_config(
    page_title="Neuro-Symbolic OWIP",
    page_icon="🧠",
    layout="centered"
)

# 🔥 Title Section
st.markdown("""
<h1 style='text-align:center;'>🧠 Neuro-Symbolic OWIP System</h1>
<p style='text-align:center; color:gray;'>
(Neuro = AI reasoning, Symbolic = rule-based logic)
</p>
<hr>
""", unsafe_allow_html=True)

# 🔍 Input
query = st.text_input("🔍 Enter entity name:")

# 🚀 Button
if st.button("🚀 Find Official Website"):

    if not query.strip():
        st.warning("⚠️ Please enter something!")
    else:
        placeholder = st.empty()

        # 🔥 Animation
        for i in range(3):
            placeholder.markdown(f"### 🔍 Searching{'.'*i}")
            time.sleep(0.5)

        placeholder.markdown("### 🧠 Applying reasoning...")
        time.sleep(1)

        # 🔍 Call function
        try:
            result = identify_official_website(query)
            placeholder.empty()

            link = result.get("link", "Not found")
            category = result.get("category", "Unknown")

            # ✅ Result Display
            st.success("✅ Result Found")

            st.markdown(f"""
            ### 👉 [Open Website]({link})
            """)

            st.info(f"📌 Category: {category}")

        except Exception as e:
            placeholder.empty()
            st.error(f"❌ Error: {str(e)}")

# 🔻 Footer (YOUR REQUEST)
st.markdown("""
<hr>
<p style='text-align:center; color:gray; font-size:14px;'>
✨ Project by <b>U.Raha</b> and <b>Yazhini</b> ✨
</p>
""", unsafe_allow_html=True)