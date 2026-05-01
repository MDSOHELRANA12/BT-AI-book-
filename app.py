import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime
from moviepy.editor import VideoFileClip 

# --- [জংশন বক্স শুরু] ---
MAIN_URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
MAIN_KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(MAIN_URL, MAIN_KEY)

# সোহেল ভাইয়ের ১০টি স্টোরেজ চাবি
STORAGE_KEYS = [
    {"url": "https://wzwhcuifcdkhjkvhndcp.supabase.co", "key": "sb_secret_bt9SDKvRqm9J91cZD-MAkw_caf0Gnkh"},
    {"url": "https://fypvwatkffekksbceofu.supabase.co", "key": "sb_secret_JeRIhaN33UZe9nTKgfMzwQ_Kc5rHL8o"},
    {"url": "https://osdjwtywivieuetnhxyo.supabase.co", "key": "sb_secret_ffiZGQ8XSUdAWXa26Ut2ww_-dVCfJy4"},
    {"url": "https://fiqjddgdpirdpbaccynt.supabase.co", "key": "sb_secret_kKfsUaR3Eyxp-W-ZLQYftg_9THDBB3C"},
    {"url": "https://ebkpbdjfeabqfwbkgvrg.supabase.co", "key": "sb_secret_HuxmaOONEyvFBqDB2yH_IQ_OcC6Pm4b"},
    {"url": "https://xjquucfkndfzawjscmdb.supabase.co", "key": "sb_secret_dRBwgkxRhwLwwYLSU92VBw_NUKkyX32"},
    {"url": "https://ziliihcgqsxnttrtupgm.supabase.co", "key": "sb_secret_GyhZd_60lAW6np0uBNjuBA_amZpgwUl"},
    {"url": "https://optlxxgrdmrvvkzwkmui.supabase.co", "key": "sb_secret_aKImpLhPtUkF3ggXgDKGRw_BJC7Qd_M"},
    {"url": "https://owlhzlgegmezedskzwgl.supabase.co", "key": "sb_secret_wOMZKz1TtugQNXFYgV4d4g_K82EnAl1"},
    {"url": "https://bczxwfclimiaaljjfegq.supabase.co", "key": "sb_secret_7rFR003t7a_N_VIEbf7aAw_WfPL7xRs"},
]

MAX_VIDEOS = 100 # ১০০ ভিডিওর বেশি হলে অটো ডিলিট হবে
DAILY_LIMIT = 3  # প্রতিদিন ৩টি ভিডিও লিমিট
# --- [জংশন বক্স শেষ] ---

st.set_page_config(page_title="BT AI book", layout="wide")

# --- অটো ডিলিট ফাংশন (সুপারভাইজার লোড কমাতে) ---
def delete_oldest_video():
    try:
        res = supabase.table("videos").select("*").order("created_at", desc=False).limit(1).execute()
        if res.data:
            old_video = res.data[0]
            v_url = old_video['video_url']
            v_id = old_video['id']
            for store in STORAGE_KEYS:
                if store['url'] in v_url:
                    s_bot = create_client(store['url'], store['key'])
                    file_path = v_url.split('/')[-1]
                    s_bot.storage.from_("videos").remove([file_path])
                    break
            supabase.table("videos").delete().eq("id", v_id).execute()
    except: pass

def format_value(value):
    if value >= 1000000: return f"{value/1000000:.1f}M"
    elif value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

# CSS ডিজাইন
st.markdown("""<style>.stApp { background-color: #000; color: #fff; }.video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 15px; padding: 15px; margin-bottom: 50px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); max-width: 500px; margin-left: auto; margin-right: auto; }.user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; }.username-text { font-weight: bold; font-size: 18px; color: #fff; }.stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }.btn-reward { display: block; width: 100%; padding: 12px; margin: 10px 0; background: linear-gradient(135deg, #ed1c24, #aa0000); color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; }</style>""", unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ইউজার সেশন ম্যানেজমেন্ট
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

# লগইন সিস্টেম
if not st.session_state.user:
    st.sidebar.header("🔐 User Login")
    u_name = st.sidebar.text_input("Enter Your Registered Name")
    if u_name:
        user_data = supabase.table("users").select("*").eq("username", u_name).execute()
        if user_data.data:
            if st.sidebar.button("Login"):
                st.session_state.user = u_name
                st.session_state.pic = user_data.data[0]['profile_pic']
                st.rerun()
        else:
            u_pic = st.sidebar.file_uploader("Upload Photo once", type=['jpg', 'png', 'jpeg'])
            if st.sidebar.button("Create Account"):
                if u_name and u_pic:
                    fname = f"p_{uuid.uuid4()}.jpg"
                    supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                    p_url = supabase.storage.from_("videos").get_public_url(fname)
                    supabase.table("users").insert({"username": u_name, "profile_pic": p_url}).execute()
                    st.session_state.user = u_name
                    st.session_state.pic = p_url
                    st.rerun()
else:
    st.sidebar.image(st.session_state.pic, width=100)
    st.sidebar.success(f"Profile: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

tab = st.sidebar.radio("Navigation", ["🌍 World Feed", "📤 Upload Video"])

# --- হাই স্পিড ওয়ার্ল্ড ফিড (অ্যালগরিদম) ---
if tab == "🌍 World Feed":
    try:
        # সব ভিডিও ডাটাবেজ থেকে আনা
        res = supabase.table("videos").select("*").execute()
        data = res.data if res.data else []
        
        # অ্যালগরিদম: ভিডিওগুলোকে এলোমেলো করা (যাতে পুরানো-নতুন মিক্স হয়ে ১টি ১টি করে আসে)
        random.shuffle(data)
        
        # লুপের মাধ্যমে একটি একটি ভিডিও কার্ড তৈরি
        for index, v in enumerate(data):
            v_id = v['id']
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><span class="username-text">{v.get("uploader_name", "BT User")}</span></div>', unsafe_allow_html=True)
            
            # ভিডিও প্লেয়ার
            st.video(v['video_url'])
            
            # ভিউ আপডেট
            try: supabase.table("videos").update({"views": v.get("views", 0) + 1}).eq("id", v_id).execute()
            except: pass
            
            st.markdown(f'<div style="margin: 12px 0;"><span class="stat-box">👁️ {format_value(v.get("views", 0)+1)} Views</span><span class="stat-box">❤️ {format_value(v.get("likes", 0))} Likes</span></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"❤️ Like", key=f"l_{v_id}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v_id).execute(); st.rerun()
            with col2:
                if st.button(f"➕ Follow", key=f"f_{v_id}"):
                    supabase.table("followers").insert({"user": v.get("uploader_name"), "follower": st.session_state.user}).execute()
                    st.success("Followed!")

            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521" target="_blank" class="btn-reward">💎 Claim Diamond Reward</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # প্রতি ২টি ভিডিওর পর একটি বিজ্ঞাপন (সার্ভার লোড কমাতে সাহায্য করে)
            if (index + 1) % 2 == 0:
                st.components.v1.html("""<div style="text-align:center;"><script type="text/javascript">atOptions = { 'key' : '342950879f2064f7255ad047622381c8', 'format' : 'iframe', 'height' : 50, 'width' : 320, 'params' : {} };</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script></div>""", height=70)
                
    except: st.error("ভিডিও লোড হতে সময় লাগছে... রিফ্রেশ করুন।")

# --- আপলোড সেকশন ---
elif tab == "📤 Upload Video":
    if st.session_state.user:
        v_file = st.file_uploader("Select MP4 (Max 15 Sec)", type=['mp4'])
        if st.button("🚀 Publish") and v_file:
            today = datetime.now().strftime("%Y-%m-%d")
            check = supabase.table("videos").select("*").eq("uploader_name", st.session_state.user).gte("created_at", today).execute()
            
            if len(check.data) >= DAILY_LIMIT:
                st.error(f"❌ ডেইলি লিমিট শেষ! আপনি কালকে আবার আপলোড করতে পারবেন।")
            else:
                with st.spinner("🤖 ভিডিও প্রসেস হচ্ছে..."):
                    try:
                        # অটো ডিলিট চেক (১০০ এর বেশি হলে)
                        count_res = supabase.table("videos").select("*", count='exact').execute()
                        if count_res.count and count_res.count >= MAX_VIDEOS:
                            delete_oldest_video()
                        
                        temp_in, temp_out = "temp_in.mp4", "temp_out.mp4"
                        with open(temp_in, "wb") as f: f.write(v_file.getvalue())
                        
                        clip = VideoFileClip(temp_in)
                        duration = clip.duration
                        clip.close()
                        
                        if duration > 16:
                            st.error(f"❌ ভিডিও ১৫ সেকেন্ডের বেশি!")
                            os.remove(temp_in)
                        else:
                            # হাই স্পিড কনভার্ট এবং সাইজ অপ্টিমাইজেশন
                            subprocess.run(f"ffmpeg -i {temp_in} -vcodec libx264 -crf 28 -maxrate 1M -bufsize 2M -y {temp_out}", shell=True)
                            v_uuid = f"v_{uuid.uuid4()}.mp4"
                            
                            # র‍্যান্ডম স্টোরেজ চাবি নির্বাচন
                            target = random.choice(STORAGE_KEYS)
                            storage_bot = create_client(target['url'], target['key'])
                            
                            with open(temp_out, "rb") as f:
                                storage_bot.storage.from_("videos").upload(path=v_uuid, file=f.read())
                            
                            v_url = storage_bot.storage.from_("videos").get_public_url(v_uuid)
                            
                            # ডাটাবেজে তথ্য সেভ
                            supabase.table("videos").insert({
                                "video_url": v_url, 
                                "uploader_name": st.session_state.user, 
                                "uploader_pic": st.session_state.pic, 
                                "likes": 0, "views": 0, 
                                "created_at": datetime.now().isoformat()
                            }).execute()
                            
                            st.success("✅ ভিডিও সফলভাবে পাবলিশ হয়েছে!")
                            os.remove(temp_in); os.remove(temp_out)
                    except Exception as e: st.error(f"Error: {e}")
