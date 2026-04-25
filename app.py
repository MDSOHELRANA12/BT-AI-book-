import streamlit as st
from supabase import create_client

# সুপাবেস কানেকশন
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"

try:
    supabase = create_client(URL, KEY)
    conn_status = "✅ Bt-Ai-Book Cloud Connected"
except:
    conn_status = "❌ Connection Failed"

st.set_page_config(page_title="Bt-Ai-Book", layout="wide")
st.title("🌐 Bt-Ai-Book International")
st.sidebar.success(conn_status)

menu = ["🏠 Home Feed", "📤 Upload Video", "💰 Monetization"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "🏠 Home Feed":
    st.header("Global Trending Videos")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

elif choice == "📤 Upload Video":
    st.header("Post New Content")
    st.file_uploader("Select Video", type=["mp4", "mov"])
    if st.button("Publish Now"):
        st.balloons()
        st.success("Successfully Uploaded!")

elif choice == "💰 Monetization":
    st.header("Creator Dashboard")
    st.info("Target: 1000 Followers & 6 Months Activity")
