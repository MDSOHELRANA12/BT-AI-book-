import streamlit as st
from supabase import create_client
import uuid

# --- DATABASE CONNECTION ---
# Using the credentials from your Supabase setup
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="Bt-Ai Global Pro", layout="centered")

# --- CUSTOM CSS FOR MODERN LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { border: 1px solid #333; padding: 15px; border-radius: 15px; margin-bottom: 20px; background: #111; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR MENU ---
st.sidebar.title("✪ Bt-Ai Book")
menu = ["🔥 Global Feed", "📤 Publish Video"]
choice = st.sidebar.selectbox("Platform Menu", menu)

# --- 1. GLOBAL FEED ---
if choice == "🔥 Global Feed":
    st.title("🌎 Trending Globally")
    try:
        # Fetching videos from the database table you created
        v_data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        
        if v_data.data:
            for v in v_data.data:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                st.subheader(v.get('title', 'Untitled Video'))
                
                col1, col2 = st.columns(2)
                col1.write(f"❤️ {v.get('likes', 0)} Likes")
                col2.write(f"👁️ {v.get('views', 0)} Views")
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("---")
        else:
            st.info("No videos found. Be the first to upload!")
    except Exception as e:
        st.error(f"System Busy: Please ensure your Database Tables are ready.")

# --- 2. UPLOAD SECTION ---
elif choice == "📤 Publish Video":
    st.title("📤 Creator Studio")
    st.write("Upload your MP4 video directly to our global servers.")
    
    video_file = st.file_uploader("Select Video File (MP4)", type=['mp4'])
    title = st.text_input("Video Title", placeholder="Enter a catchy title...")
    
    if st.button("Publish Now") and video_file:
        with st.spinner("Uploading to Global Server..."):
            try:
                # Unique filename generation
                file_id = str(uuid.uuid4())
                file_path = f"public/{file_id}.mp4"
                
                # 1. Upload to Supabase Storage Bucket
                # Ensure the 'videos' bucket is set to PUBLIC in Supabase settings
                supabase.storage.from_('videos').upload(file_path, video_file.read())
                
                # 2. Get Public URL
                video_url = supabase.storage.from_('videos').get_public_url(file_path)
                
                # 3. Insert metadata into Database
                supabase.table("videos").insert({
                    "video_url": video_url, 
                    "title": title,
                    "likes": 0,
                    "views": 0
                }).execute()
                
                st.success("Congratulations! Your video is now LIVE on the Feed. ✅")
                st.balloons()
            except Exception as e:
                st.error(f"Upload Failed: Check if your 'videos' bucket is Public.")
