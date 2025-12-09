import os
import streamlit as st
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from supabase import create_client

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

st.title("新規ユーザー登録")

# Supabase 接続
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

with st.form("register_form"):
    new_username = st.text_input("ユーザーID")
    new_name = st.text_input("表示名")
    new_email = st.text_input("メールアドレス")
    new_password = st.text_input("パスワード", type="password")
    submitted = st.form_submit_button("登録")

if submitted:
    if not new_username or not new_password:
        st.error("ユーザーIDとパスワードは必須です")
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

        # config読み込み
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            config = yaml.load(file, Loader=SafeLoader)

        # 重複チェック
        if new_username in config["credentials"]["usernames"]:
            st.error("このユーザーIDはすでに使われています")
        else:
            # パスワードハッシュ化
            hashed_password = stauth.utilities.hasher.Hasher.hash(new_password)

            # ユーザー追加
            config["credentials"]["usernames"][new_username] = {
                "name": new_name,
                "email": new_email,
                "password": hashed_password
            }

            # YAML保存
            with open(CONFIG_PATH, "w", encoding="utf-8") as file:
                yaml.dump(config, file, allow_unicode=True)

            # セッションに user_id 保存
            st.session_state["user_id"] = new_username

            # Supabase character テーブルに追加
            try:
                supabase.table("character").insert({
                    "user_id_text": st.session_state["user_id"]
                }).execute()
            except Exception as e:
                st.error(f"Supabase登録エラー: {e}")

            st.success("登録できました！ログイン画面からログインしてください。")

if st.button("ログイン画面へ戻る"):
    st.rerun()