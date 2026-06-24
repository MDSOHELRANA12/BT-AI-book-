import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime
import streamlit.components.v1 as components

# ১. মেটা ট্যাগ ও ভেরিফিকেশন
st.markdown(
    """
    <head>
        <meta name="msvalidate.01" content="e776b8ce73ea3dcc07551e8a021a0907">
        <meta name="monetag" content="5cc1b7ba5cb29eff802ce49009f87e2b">
    </head>
    """,
    unsafe_allow_html=True
)

SMART_LINK = "https://omg10.com/4/10954816"

# ২. সুপাবেস কানেকশন (সুরক্ষিত উপায়ে secrets থেকে নেওয়া)
try:
    URL = st.secrets["SUPABASE_URL"]
    KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    # ব্যাকআপ বা লোকাল টেস্টের জন্য (লোকালি না চললে সরাসরি secrets ব্যবহার হবে)
    URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
    KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"

supabase = create_client(URL, KEY)

# স্টোরেজ কি-গুলো ডাইনামিকালি সেটিংস থেকে লোড করা হবে সুরক্ষার জন্য
STORAGE_KEYS = []
if "STORAGE_KEYS" in st.secrets:
    STORAGE_KEYS = st.secrets["STORAGE_KEYS"]
else:
    # সিক্রেটস সেটআপ না করা পর্যন্ত ব্যাকআপ সোর্স
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

st.set_page_config(page_title="BT AI book", layout="wide")

# ৩. ফরম্যাট ও অটো ক্লিনআপ
def format_value(value):
    if value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

def auto_cleanup(target_storage_url):
    try:
        res = supabase.table("videos").select("id", "video_url").like("video_url", f"%{target_storage_url}%").order("created_at", ascending=True).execute()
        data = res.data if hasattr(res, 'data') else res
        if data and len(data) >= 500:
            old = data[0]
            v_url = old['video_url']
            v_name = v_url.split('/')[-1]
            for s in STORAGE_KEYS:
                if s['url'] in v_url:
                    try: create_client(s['url'], s['key']).storage.from_("videos").remove([v_name])
                    except: pass
            supabase.table("videos").delete().eq("id", old['id']).execute()
    except:
        pass

def show_auto_moving_banner():
    ad_html = f"""
    <div style="text-align:center; margin: 10px 0;">
        <a href="{SMART_LINK}" target="_blank" style="text-decoration:none;">
            <div style="background: linear-gradient(90deg, #00c853, #000); 
                        color: #fff; padding: 15px; border-radius: 10px; 
                        border: 2px solid #00c853; font-family: sans-serif;">
                <span style="font-size: 18px; font-weight: bold;">⚡ PREMIUM REWARD ACTIVE ⚡</span><br>
                <span style="font-size: 12px;">Click to Claim Your Diamond Bonus!</span>
            </div>
        </a>
    </div>
    """
    components.html(ad_html, height=120)

# ৪. একদম সাদা ব্যাকগ্রাউন্ড ডিজাইন
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; }
    .video-card { background: #ffffff; border: 1px solid #ddd; border-radius: 15px; padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00c853; object-fit: cover; margin-right: 12px; }
    .stat-box { font-size: 14px; color: #333; font-weight: bold; margin-right: 15px; }
    .btn-direct { display: block; width: 100%; padding: 12px; margin: 8px 0; color: white !important; text-align: center; border-radius: 10px; font-weight: bold; text-decoration: none; font-size: 15px; }
    .bg-1 { background: linear-gradient(135deg, #FF416C, #FF4B2B); }
    .bg-2 { background: linear-gradient(135deg, #1DE9B6, #26A69A); }
    .bg-3 { background: linear-gradient(135deg, #667eea, #764ba2); }
    .bg-4 { background: linear-gradient(135deg, #f6d365, #fda085); }
    .banner-box { background: #fff; border: 1px dashed #ed1c24; padding: 15px; text-align: center; border-radius: 10px; margin: 15px 0; color: #000; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৫. লগইন সিস্টেম
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

if not st.session_state.user:
    u_name = st.sidebar.text_input("Name")
    if u_name:
        user_data_res = supabase.table("users").select("*").eq("username", u_name).execute()
        user_data = user_data_res.data if hasattr(user_data_res, 'data') else user_data_res
        if user_data:
            if st.sidebar.button("Login"):
                st.session_state.user = u_name
                st.session_state.pic = user_data[0]['profile_pic']
                st.rerun()
        else:
            u_pic = st.sidebar.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'])
            if st.sidebar.button("Join Now"):
                if u_name and u_pic:
                    fname = f"p_{uuid.uuid4()}.jpg"
                    supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                    p_url = supabase.storage.from_("videos").get_public_url(fname)
                    supabase.table("users").insert({"username": u_name, "profile_pic": p_url}).execute()
                    st.session_state.user = u_name
                    st.session_state.pic = p_url
                    st.rerun()
else:
    if st.session_state.pic:
        st.sidebar.image(st.session_state.pic, width=80)
    st.sidebar.write(f"Hello, **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.pic = None
        st.rerun()

tab = st.sidebar.radio("Menu", ["🌍 World Feed", "📤 Upload Video"])

# ৬. মেইন ফিড (ভিডিও দেখার অংশ)
if tab == "🌍 World Feed":
    try:
        res = supabase.table("videos").select("*").execute()
        data = res.data if hasattr(res, 'data') else res
        data = data if data else []
        random.shuffle(data)
        
        for index, v in enumerate(data):
            v_id = str(v['id']) 
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:12px; color:#000;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><b>{v.get("uploader_name")}</b></div>', unsafe_allow_html=True)
            
            # ভিডিও রেন্ডারিং
            st.video(v['video_url'])
            
            # ভিউ আপডেট
            try: supabase.table("videos").update({"views": v.get("views", 0) + 1}).eq("id", v_id).execute()
            except: pass

            show_auto_moving_banner()

            st.markdown(f'''
                <div class="banner-box">
                    <a href="{SMART_LINK}" target="_blank" 
                       style="background:#ed1c24; color:white; padding:10px 25px; border-radius:5px; text-decoration:none; font-weight:bold; display:inline-block;">Click to Win Reward 🎁</a>
                </div>
                <div style="margin: 10px 0; display: flex; justify-content: start;">
                    <span class="stat-box">👁️ {format_value(v.get("views", 0))} Views</span>
                    <span class="stat-box">❤️ {format_value(v.get("likes", 0))} Likes</span>
                    <span class="stat-box">👤 {format_value(v.get("followers", 0))} Followers</span>
                </div>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-1">💰 High CPC Reward 1</a>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-2">💎 Premium Bonus 2</a>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-3">🚀 Mega Earning 3</a>
                <a href="{SMART_LINK}" target="_blank" class="btn-direct bg-4">🎁 Special Gift 4</a>
            ''', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"lk_{v_id}_{index}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"fl_{v_id}_{index}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Feed Error: {e}")

# ৭. ভিডিও আপলোড
elif tab == "📤 Upload Video":
    if not st.session_state.user: 
        st.warning("Login first!")
    else:
        st.markdown("<h3 style='color:#000;'>Upload Your Video</h3>", unsafe_allow_html=True)
        file = st.file_uploader("Select Video", type=['mp4'])
        if st.button("🚀 Publish Video") and file:
            today = datetime.now().strftime("%Y-%m-%d")
            check_res = supabase.table("videos").select("*").eq("uploader_name", st.session_state.user).gte("created_at", today).execute()
            check_data = check_res.data if hasattr(check_res, 'data') else check_res
            
            if check_data and len(check_data) >= 3:
                st.error("Daily limit reached!")
            else:
                with st.spinner("Publishing..."):
                    target = random.choice(STORAGE_KEYS)
                    auto_cleanup(target['url'])
                    t_in, t_out = "raw.mp4", "final.mp4"
                    with open(t_in, "wb") as f: f.write(file.getvalue())
                    
                    # ২০ সেকেন্ড এবং ৩ এমবি লিমিট কম্প্রেশন
                    cmd = f'ffmpeg -i {t_in} -t 20 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -fs 2.9M -y {t_out}'
                    subprocess.run(cmd, shell=True)
                    
                    try:
                        s_bot = create_client(target['url'], target['key'])
                        v_name = f"v_{uuid.uuid4()}.mp4"
                        with open(t_out, "rb") as f: 
                            s_bot.storage.from_("videos").upload(v_name, f.read())
                        v_url = s_bot.storage.from_("videos").get_public_url(v_name)
                        
                        supabase.table("videos").insert({
                            "video_url": v_url, 
                            "uploader_name": st.session_state.user,
                            "uploader_pic": st.session_state.pic, 
                            "likes": random.randint(20, 50), 
                            "views": random.randint(850, 1200), 
                            "followers": random.randint(100, 150)
                        }).execute()
                        
                        st.success("Published!")
                    except Exception as upload_err:
                        st.error(f"Upload failed: {upload_err}")
                    
                    if os.path.exists(t_in): os.remove(t_in)
                    if os.path.exists(t_out): os.remove(t_out)
                    st.rerun()
