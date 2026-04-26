import streamlit as st
from supabase import create_client
import uuid

# 1. SERVER CONFIGURATION
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# 2. HD INTERFACE & PROFESSIONAL UI
st.set_page_config(page_title="Bt-Ai-Book Global", layout="centered", page_icon="🌎")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .stMarkdown, p, h1, h2, h3, span { color: white !important; font-family: 'Arial', sans-serif; }
    
    /* Professional Video Player Overlay */
    .video-container { position: relative; width: 100%; max-width: 400px; margin: auto; border-radius: 25px; border: 2px solid #fe2c55; overflow: hidden; }
    .stVideo { height: 720px !important; border-radius: 20px; object-fit: cover; }
    
    /* Creator Identity Overlay */
    .creator-overlay {
        position: absolute; top: 20px; left: 20px; display: flex; align-items: center; gap: 12px; z-index: 100;
    }
    .profile-img { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #fff; object-fit: cover; }
    .plus-follow { background: #fe2c55; color: white; border-radius: 50%; width: 20px; height: 20px; display: flex; justify-content: center; align-items: center; font-size: 14px; margin-left: -22px; margin-top: 30px; border: 1px solid #fff; }
    
    /* Watermark Branding */
    .branding { position: absolute; top: 20px; right: 20px; color: rgba(255,255,255,0.4); font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
st.sidebar.title("✪ Bt-Ai-Book")
user_search = st.sidebar.text_input("🔍 Search Users")
main_menu = ["🔥 Global Feed", "📤 Creator Studio", "👤 Profile Settings", "🏦 Wallet & Payout", "🤖 Bt-Ai Chat"]
choice = st.sidebar.selectbox("Dashboard", main_menu)

# --- SECTION 1: GLOBAL FEED (Real-Time Stats) ---
if choice == "🔥 Global Feed":
    st.title("🌎 Trending Feed")
    
    try:
        # Fetch Data from Supabase
        video_res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        profile_res = supabase.table("profiles").select("*").limit(1).execute()
        
        # Identity Logic
        creator_name = profile_res.data[0]['name'] if profile_res.data else "MD SOHEL RANA"
        creator_pic = profile_res.data[0].get('avatar_url', 'https://ui-avatars.com/api/?name=User')

        if not video_res.data:
            st.info("No content available yet. Be the first to post!")
        
        for v in video_res.data:
            # Auto-Update View Count
            v_count = v.get('views', 0)
            supabase.table("videos").update({"views": v_count + 1}).eq("id", v['id']).execute()
            
            with st.container():
                st.markdown(f'''
                <div class="video-container">
                    <div class="branding">✪ Bt-Ai-Book</div>
                    <div class="creator-overlay">
                        <img src="{creator_pic}" class="profile-img">
                        <div class="plus-follow">+</div>
                        <span style="font-weight:bold; text-shadow: 2px 2px 5px #000;">{creator_name}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                st.video(v['video_url'])
                
                col1, col2, col3 = st.columns(3)
                # Real Engagement System
                if col1.button(f"❤️ {v.get('likes', 0)} Likes", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0)+1}).eq("id", v['id']).execute()
                    st.rerun()
                
                col2.write(f"👁️ {v_count + 1} Views")
                
                if col3.button("🚀 Share", key=f"sh_{v['id']}"):
                    st.code(v['video_url'])
                    st.toast("Direct link copied!")
                st.write("---")
    except Exception as e:
        st.error(f"Database sync error: {e}")

# --- SECTION 2: PROFILE MANAGEMENT ---
elif choice == "👤 Profile Settings":
    st.title("👤 Universal Profile")
    user_data = supabase.table("profiles").select("*").execute()
    
    current_name = user_data.data[0]['name'] if user_data.data else "MD SOHEL RANA"
    new_name = st.text_input("Creator Username", value=current_name)
    avatar = st.file_uploader("Upload Identity Photo", type=['jpg', 'png'])
    
    if st.button("Save Profile Globally"):
        payload = {"name": new_name}
        if avatar:
            path = f"avatars/{uuid.uuid4()}.jpg"
            supabase.storage.from_('videos').upload(path, avatar.read())
            payload["avatar_url"] = supabase.storage.from_('videos').get_public_url(path)
        
        supabase.table("profiles").upsert(payload).execute()
        st.success("Global Identity Synced Successfully! ✅")

# --- SECTION 3: CREATOR STUDIO ---
elif choice == "📤 Creator Studio":
    st.title("📤 World Publisher")
    vid_file = st.file_uploader("Select MP4 Video File", type=['mp4'])
    if st.button("Publish Live") and vid_file:
        with st.spinner("Processing Global Broadcast..."):
            file_id = f"reels/{uuid.uuid4()}.mp4"
            supabase.storage.from_('videos').upload(file_id, vid_file.read())
            live_url = supabase.storage.from_('videos').get_public_url(file_id)
            supabase.table("videos").insert({"video_url": live_url, "likes": 0, "views": 0}).execute()
            st.success("Content is now live in all regions!")

# --- SECTION 4: WALLET & AI ---
elif choice == "🏦 Wallet & Payout":
    st.title("💰 Earnings Control")
    st.metric("Global Balance", "$120.45", "+$15.20 Today")
    st.info("🏦 Clear Bank, London | Status: Active & Secured ✅")

elif choice == "🤖 Bt-Ai Chat":
    st.title("🤖 Intelligent Assistant")
    user_input = st.chat_input("Ask about traffic, bank, or system status...")
    if user_input:
        st.chat_message("user").write(user_input)
        # Clear English Response
        st.chat_message("assistant").write(f"Confirmed. Analyzing: '{user_input}'. All global servers are 100% operational.")
