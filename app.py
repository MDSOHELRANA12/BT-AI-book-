import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime
import streamlit.components.v1 as components

# ১. সুপাবেস কানেকশন ও জংশন বক্স (১০টি স্টোরেজ কি সহ)
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

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

# ২. ফরম্যাট ও অটো ক্লিনআপ লজিক (১০০ ভিডিও লিমিট)
def format_value(value):
    if value >= 1000000: return f"{value/1000000:.1f}M"
    elif value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

def auto_cleanup():
    res = supabase.table("videos").select("id", "video_url").order("created_at", desc=False).execute()
    if len(res.data) >= 100:
        old = res.data[0]
        v_url = old['video_url']
        v_name = v_url.split('/')[-1]
        for s in STORAGE_KEYS:
            if s['url'] in v_url:
                try: create_client(s['url'], s['key']).storage.from_("videos").remove([v_name])
                except: pass
        supabase.table("videos").delete().eq("id", old['id']).execute()

# ৩. ডিজাইন ও স্টাইল (আপনার অরিজিনাল সব বাটন এখানে আছে)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { 
        background: #0d0d0d; border: 1px solid #333; border-radius: 15px; 
        padding: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .user-avatar { 
        width: 50px; height: 50px; border-radius: 50%; 
        border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; 
    }
    .username-text { font-weight: bold; font-size: 18px; color: #fff; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    .btn-reward { 
        display: block; width: 100%; padding: 12px; margin: 10px 0; 
        background: linear-gradient(135deg, #ed1c24, #aa0000); 
        color: white !important; text-align: center; border-radius: 8px; 
        font-weight: bold; text-decoration: none;
    }
    .big-ad-box {
        background: #1a1a1a; border: 2px dashed #ed1c24; border-radius: 15px;
        padding: 25px; text-align: center; margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৪. লগইন সিস্টেম (আপনার অরিজিনাল লজিক)
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.pic = None

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

# ৫. মেইন ফিড (আপনার ডিজাইন + প্রতিটি ভিডিওর নিচে অ্যাড)
if tab == "🌍 World Feed":
    # জাভাস্ক্রিপ্ট অ্যাড স্ক্রিপ্ট
    ad_script = """
    <div style="text-align:center; margin: 10px 0;">
        <script type="text/javascript" src="https://pl29289908.profitablecpmratenetwork.com/75/f2/b3/75f2b3ea1ac23fb6fb2830593292cea8.js"></script>
    </div>
    """
    
    try:
        res = supabase.table("videos").select("*").execute()
        data = res.data if res.data else []
        random.shuffle(data)

        for index, v in enumerate(data):
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            # প্রোফাইল ছবি ও নাম
            st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><img src="{v.get("uploader_pic", "")}" class="user-avatar"><span class="username-text">{v.get("uploader_name", "BT User")}</span></div>', unsafe_allow_html=True)
            
            # ভিডিও প্লেয়ার
            st.video(v['video_url'])
            
            # ভিউ কাউন্ট আপডেট
            v_id = v['id']
            try: supabase.table("videos").update({"views": v.get("views", 0) + 1}).eq("id", v_id).execute()
            except: pass

            # আপনার অরিজিনাল স্ট্যাটাস বার
            st.markdown(f'''
                <div style="margin: 12px 0;">
                    <span class="stat-box">👁️ {format_value(v.get("views", 0)+1)} Views</span>
                    <span class="stat-box">❤️ {format_value(v.get("likes", 0))} Likes</span>
                    <span class="stat-box">👤 {format_value(v.get("followers", 0))} Followers</span>
                </div>
            ''', unsafe_allow_html=True)

            # আপনার অরিজিনাল রিওয়ার্ড বাটন
            st.markdown(f'<a href="https://www.profitablecpmratenetwork.com/your-link" class="btn-reward">🎁 Collect Reward / Watch Ad</a>', unsafe_allow_html=True)
            
            # লাইক ও ফলো বাটন লজিক (১০০% ফিক্সড)
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"❤️ Like", key=f"lk_{v_id}_{index}"):
                    supabase.table("videos").update({"likes": v.get("likes", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()
            with c2:
                if st.button(f"➕ Follow", key=f"fl_{v_id}_{index}"):
                    supabase.table("videos").update({"followers": v.get("followers", 0) + 1}).eq("id", v_id).execute()
                    st.rerun()

            # প্রতিটি ভিডিওর নিচে অটো জাভাস্ক্রিপ্ট অ্যাড
            components.html(ad_script, height=180)
            st.markdown('</div>', unsafe_allow_html=True)

            # ৫টি ভিডিও পর পর আপনার সেই "Big Ad Box"
            if (index + 1) % 5 == 0:
                st.markdown('''
                    <div class="big-ad-box">
                        <h3 style="color:#ed1c24;">🔥 Special Mega Reward 🔥</h3>
                        <p>Click below to unlock premium points!</p>
                        <a href="https://your-ad-link.com" class="btn-reward" style="width:250px; margin: 0 auto;">Claim Mega Prize</a>
                    </div>
                ''', unsafe_allow_html=True)

    except Exception as e:
        st.error("Feed Error")

# ৬. ভিডিও আপলোড (১৫ সেকেন্ড, ৩ লিমিট এবং ২ এমবি কনভার্ট)
elif tab == "📤 Upload Video":
    if not st.session_state.user:
        st.warning("Please login first to upload!")
    else:
        file = st.file_uploader("Select Video (Max 15s, Auto 2MB)", type=['mp4'])
        if st.button("🚀 Publish Video") and file:
            # দৈনিক ৩ ভিডিও লিমিট চেক
            today = datetime.now().strftime("%Y-%m-%d")
            check = supabase.table("videos").select("*").eq("uploader_name", st.session_state.user).gte("created_at", today).execute()
            
            if len(check.data) >= 3:
                st.error("Today's limit (3 videos) reached! Come back tomorrow.")
            else:
                with st.spinner("Converting & Compressing to 2MB..."):
                    auto_cleanup() # ১০০ ভিডিওর লিমিট চেক
                    t_in, t_out = "raw_in.mp4", "final_out.mp4"
                    with open(t_in, "wb") as f: f.write(file.getvalue())
                    
                    # FFMPEG: ১৫ সেকেন্ড + ২ এমবি + ব্রাউজার সাপোর্ট ফিক্স
                    cmd = f'ffmpeg -i {t_in} -t 15 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -pix_fmt yuv420p -crf 28 -b:v 1M -fs 1.9M -movflags +faststart -y {t_out}'
                    subprocess.run(cmd, shell=True)
                    
                    # র্যান্ডম স্টোরেজ সিলেক্ট করা
                    target = random.choice(STORAGE_KEYS)
                    s_bot = create_client(target['url'], target['key'])
                    v_uuid = f"v_{uuid.uuid4()}.mp4"
                    
                    with open(t_out, "rb") as f:
                        s_bot.storage.from_("videos").upload(v_uuid, f.read())
                    
                    v_url = s_bot.storage.from_("videos").get_public_url(v_uuid)
                    
                    # ডাটাবেজে ডাটা সেভ করা
                    supabase.table("videos").insert({
                        "video_url": v_url,
                        "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic,
                        "likes": 0,
                        "views": 0,
                        "followers": 0
                    }).execute()
                    
                    st.success("Video Published Successfully!")
                    os.remove(t_in); os.remove(t_out)
                    st.rerun()
