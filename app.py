import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime
import streamlit.components.v1 as components

# --- [জংশন বক্স] ---
MAIN_URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
MAIN_KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(MAIN_URL, MAIN_KEY)

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

st.set_page_config(page_title="BT AI book", layout="centered")

# --- ডিজাইন এবং স্টাইল ---
st.markdown("""
<style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #111; border-radius: 15px; padding: 10px; margin-bottom: 5px; border: 1px solid #333; }
    .profile-header { display: flex; align-items: center; gap: 10px; padding: 8px; }
    .profile-pic { width: 40px; height: 40px; border-radius: 50%; border: 2px solid #00ff00; object-fit: cover; }
</style>
""", unsafe_allow_html=True)

if 'user' not in st.session_state: st.session_state.user = None

# --- ১. অটো ক্লিনআপ ---
def auto_cleanup():
    res = supabase.table("videos").select("id", "video_url").order("created_at", desc=False).execute()
    if len(res.data) >= 100:
        old = res.data[0]
        v_name = old['video_url'].split('/')[-1]
        for s in STORAGE_KEYS:
            if s['url'] in old['video_url']:
                try: create_client(s['url'], s['key']).storage.from_("videos").remove([v_name])
                except: pass
        supabase.table("videos").delete().eq("id", old['id']).execute()

tab = st.sidebar.radio("BT Menu", ["🌍 World Feed", "📤 Upload Video", "🔐 Profile"])

# --- ২. ওয়ার্ল্ড ফিড (ভিডিও ও প্রতিটি ভিডিওর নিচে অ্যাড) ---
if tab == "🌍 World Feed":
    st.title("🛡️ BT AI book")
    
    # আপনার দেওয়া অ্যাড কোড স্লট
    ad_script = """
    <div style="text-align:center; margin: 10px 0;">
        <script type="text/javascript" src="https://pl29289908.profitablecpmratenetwork.com/75/f2/b3/75f2b3ea1ac23fb6fb2830593292cea8.js"></script>
    </div>
    """
    
    res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    
    for v in res.data:
        with st.container():
            # প্রোফাইল ছবি ও নাম
            st.markdown(f'''
            <div class="profile-header">
                <img src="{v.get('uploader_pic', '')}" class="profile-pic">
                <b>{v['uploader_name']}</b>
            </div>
            ''', unsafe_allow_html=True)
            
            # ভিডিও প্লেয়ার (ব্রাউজার সাপোর্ট ফিক্সড)
            st.video(v['video_url'])
            
            # লাইক, ভিউ এবং ফলোয়ার বাটন
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(f"❤️ {v.get('likes', 0)}", key=f"lk_{v['id']}"):
                    supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v['id']).execute()
                    st.rerun()
            with c2:
                st.markdown(f"👁️ {v.get('views', 0)}")
            with c3:
                fol = v.get('followers', 0)
                if st.button(f"👥 Follow ({fol})", key=f"fl_{v['id']}"):
                    supabase.table("videos").update({"followers": fol + 1}).eq("id", v['id']).execute()
                    st.toast(f"Followed {v['uploader_name']}")
                    st.rerun()
            
            # --- প্রতিটি ভিডিওর ঠিক নিচে অ্যাড লোড হবে ---
            components.html(ad_script, height=200) 
            
            st.markdown("<hr style='border: 0.1px solid #222;'>", unsafe_allow_html=True)

# --- ৩. ভিডিও আপলোড (২ এমবি ও ব্রাউজার ফ্রেন্ডলি কনভার্ট) ---
elif tab == "📤 Upload Video":
    if not st.session_state.user:
        st.error("আগে লগইন করুন!")
    else:
        file = st.file_uploader("ভিডিও সিলেক্ট করুন (অটো ২ এমবি হবে)", type=['mp4'])
        if st.button("🚀 Publish") and file:
            today = datetime.now().strftime("%Y-%m-%d")
            check = supabase.table("videos").select("*").eq("uploader_name", st.session_state.user).gte("created_at", today).execute()
            
            if len(check.data) >= 3:
                st.error("আজকের ৩টি ভিডিওর লিমিট শেষ!")
            else:
                with st.spinner("ভিডিও প্রসেসিং হচ্ছে..."):
                    auto_cleanup() # স্টোরেজ চেক
                    t_in, t_out = "in.mp4", "out.mp4"
                    with open(t_in, "wb") as f: f.write(file.getvalue())
                    
                    # ব্রাউজারে যেন ভিডিও আটকে না যায় এবং ২ এমবি-র নিচে থাকে
                    cmd = f'ffmpeg -i {t_in} -t 15 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -pix_fmt yuv420p -crf 28 -b:v 1M -fs 1.9M -movflags +faststart -y {t_out}'
                    subprocess.run(cmd, shell=True)
                    
                    target = random.choice(STORAGE_KEYS)
                    s_bot = create_client(target['url'], target['key'])
                    v_name = f"v_{uuid.uuid4()}.mp4"
                    
                    with open(t_out, "rb") as f:
                        s_bot.storage.from_("videos").upload(v_name, f.read())
                    
                    v_url = s_bot.storage.from_("videos").get_public_url(v_name)
                    
                    supabase.table("videos").insert({
                        "video_url": v_url,
                        "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic,
                        "likes": 0,
                        "views": random.randint(10, 100),
                        "followers": 0
                    }).execute()
                    
                    st.success("পাবলিশ হয়েছে!")
                    os.remove(t_in); os.remove(t_out)
                    st.rerun()

# --- ৪. প্রোফাইল ---
elif tab == "🔐 Profile":
    if not st.session_state.user:
        u_name = st.text_input("ইউজার নাম")
        u_pass = st.text_input("পাসওয়ার্ড", type="password")
        if st.button("লগইন"):
            res = supabase.table("users").select("*").eq("username", u_name).eq("password", u_pass).execute()
            if res.data:
                st.session_state.user = u_name
                st.session_state.pic = res.data[0]['profile_pic']
                st.rerun()
            else: st.error("ভুল নাম বা পাসওয়ার্ড!")
    else:
        st.image(st.session_state.pic, width=120)
        st.header(f"স্বাগতম, {st.session_state.user}")
        if st.button("লগআউট"):
            st.session_state.user = None
            st.rerun()
