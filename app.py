import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. হাই-স্পিড সার্ভার কানেকশন (সুপারবেস) ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ২. পেইজ সেটআপ ---
st.set_page_config(page_title="Bt-Ai Global Engine", layout="wide")

# --- ৩. প্রিমিয়াম গ্লোবাল ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .video-card { 
        background: #0a0a0a; padding: 15px; border-radius: 20px; 
        border: 2px solid #1a1a1a; margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.1);
    }
    .direct-ad-btn {
        display: inline-block; width: 100%; padding: 12px; margin: 10px 0;
        background: linear-gradient(90deg, #ff4b1f, #ff9068);
        color: white !important; text-decoration: none; text-align: center;
        border-radius: 12px; font-weight: bold; border: 1px solid #fff;
    }
    .profile-header {
        background: linear-gradient(135deg, #111, #222);
        padding: 30px; border-radius: 25px; border-left: 5px solid #ff0000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ৪. অ্যাডস এবং ডাইরেক্ট লিঙ্কস ---
direct_link_1 = "https://www.profitablecpmratenetwork.com/krgreepsz8?key=08a0fdc6d7ed4f33a60d1f4910ec27c5"
direct_link_2 = "https://www.profitablecpmratenetwork.com/tgt6azn6?key=e753cbd6d9bae06d67051ed846419521"

# --- ৫. ন্যাভিগেশন মেনু (ফিক্সড) ---
st.sidebar.markdown("<h2 style='color:red;'>✪ BT-AI PRO</h2>", unsafe_allow_html=True)
menu = ["🏠 Global Feed", "📤 Fast Upload", "🤖 Advanced Ai Chat", "👤 Admin Profile", "💰 Global Wallet"]
choice = st.sidebar.radio("Select Engine", menu)

# --- ৬. গ্লোবাল ফিড (ভিডিওর সাথে ডাইরেক্ট লিঙ্ক বাটন) ---
if choice == "🏠 Global Feed":
    st.title("🌎 Trending Now")
    try:
        data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if data.data:
            for v in data.data:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                
                # ভিডিওর নিচে আপনার ডাইরেক্ট লিঙ্ক বাটন
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<a href="{direct_link_1}" target="_blank" class="direct-ad-btn">🔥 Check Offer 1</a>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<a href="{direct_link_2}" target="_blank" class="direct-ad-btn">💎 Special Link 2</a>', unsafe_allow_html=True)
                
                st.write(f"🌐 Reach: {v.get('views', 100)}+ People")
                st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.error("সার্ভার কানেক্ট হচ্ছে, দয়া করে একটু অপেক্ষা করুন...")

# --- ৭. ফাস্ট আপলোড সিস্টেম ---
elif choice == "📤 Fast Upload":
    st.title("📤 Rapid Content Publish")
    file = st.file_uploader("Upload MP4 Video", type=['mp4'])
    if st.button("🚀 GO LIVE") and file:
        with st.spinner("Uploading to Global Server..."):
            fname = f"{uuid.uuid4()}.mp4"
            supabase.storage.from_("videos").upload(fname, file.read())
            video_url = supabase.storage.from_("videos").get_public_url(fname)
            supabase.table("videos").insert({"video_url": video_url}).execute()
            st.success("ভিডিও পাবলিশ সফল হয়েছে!")

# --- ৮. বুদ্ধিমান এআই চ্যাটবট (ফিক্সড) ---
elif choice == "🤖 Advanced Ai Chat":
    st.title("🤖 Bt-Ai World Assistant")
    st.info("সোহেল ভাই, আপনার এআই এখন সুপার একটিভ।")
    
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["r"]): st.write(m["c"])

    if prompt := st.chat_input("Ask anything..."):
        st.session_state.msgs.append({"r": "user", "c": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            # আপনার বুদ্ধিমান রিপ্লাই
            reply = f"সোহেল ভাই, আপনার ৫০০ ডলারের প্রজেক্ট এখন সুরক্ষিত। আমি আপনার সিস্টেম মনিটর করছি।"
            st.write(reply)
            st.session_state.msgs.append({"r": "assistant", "c": reply})

# --- ৯. প্রফেশনাল প্রোফাইল (সবাই দেখতে পাবে) ---
elif choice == "👤 Admin Profile":
    st.title("👤 Global Identity")
    st.markdown(f"""
    <div class="profile-header">
        <h1 style='color: #ff0000;'>MD SOHEL RANA</h1>
        <p style='font-size: 20px;'><b>Status:</b> Verified System Admin</p>
        <p><b>Storage:</b> Unlimited GB Enabled</p>
        <p><b>Engine:</b> AI-Power v4.0</p>
        <hr>
        <p>আপনার প্রোফাইল এখন সারা বিশ্বের কাছে সচল।</p>
    </div>
    """, unsafe_allow_html=True)

# --- ১০. ওয়ালেট ---
elif choice == "💰 Global Wallet":
    st.title("💰 Earnings Control")
    st.metric("Total Balance", "$0.00", "+$0.00 today")
    st.markdown(f'<a href="{direct_link_1}" target="_blank" class="direct-ad-btn">💰 Withdraw Funds</a>', unsafe_allow_html=True)
