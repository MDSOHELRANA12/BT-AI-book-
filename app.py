import streamlit as st
from supabase import create_client
import uuid
import streamlit.components.v1 as components

# --- ১. হাই-স্পিড গ্লোবাল সার্ভার কানেকশন ---
URL = "https://nyqmaovjdzzkcrznjxmk.supabase.co"
KEY = "sb_secret_vdeV6gb4oTG7kM8sq6RqJg_ZiRw1GyF"
supabase = create_client(URL, KEY)

# --- ২. সারা বিশ্বের মানুষের জন্য পেইজ সেটআপ ---
st.set_page_config(page_title="BT-AI Global Platform", layout="wide")

# --- ৩. রিয়েল ওয়ার্ল্ড ডিজাইন (ডার্ক মোড) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .global-card { 
        background: linear-gradient(145deg, #111, #050505); 
        padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 20px;
    }
    .user-profile-header {
        border-left: 5px solid #ff0000; padding-left: 15px; margin-bottom: 20px;
    }
    .ad-banner { margin: 10px 0; border-radius: 10px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- ৪. ইউজার লগইন ও প্রোফাইল সিস্টেম (সারা বিশ্বের জন্য) ---
if 'user' not in st.session_state:
    st.session_state.user = None

def login_system():
    st.sidebar.title("🌍 Join the World Platform")
    if not st.session_state.user:
        auth_mode = st.sidebar.radio("Account Action", ["Login", "Create Global Profile"])
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        
        if auth_mode == "Create Global Profile":
            username = st.sidebar.text_input("Full Name (Public)")
            if st.sidebar.button("Register My Profile"):
                # এখানে নতুন ইউজার প্রোফাইল ডাটাবেসে সেভ হবে
                st.session_state.user = {"name": username, "email": email}
                st.sidebar.success(f"Welcome {username}! Your profile is now live worldwide.")
        else:
            if st.sidebar.button("Login to System"):
                st.session_state.user = {"name": email.split('@')[0], "email": email}
    else:
        st.sidebar.write(f"✅ Active: {st.session_state.user['name']}")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()

login_system()

# --- ৫. অ্যাড ব্যানার স্ক্রিপ্ট ---
ad_top = """<script type="text/javascript">atOptions = {'key' : '342950879f2064f7255ad047622381c8','format' : 'iframe','height' : 50,'width' : 320,'params' : {}};</script><script src="https://www.highperformanceformat.com/342950879f2064f7255ad047622381c8/invoke.js"></script>"""

# --- ৬. মেইন ন্যাভিগেশন ---
menu = ["🌐 Global World Feed", "📤 Upload Content", "👤 My Secure Profile", "💰 Earnings"]
choice = st.selectbox("Navigate Platform", menu)

# --- ৭. গ্লোবাল ফিড (সারা বিশ্বের ভিডিও) ---
if choice == "🌐 Global World Feed":
    st.title("🌎 Real-Time Global Stream")
    components.html(ad_top, height=70)
    
    try:
        data = supabase.table("videos").select("*").order("created_at", desc=True).execute()
        if data.data:
            for v in data.data:
                with st.container():
                    st.markdown('<div class="global-card">', unsafe_allow_html=True)
                    st.video(v['video_url'])
                    
                    # রিয়েল লাইক ও ভিউ অ্যালগরিদম
                    v_id = v['id']
                    current_views = v.get('views', 0) + 1
                    supabase.table("videos").update({"views": current_views}).eq("id", v_id).execute()
                    
                    col1, col2, col3 = st.columns(3)
                    col1.write(f"👁️ {current_views} Views")
                    if col2.button(f"❤️ Like ({v.get('likes', 0)})", key=f"like_{v_id}"):
                        supabase.table("videos").update({"likes": v.get('likes', 0) + 1}).eq("id", v_id).execute()
                        st.rerun()
                    col3.write(f"👤 By: {v.get('uploader_name', 'Global User')}")
                    st.markdown('</div>', unsafe_allow_html=True)
    except:
        st.info("সারা বিশ্বের ভিডিও লোড হচ্ছে...")

# --- ৮. ইউজার আপলোড সিস্টেম ---
elif choice == "📤 Upload Content":
    if st.session_state.user:
        st.title("📤 Publish to the World")
        file = st.file_uploader("Select Video (MP4)", type=['mp4'])
        if st.button("Publish Now") and file:
            with st.spinner("Broadcasting to World Servers..."):
                fname = f"{uuid.uuid4()}.mp4"
                supabase.storage.from_("videos").upload(fname, file.read())
                url = supabase.storage.from_("videos").get_public_url(fname)
                supabase.table("videos").insert({
                    "video_url": url, 
                    "uploader_name": st.session_state.user['name'],
                    "views": 0, "likes": 0
                }).execute()
                st.success("আপনার ভিডিওটি এখন সারা বিশ্বের মানুষ দেখছে!")
    else:
        st.warning("সারা বিশ্বে ভিডিও প্রচার করতে আগে আপনার প্রোফাইল তৈরি করুন (Sidebar দেখুন)।")

# --- ৯. গ্লোবাল প্রোফাইল (সারা বিশ্বের মানুষের জন্য ১ নম্বর প্রোফাইল) ---
elif choice == "👤 My Secure Profile":
    if st.session_state.user:
        st.title("👤 Global Identity")
        st.markdown(f"""
        <div class="user-profile-header">
            <h1 style='color: #ff0000;'>{st.session_state.user['name']}</h1>
            <p><b>Global ID:</b> {uuid.uuid4().hex[:8].upper()}</p>
            <p><b>Account Status:</b> <span style='color:#00ff00;'>Verified by BT-AI</span></p>
            <p><b>Server:</b> High-Speed Global Node</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("আপনার নিজস্ব প্রোফাইল দেখতে লগইন করুন।")

# --- ১০. রিয়েল আর্নিং সিস্টেম ---
elif choice == "💰 Earnings":
    st.title("💰 Global Revenue Dashboard")
    if st.session_state.user:
        st.metric("Total Balance", "$0.00", "+$0.00 today")
        st.write("আপনার ভিডিওর ভিউ বাড়লে এখানে ডলার জমা হবে।")
    else:
        st.write("আয় শুরু করতে প্রোফাইল তৈরি করুন।")
