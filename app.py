import streamlit as st
import streamlit.components.v1 as components

st.title("অ্যাড ব্যানার টেস্টিং")

# আপনার দেওয়া অ্যাড কোডটি এখানে সাজানো হয়েছে
ad_script = """
<div style="text-align:center;">
    <script type="text/javascript" src="https://pl29289908.profitablecpmratenetwork.com/75/f2/b3/75f2b3ea1ac23fb6fb2830593292cea8.js"></script>
</div>
"""

st.write("নিচে যদি অ্যাড দেখা যায়, তবে বুঝবেন সিস্টেম রেডি:")

# অ্যাড শো করার জন্য কম্পোনেন্ট (উচ্চতা বা height আপনি বাড়িয়ে কমিয়ে নিতে পারেন)
components.html(ad_script, height=250, scrolling=True)

st.write("অ্যাড লোড হতে ৫-১০ সেকেন্ড সময় নিতে পারে।")
