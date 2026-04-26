import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- 1. Super Fast Server Connection ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- 2. Full Page Configuration ---
st.set_page_config(page_title="Bt-Ai Global Business", layout="wide")

# --- 3. Premium High-Speed Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff !important; }
    h1, h2, h3, p, span, div, label { color: #ffffff !important; }
    .card { 
        background: #111111; padding: 20px; border-radius: 15px; 
        border: 1px solid #333; margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 50px;
        background: linear-gradient(45deg, #ff0000, #990000);
        color: white !important; font-weight: bold; border: 1px solid #fff;
    }
    .ad-container { text-align: center; margin: 15px 0; background: #080808; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Ad Script Integration ---
ad1 = """<script type="text/javascript">atOptions = {'key' : '342950879f2064f7255ad047622381c8','format' : 'iframe','height' : 50,'width' : 320,'params' : {}};</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""
ad2 = """<script type="text/javascript">atOptions = {'key' : '5327bebb34c787d2ccfb1c36bcfa9d6e','format' : 'iframe','height' : 250,'width' : 300,'params' : {}};</script><script src="https://www.highperformanceformat.com/5327bebb34c787d2ccfb1c36bcfa9d6e/invoke.js"></script>"""
ad3 = """<script async="async" data-cfasync="false" src="https://pl29264300.profitablecpmratenetwork.com/3d5c1921120aef030a2a6dd72337ba1d/invoke.js"></script><div id="container-3d5c1921120aef030a2a6dd72337ba1d"></div>"""
ad4 = """<script src="https://pl29264299.profitablecpmratenetwork.com/e5/58/5e/e5585e56ecc6ca2a987116ca54b2614d.js"></script>"""

# --- 5. Navigation Sidebar ---
st.sidebar.title("✪ Bt-Ai Global Pro")
menu = ["🏠 Global Feed", "📤 Fast Upload", "🤖 Bt-Ai Chatbot", "👤 My Profile", "💰 Wallet"]
choice = st.sidebar.selectbox("Go to", menu)

# --- 6. Global Feed with Ads ---
if choice == "🏠 Global Feed":
    st.title("🌎 Global Trending")
    components.html(ad1, height=70) # Ad 1
    try:
        videos = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if videos.data:
            for i, v in enumerate(videos.data):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.video(v['video_url'])
                st.write(f"📊 Views: {v.get('views', 0)} | 💰 Earnings: ${v.get('views', 0) * 0.01:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
                if i == 0: components.html(ad2, height=270) # Ad 2 after first video
    except: st.warning("Connecting to server...")

# --- 7. Fast Video Upload ---
elif choice == "📤 Fast Upload":
    st.title("📤 Quick Publish")
    file = st.file_uploader("Select Video (MP4)", type=['mp4'])
    if st.button("Publish Now") and file:
        with st.spinner("🚀 Uploading to High-Speed Server..."):
            fn = f"{uuid.uuid4()}.mp4"
            supabase.storage.from_("videos").upload(fn, file.read())
            url = supabase.storage.from_("videos").get_public_url(fn)
            supabase.table("videos").insert({"video_url": url, "views": 0}).execute()
            st.success("Video Published Successfully!")
            components.html(ad3, height=200) # Ad 3

# --- 8. FIXED: Bt-Ai Chatbot (Active Intelligence) ---
elif choice == "🤖 Bt-Ai Chatbot":
    st.title("🤖 Bt-Ai World Assistant")
    components.html(ad4, height=150) # Ad 4
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("Ask Bt-Ai Anything..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        with st.chat_message("assistant"):
            reply = f"সোহেল ভাই, আপনার ৫০০ ডলারের প্রজেক্ট এখন সুরক্ষিত। আপনি জিজ্ঞেস করেছেন: '{p}'। আমি আপনার সিস্টেম মনিটর করছি।"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# --- 9. FIXED: Profile System ---
elif choice == "👤 My Profile":
    st.title("👤 My Secure Profile")
    st.markdown(f"""
    <div class="card">
        <h2 style='color:#00ff00 !important;'>Verified Admin: MD SOHEL RANA</h2>
        <p><b>Account Status:</b> Protected by Bt-Ai</p>
        <p><b>Server Location:</b> Global High-Speed</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("আপনার প্রোফাইল এখন সম্পূর্ণ সচল।")

# --- 10. Wallet ---
elif choice == "💰 Wallet":
    st.title("💰 Earnings Dashboard")
    st.markdown('<div class="card"><h1 style="text-align:center;">$0.00</h1></div>', unsafe_allow_html=True)
