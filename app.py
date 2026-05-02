import streamlit as st
from supabase import create_client
import uuid
import random
import os
import subprocess
from datetime import datetime
import streamlit.components.v1 as components

(google-site-verification: google7ed30cce8d663bc4.html)
# --- ১. গুগল ভেরিফিকেশন নতুন পদ্ধতি (URL Parameter দিয়ে) ---
# গুগল যখন আপনার সাইটে এই ফাইলটি খুঁজবে, কোডটি তখন তাকে 'google-site-verification' দেখাবে
query_params = st.query_params
if "google3O60nQs2GvZwmbI9SnedDrlRYi_Upwtzs3.html" in query_params or "google_verify" in query_params:
    st.write("google-site-verification: google3O60nQs2GvZwmbI9SnedDrlRYi_Upwtzs3.html")
    st.stop()

# সুপাবেস কানেকশন
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

# আগের মেটা ট্যাগটিও থাকল ব্যাকআপ হিসেবে
st.markdown("""
    <head>
        <meta name="google-site-verification" content="g3O60nQs2GvZwmbI9SnedDrlRYi_Upwtzs3" />
    </head>
""", unsafe_allow_html=True)

# বাকি সব ফাংশন এবং কোড আগের মতোই থাকবে (নিচে সংক্ষেপে দেওয়া হলো)
# ২. ফরম্যাট ও অটো ক্লিনআপ
def format_value(value):
    if value >= 1000: return f"{value/1000:.1f}K"
    return str(value)

def auto_cleanup(target_storage_url):
    res = supabase.table("videos").select("id", "video_url").like("video_url", f"%{target_storage_url}%").order("created_at", desc=False).execute()
    if len(res.data) >= 500:
        old = res.data[0]
        v_url = old['video_url']
        v_name = v_url.split('/')[-1]
        for s in STORAGE_KEYS:
            if s['url'] in v_url:
                try: create_client(s['url'], s['key']).storage.from_("videos").remove([v_name])
                except: pass
        supabase.table("videos").delete().eq("id", old['id']).execute()

# ৩. স্টাইল
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .video-card { background: #0d0d0d; border: 1px solid #333; border-radius: 15px; padding: 15px; margin-bottom: 25px; }
    .user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00ff00; object-fit: cover; margin-right: 12px; }
    .stat-box { font-size: 14px; color: #00ff00; font-weight: bold; margin-right: 15px; }
    .btn-direct { display: block; width: 100%; padding: 10px; margin: 5px 0; color: white !important; text-align: center; border-radius: 8px; font-weight: bold; text-decoration: none; font-size: 14px; }
    .bg-1 { background: linear-gradient(135deg, #FF416C, #FF4B2B); }
    .bg-2 { background: linear-gradient(135deg, #1DE9B6, #26A69A); }
    .bg-3 { background: linear-gradient(135deg, #667eea, #764ba2); }
    .bg-4 { background: linear-gradient(135deg, #f6d365, #fda085); }
    .banner-box { background: #1a1a1a; border: 1px dashed #ed1c24; padding: 15px; text-align: center; border-radius: 10px; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ BT AI book")

# ৪. লগইন ৫. ফিড ৬. আপলোড (আগের কোড বসিয়ে নিন)
# ... (বাকি কোড আপনার ফাইলে যেমন আছে তেমনই থাকবে)
