import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime

# --- [জংশন বক্স] ---
MAIN_URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
MAIN_KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(MAIN_URL, MAIN_KEY)

# ১০টি চাবি (ভিডিওর জন্য)
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
# --- [জংশন বক্স শেষ] ---

st.set_page_config(page_title="BT AI book", layout="wide")

# ডিজাইন (CSS)
st.markdown("""<style>.stApp { background-color: #000; color: #fff; }.video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 15px; padding: 15px; margin-bottom: 30px; max-width: 450px; margin-left: auto; margin-right: auto; }.profile-img { border-radius: 50%; border: 2px solid #00ff00; }</style>""", unsafe_allow_html=True)

if 'user' not in st.session_state: st.session_state.user = None

tab = st.sidebar.radio("BT Menu", ["🌍 World Feed", "📤 Upload Video", "🔐 Profile"])

# --- ১. অটো ডিলিট ফাংশন (পুরানো ভিডিও মোছার জন্য) ---
def auto_cleanup():
    # মোট ভিডিও সংখ্যা চেক করা
    res = supabase.table("videos").select("id", "video_url").order("created_at", desc=False).execute()
    total_videos = len(res.data)
    
    # যদি ভিডিও ১০০টির বেশি হয়, তবে সবচেয়ে পুরনোটি ডিলিট হবে
    if total_videos > 100:
        oldest_video = res.data[0]
        v_id = oldest_video['id']
        v_url = oldest_video['video_url']
        
        # স্টোরেজ থেকে ভিডিও ডিলিট করা (১০টি চাবির মধ্যে খুঁজে বের করে)
        v_name = v_url.split('/')[-1]
        for storage in STORAGE_KEYS:
            if storage['url'] in v_url:
                try:
                    s_client = create_client(storage['url'], storage['key'])
                    s_client.storage.from_("videos").remove([v_name])
                    break
                except: pass
        
        # ডাটাবেজ থেকে ডিলিট করা
        supabase.table("videos").delete().eq("id", v_id).execute()

# --- প্রোফাইল লগইন ও রেজিস্ট্রেশন ---
if tab == "🔐 Profile":
    if not st.session_state.user:
        auth_mode = st.radio("অ্যাকশন বেছে নিন", ["লগইন করুন", "নতুন অ্যাকাউন্ট খুলুন"])
        u_name = st.text_input("ইউজার নাম")
        u_pass = st.text_input("পাসওয়ার্ড", type="password")
        
        if auth_mode == "নতুন অ্যাকাউন্ট খুলুন":
            u_pic = st.file_uploader("প্রোফাইল ফটো আপলোড (একবারই লাগবে)", type=['jpg','png'])
            if st.button("রেজিস্ট্রেশন করুন"):
                if u_name and u_pass and u_pic:
                    fname = f"profile_{uuid.uuid4()}.jpg"
                    supabase.storage.from_("videos").upload(path=fname, file=u_pic.getvalue())
                    p_url = supabase.storage.from_("videos").get_public_url(fname)
                    try:
                        supabase.table("users").insert({
                            "username": u_name, "password": u_pass, "profile_pic": p_url
                        }).execute()
                        st.success("অ্যাকাউন্ট তৈরি হয়েছে! এখন লগইন ট্যাবে যান।")
                    except: st.error("এই নামটি অন্য কেউ ব্যবহার করছে!")
                else: st.warning("সবগুলো ঘর পূরণ করুন!")
        else: # লগইন
            if st.button("লগইন"):
                res = supabase.table("users").select("*").eq("username", u_name).eq("password", u_pass).execute()
                if res.data:
                    st.session_state.user = u_name
                    st.session_state.pic = res.data[0]['profile_pic']
                    st.rerun()
                else: st.error("ভুল নাম বা পাসওয়ার্ড!")
    else:
        st.image(st.session_state.pic, width=150)
        st.title(f"স্বাগতম, {st.session_state.user}")
        if st.button("লগআউট"):
            st.session_state.user = None
            st.rerun()

# --- ভিডিও ফিড ---
elif tab == "🌍 World Feed":
    st.title("🛡️ BT AI book")
    res = supabase.table("videos").select("*").order("created_at", desc=True).execute()
    for v in res.data:
        st.markdown(f'<div class="video-card">', unsafe_allow_html=True)
        st.markdown(f"**<img src='{v['uploader_pic']}' width='30' class='profile-img' style='vertical-align:middle;'> {v['uploader_name']}**", unsafe_allow_html=True)
        st.video(v['video_url'])
        st.markdown(f'👁️ {v["views"]} | ❤️ {v["likes"]} | 👥 {v["followers"]}', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- ভিডিও আপলোড ---
elif tab == "📤 Upload Video":
    if not st.session_state.user:
        st.warning("আগে প্রোফাইল থেকে লগইন করুন!")
    else:
        file = st.file_uploader("ভিডিও নির্বাচন করুন (১৫ সেকেন্ড ও ২ এমবি হবে অটো)", type=['mp4'])
        if st.button("🚀 Publish") and file:
            today = datetime.now().strftime("%Y-%m-%d")
            check = supabase.table("videos").select("*").eq("uploader_name", st.session_state.user).gte("created_at", today).execute()
            
            if len(check.data) >= 3:
                st.error("আজকের ৩টি ভিডিওর লিমিট শেষ হয়ে গেছে!")
            else:
                with st.spinner("ভিডিও প্রসেস ও ২ এমবি-তে রূপান্তর হচ্ছে..."):
                    # অটো-ক্লিনআপ রান করা (আপলোডের আগে জায়গা খালি করবে)
                    auto_cleanup()
                    
                    t_in, t_out = "temp_in.mp4", "temp_out.mp4"
                    with open(t_in, "wb") as f: f.write(file.getvalue())
                    
                    subprocess.run(f"ffmpeg -i {t_in} -t 15 -vcodec libx264 -crf 28 -fs 2M -y {t_out}", shell=True)
                    
                    target = random.choice(STORAGE_KEYS)
                    s_bot = create_client(target['url'], target['key'])
                    v_uuid = f"v_{uuid.uuid4()}.mp4"
                    
                    with open(t_out, "rb") as f:
                        s_bot.storage.from_("videos").upload(path=v_uuid, file=f.read())
                    v_url = s_bot.storage.from_("videos").get_public_url(v_uuid)
                    
                    supabase.table("videos").insert({
                        "video_url": v_url, 
                        "uploader_name": st.session_state.user,
                        "uploader_pic": st.session_state.pic,
                        "likes": random.randint(10,50),
                        "views": random.randint(50,200)
                    }).execute()
                    
                    st.success("সফলভাবে পাবলিশ হয়েছে!")
                    os.remove(t_in); os.remove(t_out)
