# --- ২. ওয়ার্ল্ড ফিড (ভিডিও ও অটো অ্যাড) ---
if tab == "🌍 World Feed":
    st.title("🛡️ BT AI book")
    
    # অ্যাড কোড স্লট (সহজে পরিবর্তন করার জন্য এখানে রাখা হয়েছে)
    ad_html = """
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
            
            # ভিডিও প্লেয়ার
            st.video(v['video_url'])
            
            # লাইক ও ফলো বাটন
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
            
            # --- অটোমেটিক অ্যাড স্লট ---
            # প্রতিটি ভিডিওর নিচেই এই অ্যাডটি শো হবে
            import streamlit.components.v1 as components
            components.html(ad_html, height=150) # হাইট আপনার প্রয়োজনমতো বাড়িয়ে কমিয়ে নিতে পারেন
            
            st.markdown("<hr style='border: 0.1px solid #222;'>", unsafe_allow_html=True)
