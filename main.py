import os
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

bg_url = "https://wmcppeiutkzrxrgwguvm.supabase.co/storage/v1/object/public/material/character_background_5.png"
st.markdown(f"""
<style>
.stApp {{
    background-image: url("{bg_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
</style>
""", unsafe_allow_html=True)

# config.yaml の絶対パス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

# 読み込み
with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    cookie_key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
)

# ログインフォーム
authenticator.login(
    location="main",
    fields={
        "Form name": "ログイン",
        "Username": "ユーザーID",
        "Password": "パスワード",
        "Login": "ログイン"
    }
)

status = st.session_state.get("authentication_status")

if status:
    with st.sidebar:
        st.markdown(f'## ようこそ、 *{st.session_state.get("name", "")}* さん')
        authenticator.logout('ログアウト', 'sidebar')
        st.divider()
    # st.write('# ログインしました!')

    page_home = st.Page(page="contents/temp_home.py", title="Home", icon="🏠")
    page_register_by_barcode = st.Page(page="contents/register_by_barcode.py", title="本のバーコードで登録・編集", icon="📝")
    page_book_ichiran = st.Page(page="contents/book_ichiran.py", title="書籍一覧", icon="📚")
    page_character = st.Page(page="contents/character.py", title="キャラクター", icon="🥚")
    pg = st.navigation([page_home, page_register_by_barcode, page_book_ichiran, page_character])
    pg.run()


elif status is False:
    st.error('ユーザーIDかパスワードが間違っています')
else:
    if st.button("ユーザー登録", key="go_register"):
        st.switch_page("register_user")
    # st.warning('ユーザーIDとパスワード、入力できましたか？')