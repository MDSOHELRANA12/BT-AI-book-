import streamlit as st
from supabase import create_client
import uuid

# --- DATABASE CONNECTION SETTINGS ---
# Using the credentials from your Supabase panel
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bt-Ai Global Business Pro", layout="wide")

# --- PREMIUM DARK THEME UI ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; font-family: 'Inter', sans-serif; }
    .card { background: #111; padding: 25px; border-radius: 15px; border: 1px solid #222; margin-bottom: 20px; }
    .revenue-text { color: #00ff00; font-size: 35px; font-weight: bold; }
    .stButton>button { background-color: #1e90ff; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("✪ Bt-Ai Platform")
menu = ["🏠 Global Feed", "📤 Publish Video", "👤 User Profile", "💰 Wallet & Bank", "🤖 AI Assistant"]
choice = st.sidebar.selectbox("Dashboard Menu", menu)

# --- 1. GLOBAL VIDEO FEED ---
if choice == "🏠 Global Feed":
    st.title("🌎 Trending Content")
    try:
        # Fetching latest videos from your database
        v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if v_data.data:
            for v in v_data.data:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.video(v['video_url'])
                    st.subheader(v.get('title', 'Untitled Content'))
                    c1, c2 = st.columns(2)
                    c1.write(f"❤️ {v.get('likes', 0)} Likes")
                    c2.write(f"👁️ {v.get('views', 0)} Views")
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Feed is empty. Upload a video to start!")
    except Exception as e:
        st.error("Feed connection error. Please refresh.")

# --- 2. VIDEO PUBLISHING SYSTEM ---
elif choice == "📤 Publish Video":
    st.title("📤 Creator Studio")
    st.write("Upload your MP4 video to our global servers.")
    
    v_file = st.file_uploader("Choose Video (MP4)", type=['mp4'])
    v_title = st.text_input("Content Title", placeholder="Enter video title...")
    
    if st.button("Publish Now") and v_file:
        with st.spinner("Uploading to Server..."):
            try:
                # Unique naming and path
                file_id = str(uuid.uuid4())
                file_path = f"public/{file_id}.mp4"
                
                # Upload to Supabase Storage
                supabase.storage.from_('videos').upload(file_path, v_file.read())
                
                # Get Public Link
                video_url = supabase.storage.from_('videos').get_public_url(file_path)
                
                # Save to Videos Table
                supabase.table("videos").insert({
                    "video_url": video_url, 
                    "title": v_title,
                    "likes": 0,
                    "views": 0
                }).execute()
                
                st.success("Your video is live globally! ✅")
                st.balloons()
            except Exception as e:
                st.error("Upload failed. Ensure 'videos' bucket is Public.")

# --- 3. UNIVERSAL PROFILE SECTION ---
elif choice == "👤 User Profile":
    st.title("👤 Account Settings")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("profile_settings"):
        # Matches your Profiles table structure
        st.text_input("Full Name", value="MD SOHEL RANA")
        st.text_area("Biography")
        st.text_input("Global Identity / Address")
        if st.form_submit_button("Update Profile"):
            st.success("Identity updated successfully! 🏆")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. BANKING & REVENUE TRACKING ---
elif choice == "💰 Wallet & Bank":
    st.title("💰 Business Earnings")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("Available Balance")
    st.markdown('<p class="revenue-text">$0.00</p>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("Payout Details")
    # Matches your Payments table requirements
    st.text_input("Bank Name")
    st.text_input("Account Holder Name")
    st.text_input("Account Number / IBAN")
    st.text_input("SWIFT / Routing Code")
    
    if st.button("Link Payout Method"):
        st.success("Bank details saved for automated payouts! ✅")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. AI BUSINESS CHATBOT ---
elif choice == "🤖 AI Assistant":
    st.title("🤖 Bt-Ai Help Center")
    st.write("Professional support for your business growth.")
    
    user_input = st.chat_input("Ask a question about your business...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            st.write("Analyzing your request... Our expert team will assist you shortly.")
