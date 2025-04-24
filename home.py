import streamlit as st
import json
import os

st.set_page_config(page_title="🔐 Login", layout="centered")

users_file = "users.json"

# Load users from file
if os.path.exists(users_file):
    with open(users_file, "r") as f:
        users = json.load(f)
else:
    users = {}

# Tabs for login/register
tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

# 🔐 Login Tab
with tab1:
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = users[username]["role"]
            st.success(f"✅ Welcome, {username}!")
        else:
            st.error("❌ Invalid credentials")

# 📝 Registration Tab
with tab2:
    st.subheader("Create New Account")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    role = st.selectbox("Select Role", ["analyst", "admin"])

    if st.button("Register"):
        if new_user in users:
            st.warning("⚠️ Username already exists")
        elif not new_user or not new_pass:
            st.warning("Please fill in both fields")
        else:
            users[new_user] = {"password": new_pass, "role": role}
            with open(users_file, "w") as f:
                json.dump(users, f)
            st.success("✅ Account created! You can now log in.")
